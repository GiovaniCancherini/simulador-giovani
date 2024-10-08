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
        self.queues = {}
        self.escalonador = Escalonador()
        self.global_time = 0
        self.random_count = 0
        
        self._setup_queues()
        self._setup_network()
    
    def next_random(self):
        self.seed = (self.a * self.seed + self.c) % self.M
        self.random_count += 1
        return self.seed / self.M
    
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
        
        # Determine next queue
        next_queue = origin_queue.get_route(self.next_random())
        
        if next_queue != "exit" and next_queue in self.queues:
            target_queue = self.queues[next_queue]
            if target_queue.can_accept():
                target_queue.in_queue()
                if target_queue.can_serve():
                    target_queue.start_service()
                    service_time = self._get_service_time(target_queue)
                    self.escalonador.add_event(
                        Evento("departure", self.global_time + service_time, origem=next_queue)
                    )
            else:
                target_queue.add_loss()
        
        # If there are customers waiting and servers available, start new service
        if origin_queue.can_serve():
            origin_queue.start_service()
            service_time = self._get_service_time(origin_queue)
            self.escalonador.add_event(
                Evento("departure", self.global_time + service_time, origem=event.origem)
            )
    
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
            results["queues"][name] = {
                "lost_customers": queue.loss,
                "accumulated_times": queue.accumulated_times
            }
        
        return results