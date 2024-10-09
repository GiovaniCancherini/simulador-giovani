from typing import Dict, Tuple

class Fila:
    def __init__(self, name, num_servers, min_service, max_service, capacity=float('inf')):
        self.name = name
        self.num_servers = num_servers
        self.capacity = capacity
        self.min_service = min_service
        self.max_service = max_service
        
        self.customers_in_queue = 0
        self.customers_in_service = 0
        self.losses = 0
        self.routes = {}
        
        # Ajuste no cálculo do tamanho máximo de estados
        if self.capacity < float('inf'):
            self.max_state = self.capacity
        else:
            self.max_state = max(self.num_servers + 10, 20)  # Garantir um mínimo de estados
        
        self.accumulated_times = [0.0] * (self.max_state + 1)  # +1 para incluir o estado 0
    
    def add_route(self, target: str, probability: float):
        self.routes[target] = probability
    
    def get_route(self, random_value: float) -> str:
        cumulative_prob = 0
        for target, prob in self.routes.items():
            cumulative_prob += prob
            if random_value < cumulative_prob:
                return target
        return list(self.routes.keys())[-1]  # Retorna a última rota como fallback
    
    def status(self) -> int:
        return self.customers
    
    def get_capacity(self) -> float:
        return self.capacity
    
    def get_servers(self) -> int:
        return self.num_servers
    
    def add_loss(self):
        self.loss += 1
     
    def start_service(self):
        if self.can_serve():
            self.busy_servers += 1
    
    def end_service(self):
        if self.busy_servers > 0:
            self.busy_servers -= 1
            self.customers -= 1
    
    def in_queue(self):
        self.customers += 1
    
    def try_accept_customer(self) -> bool:
        total_customers = self.customers_in_queue + self.customers_in_service
        
        if total_customers < self.capacity:
            if self.customers_in_service < self.num_servers:
                self.customers_in_service += 1
            else:
                self.customers_in_queue += 1
            return True
        else:
            self.losses += 1
            return False
    
    def complete_service(self):
        if self.customers_in_service > 0:
            self.customers_in_service -= 1
            if self.customers_in_queue > 0:
                self.customers_in_queue -= 1
                self.customers_in_service += 1
    
    def can_accept(self) -> bool:
        return self.customers < self.capacity
    
    def can_serve(self) -> bool:
        return self.customers_in_service < self.num_servers and \
               (self.customers_in_queue > 0 or self.customers_in_service < self.num_servers)
    
    def accumulate_time(self, time_increment: float):
        total_customers = self.customers_in_queue + self.customers_in_service
        if total_customers <= self.max_state:
            self.accumulated_times[total_customers] += time_increment
        else:
            # Se por algum motivo tivermos mais clientes que o esperado,
            # acumular no último estado
            self.accumulated_times[self.max_state] += time_increment
