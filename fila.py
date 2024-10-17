from collections import defaultdict

class Fila:
    def __init__(self, name, min_service, max_service, num_servers, capacity):
        self.name = name
        self.min_service = min_service
        self.max_service = max_service
        self.num_servers = num_servers
        self.capacity = capacity
        self.population = 0
        self.times = defaultdict(float)
        self.loss = 0
        self.transitions = {}