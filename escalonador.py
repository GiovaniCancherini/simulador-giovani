import heapq

class Escalonador:
    def __init__(self):
        self.event_queue = []
    
    def add_event(self, evento):
        heapq.heappush(self.event_queue, evento)
    
    def get_next_event(self):
        return heapq.heappop(self.event_queue) if self.event_queue else None
    
    def peek_next_event(self):
        return self.event_queue[0] if self.event_queue else None
    
    def is_empty(self):
        return len(self.event_queue) == 0
