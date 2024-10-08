from simulador import Simulador

def print_results(results):
    print(f"Tempo global de simulação: {results['global_time']:.2f}")
    print(f"Números aleatórios utilizados: {results['random_numbers_used']}")
    print("\nResultados por fila:")
    for queue_name, queue_results in results['queues'].items():
        print(f"\nFila {queue_name}:")
        print(f"  Clientes perdidos: {queue_results['lost_customers']}")
        
        # Calcula as probabilidades de estado
        total_time = sum(queue_results['accumulated_times'])
        
        print(f"  Probabilidades de estado:")
        if total_time > 0:
            probabilities = [time/total_time for time in queue_results['accumulated_times']]
            for i, prob in enumerate(probabilities):
                print(f"    Estado {i}: {prob:.4f}")
        else:
            print("    Não há dados suficientes para calcular probabilidades (tempo total é zero)")

def main():
    simulador = Simulador("model.yaml")
    results = simulador.simulate(100000)  # Vai usar 100000 números aleatórios
    print_results(results)

if __name__ == "__main__":
    main()