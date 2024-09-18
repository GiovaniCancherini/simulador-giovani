class Fila:
    def __init__(self, num_servers, capacity, min_arrival, max_arrival, min_service, max_service):
        self.num_servers = num_servers
        self.capacity = capacity
        self.min_arrival = min_arrival
        self.max_arrival = max_arrival
        self.min_service = min_service
        self.max_service = max_service
        self.customers = 0
        self.loss = 0
        self.accumulated_times = [0] * (capacity + 1)
    
    def status(self):
        return self.customers
    
    def get_capacity(self):
        return self.capacity
    
    def get_servers(self):
        return self.num_servers
    
    def add_loss(self):
        self.loss += 1
    
    def in_queue(self):
        self.customers += 1
    
    def out_queue(self):
        if self.customers > 0:
            self.customers -= 1
        else:
            raise ValueError("No customers to remove from queue")
    
    def accumulate_time(self, state, time_increment):
        if state <= self.capacity:
            self.accumulated_times[state] += time_increment
