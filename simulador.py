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
        self.loader.validate_network()
        self.queues = {}
        self.escalonador = Escalonador()
        self.global_time = 0.0
        self.last_event_time = 0.0
        self.random_count = 0
        self.random_numbers = self.loader.random_numbers
        self.current_random_index = 0
        
        self._setup_queues()
        self._setup_network()
    
    def next_random(self):
        if self.current_random_index < len(self.random_numbers):
            value = self.random_numbers[self.current_random_index]
        else:
            # Gerador congruencial linear
            self.seed = (self.a * self.seed + self.c) % self.M
            value = self.seed / self.M
        
        self.current_random_index += 1
        self.random_count += 1
        return value
    
    def _setup_queues(self):
        for name, config in self.loader.queues.items():
            self.queues[name] = Fila(
                name=name,
                num_servers=config.servers,
                capacity=config.capacity,
                min_service=config.min_service,
                max_service=config.max_service
            )
    
    def _setup_network(self):
        for route in self.loader.network:
            if route.source in self.queues:
                self.queues[route.source].add_route(route.target, route.probability)
    
    def simulate(self, num_events: int):
        # schedule initial arrivals
        for queue_name, arrival_time in self.loader.arrivals.items():
            self.escalonador.add_event(Evento("arrival", arrival_time, destino=queue_name))
        
        while self.random_count < num_events: # TODO: PROBLEMA AQUI, LOOP INFINITO
            event = self.escalonador.get_next_event()
            if not event:
                break
            
            self.global_time = event.tempo
            self._process_event(event) # AQUI DEVERIA ACABAR ATUALIZANDO O self.random_count
        
        return self._get_results()
    
    def _process_event(self, event: Evento):
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
        accepted = queue.try_accept_customer()
        
        if accepted:
            if queue.can_serve():
                service_time = self._get_service_time(queue)
                self.escalonador.add_event(
                    Evento("departure", self.global_time + service_time, origem=event.destino)
                )
        
        # Schedule next arrival for Q1 only
        if event.destino == "Q1":
            next_arrival = self.loader.arrivals["Q1"]
            self.escalonador.add_event(
                Evento("arrival", self.global_time + next_arrival, destino="Q1")
            )
    
    def _handle_departure(self, event: Evento):
        origin_queue = self.queues[event.origem]
        origin_queue.complete_service()
        
        next_queue = self._get_next_queue(origin_queue)
        
        if next_queue != "exit":
            arrival_event = Evento("arrival", self.global_time, destino=next_queue)
            self._handle_arrival(arrival_event)
        
        if origin_queue.can_serve():
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
    
    def _get_next_queue(self, queue: Fila) -> str:
        rand = self.next_random()
        cumulative = 0.0
        for target, probability in queue.routes.items():
            cumulative += probability
            if rand < cumulative:
                return target
        return list(queue.routes.keys())[-1]  # Fallback to last route
    
    def _get_service_time(self, queue: Fila) -> float:
        rnd = self.next_random()
        return queue.min_service + rnd * (queue.max_service - queue.min_service)
    
    def _get_arrival_time(self, queue: Fila) -> float:
        rnd = self.next_random()
        return queue.min_arrival + rnd * (queue.max_arrival - queue.min_arrival)
    
    def _get_results(self) -> dict:
        results = {
            "global_time": self.global_time,
            "random_numbers_used": self.random_count,
            "queues": {}
        }
        
        for name, queue in self.queues.items():
            total_time = sum(queue.accumulated_times)
            probabilities = [time/total_time for time in queue.accumulated_times] if total_time > 0 else [0] * (queue.capacity + 1)
            
            results["queues"][name] = {
                "lost_customers": queue.losses,
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