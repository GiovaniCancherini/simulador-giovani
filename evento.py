from dataclasses import dataclass
from typing import Optional

@dataclass
class Evento:
    tipo: str  # "arrival", "departure", "passage"
    tempo: float
    origem: Optional[str] = None
    destino: Optional[str] = None
    
    def __lt__(self, other):
        return self.tempo < other.tempo
