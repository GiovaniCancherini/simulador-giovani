from simulador import Simulador

def print_results(results):
    print(f"Tempo global de simulação: {results['global_time']:.2f}")
    print(f"Números aleatórios utilizados: {results['random_numbers_used']}")
    
    print("\nResultados por fila:")
    for queue_name, queue_results in results['queues'].items():
        print(f"\nFila {queue_name}:")
        print(f"  Clientes perdidos: {queue_results['lost_customers']}")
        
        print(f"  Probabilidades de estado:")
        for i, prob in enumerate(queue_results['state_probabilities']):
            print(f"    Estado {i}: {prob:.4f}")
        
        print(f"  Rotas:")
        for target, prob in queue_results['routes'].items():
            print(f"    Para {target}: {prob:.2f}")

def main():
    simulador = Simulador("model.yaml")
    results = simulador.simulate(100000)  # Vai usar 100000 números aleatórios
    print_results(results)

if __name__ == "__main__":
    main()