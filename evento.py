class Evento:
    def __init__(self, tipo, tempo):
        self.tipo = tipo  # "arrival", "departure", "passage"
        self.tempo = tempo
    
    def __lt__(self, other):
        return self.tempo < other.tempo
