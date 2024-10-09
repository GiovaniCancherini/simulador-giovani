from dataclasses import dataclass
from typing import Optional

@dataclass
class Evento:
    tipo: str  # Agora incluindo "passage" além de "arrival" e "departure"
    tempo: float
    origem: Optional[str] = None
    destino: Optional[str] = None
    
    def __lt__(self, other):
        return self.tempo < other.tempo

    # Método auxiliar para facilitar o debugging
    def __str__(self):
        if self.tipo == "arrival":
            return f"Arrival at {self.destino} at time {self.tempo}"
        elif self.tipo == "departure":
            return f"Departure from {self.origem} at time {self.tempo}"
        else:  # passage
            return f"Passage from {self.origem} to {self.destino} at time {self.tempo}"
