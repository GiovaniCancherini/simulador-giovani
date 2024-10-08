from typing import Dict, Tuple

class Fila:
    def __init__(self, name: str, num_servers: int, capacity: float,
                 min_service: float, max_service: float,
                 min_arrival: float = 0, max_arrival: float = 0):
        self.name = name
        self.num_servers = num_servers
        self.capacity = capacity
        self.min_service = min_service
        self.max_service = max_service
        self.min_arrival = min_arrival
        self.max_arrival = max_arrival
        self.customers = 0
        self.busy_servers = 0
        self.loss = 0
        self.accumulated_times = [0] * (int(capacity) + 1 if capacity != float('inf') else 1)
        self.routes: Dict[str, float] = {}
    
    def add_route(self, target: str, probability: float):
        self.routes[target] = probability
    
    def get_route(self, random_value: float) -> str:
        cumulative_prob = 0
        for target, prob in self.routes.items():
            cumulative_prob += prob
            if random_value < cumulative_prob:
                return target
        return "exit"  # Se nenhuma rota for escolhida, o cliente sai do sistema
    
    def status(self) -> int:
        return self.customers
    
    def get_capacity(self) -> float:
        return self.capacity
    
    def get_servers(self) -> int:
        return self.num_servers
    
    def add_loss(self):
        self.loss += 1
    
    def can_accept(self) -> bool:
        return self.customers < self.capacity
    
    def can_serve(self) -> bool:
        return self.busy_servers < self.num_servers and self.customers > 0
    
    def start_service(self):
        if self.can_serve():
            self.busy_servers += 1
    
    def end_service(self):
        if self.busy_servers > 0:
            self.busy_servers -= 1
            self.customers -= 1
    
    def in_queue(self):
        self.customers += 1
    
    def accumulate_time(self, time_increment: float):
        state = min(self.customers, len(self.accumulated_times) - 1)
        self.accumulated_times[state] += time_increment
