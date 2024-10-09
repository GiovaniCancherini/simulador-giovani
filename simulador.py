from yaml_loader import YAMLLoader
from fila import Fila
from evento import Evento
from escalonador import Escalonador

class Simulador:
    # Parâmetros globais do gerador de números aleatórios
    a = 1664525
    c = 1013904223
    M = 2**32
    seed = 12345

    def __init__(self, yaml_file: str):
        self.loader = YAMLLoader(yaml_file)
        self.loader.validate_network()  # Validar rede antes de iniciar
        self.queues = {}
        self.escalonador = Escalonador()
        self.global_time = 0
        self.last_event_time = 0  # Initialize last_event_time here
        self.random_count = 0
        self.random_numbers = self.loader.random_numbers[0]  # Usar números fornecidos
        self.current_random_index = 0
        
        self._setup_queues()
        self._setup_network()
    
    def next_random(self):
        # Usar números aleatórios fornecidos ou gerar novos
        if self.current_random_index < len(self.random_numbers):
            value = self.random_numbers[self.current_random_index]
            self.current_random_index += 1
        else:
            self.seed = (self.a * self.seed + self.c) % self.M
            value = self.seed / self.M
        
        self.random_count += 1
        return value
    
    def _setup_queues(self):
        for name, config in self.loader.queues.items():
            self.queues[name] = Fila(
                name=name,
                num_servers=config.servers,
                capacity=config.capacity,
                min_service=config.min_service,
                max_service=config.max_service,
                min_arrival=config.min_arrival,
                max_arrival=config.max_arrival
            )
    
    def _setup_network(self):
        for route in self.loader.network:
            if route.source in self.queues:
                self.queues[route.source].add_route(route.target, route.probability)
    
    def simulate(self, num_events: int):
        # Agenda eventos iniciais de chegada
        for queue_name, arrival_time in self.loader.arrivals.items():
            self.escalonador.add_event(Evento("arrival", arrival_time, destino=queue_name))
        
        while self.random_count < num_events:
            event = self.escalonador.get_next_event()
            if not event:
                break
            
            self.global_time = event.tempo
            self._process_event(event)
        
        return self._get_results()
    
    def _process_event(self, event: Evento):
        # Atualizar tempos acumulados para todas as filas
        time_increment = event.tempo - self.last_event_time
        for queue in self.queues.values():
            queue.accumulate_time(time_increment)
        self.last_event_time = event.tempo

        if event.tipo == "arrival":
            self._handle_arrival(event)
        elif event.tipo == "departure":
            self._handle_departure(event)
    
    def _handle_arrival(self, event: Evento):
        queue = self.queues[event.destino]
        if queue.can_accept():
            queue.in_queue()
            if queue.can_serve():
                queue.start_service()
                service_time = self._get_service_time(queue)
                self.escalonador.add_event(
                    Evento("departure", self.global_time + service_time, origem=event.destino)
                )
        else:
            queue.add_loss()
        
        # Schedule next arrival if this queue has external arrivals
        if queue.max_arrival > 0:
            arrival_time = self._get_arrival_time(queue)
            self.escalonador.add_event(
                Evento("arrival", self.global_time + arrival_time, destino=event.destino)
            )
    
    def _handle_departure(self, event: Evento):
        origin_queue = self.queues[event.origem]
        origin_queue.end_service()
        
        # Determinar próxima fila
        next_queue_name = origin_queue.get_route(self.next_random())
        
        if next_queue_name != "exit":
            # Criar evento de passagem
            passage_event = Evento(
                tipo="passage",
                tempo=self.global_time,
                origem=event.origem,
                destino=next_queue_name
            )
            self._handle_passage(passage_event)
        
        # Se há clientes esperando e servidores disponíveis, iniciar novo serviço
        if origin_queue.can_serve():
            origin_queue.start_service()
            service_time = self._get_service_time(origin_queue)
            self.escalonador.add_event(
                Evento("departure", self.global_time + service_time, origem=event.origem)
            )
            
    def _handle_passage(self, event: Evento):
        if event.destino not in self.queues:
            return  # Cliente saiu do sistema
        
        target_queue = self.queues[event.destino]
        if target_queue.can_accept():
            target_queue.in_queue()
            if target_queue.can_serve():
                target_queue.start_service()
                service_time = self._get_service_time(target_queue)
                self.escalonador.add_event(
                    Evento("departure", self.global_time + service_time, origem=event.destino)
                )
        else:
            target_queue.add_loss()
    
    def _get_service_time(self, queue: Fila) -> float:
        rnd = self.next_random()
        return queue.min_service + rnd * (queue.max_service - queue.min_service)
    
    def _get_arrival_time(self, queue: Fila) -> float:
        rnd = self.next_random()
        return queue.min_arrival + rnd * (queue.max_arrival - queue.min_arrival)
    
    def _get_results(self) -> dict:
        # Atualizar para incluir mais detalhes nos resultados
        results = {
            "global_time": self.global_time,
            "random_numbers_used": self.random_count,
            "queues": {}
        }
        
        for name, queue in self.queues.items():
            total_time = sum(queue.accumulated_times)
            probabilities = [time/total_time for time in queue.accumulated_times] if total_time > 0 else [0] * len(queue.accumulated_times)
            
            results["queues"][name] = {
                "lost_customers": queue.loss,
                "accumulated_times": queue.accumulated_times,
                "state_probabilities": probabilities,
                "routes": queue.routes
            }
        
        return results
    
    def _validate_model(self):
        # Verificar se todas as filas referenciadas existem
        for route in self.loader.network:
            if route.source not in self.queues and route.source != "exit":
                raise ValueError(f"Fila de origem inválida: {route.source}")
            if route.target not in self.queues and route.target != "exit":
                raise ValueError(f"Fila de destino inválida: {route.target}")
        
        # Verificar se todas as filas têm rotas definidas
        for queue_name in self.queues:
            total_prob = sum(route.probability for route in self.loader.network if route.source == queue_name)
            if abs(total_prob - 1.0) > 0.0001:
                raise ValueError(f"Soma das probabilidades para a fila {queue_name} é {total_prob}, deveria ser 1.0")