class Evento:
    def __init__(self, event_type, time, queue_source=None, queue_destiny=None):
        self.event_type = event_type
        self.time = time
        self.queue_source = queue_source
        self.queue_destiny = queue_destiny
