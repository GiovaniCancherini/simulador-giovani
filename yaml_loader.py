import yaml
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class QueueConfig:
    servers: int
    min_service: float
    max_service: float
    capacity: int = float('inf')
    min_arrival: float = 0
    max_arrival: float = 0

@dataclass
class NetworkRoute:
    source: str
    target: str
    probability: float

class YAMLLoader:
    def __init__(self, yaml_file: str):
        with open(yaml_file, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.arrivals = self._parse_arrivals()
        self.queues = self._parse_queues()
        self.network = self._parse_network()
        self.random_numbers = self._parse_random_numbers()
    
    def _parse_arrivals(self) -> Dict[str, float]:
        return self.config.get('arrivals', {})
    
    def _parse_queues(self) -> Dict[str, QueueConfig]:
        queues = {}
        for name, config in self.config.get('queues', {}).items():
            # Adicionar validação para garantir que a soma das probabilidades é 1
            queues[name] = QueueConfig(
                servers=config['servers'],
                min_service=config['minService'],
                max_service=config['maxService'],
                capacity=config.get('capacity', float('inf')),
                min_arrival=config.get('minArrival', 0),
                max_arrival=config.get('maxArrival', 0)
            )
        return queues
    
    def validate_network(self):
        # Adicionar método para validar que a soma das probabilidades para cada fila é 1
        probabilities = {}
        for route in self.network:
            if route.source not in probabilities:
                probabilities[route.source] = 0
            probabilities[route.source] += route.probability
        
        for source, total_prob in probabilities.items():
            if abs(total_prob - 1.0) > 0.0001:
                raise ValueError(f"Probabilidades para a fila {source} somam {total_prob}, deveria ser 1.0")
    
    def _parse_network(self) -> List[NetworkRoute]:
        return [NetworkRoute(**route) for route in self.config.get('network', [])]
    
    def _parse_random_numbers(self) -> Tuple[List[float], List[int], int]:
        direct_numbers = self.config.get('rndnumbers', [])
        seeds = self.config.get('seeds', [])
        numbers_per_seed = self.config.get('rndnumbersPerSeed', 0)
        
        return direct_numbers, seeds, numbers_per_seed
