a = 1664525
c = 1013904223
M = 2**32
seed = 12345

def next_random():
    global seed
    seed = (a * seed + c) % M
    return seed / M

random_numbers = [next_random() for _ in range(10)]
print("#######################################################################################")
print("# SIMULADOR\n# ")
print("# Numeros aleatorios gerados:")
print("#", random_numbers)
print("# ")

def simulate_queue(num_events, arrival_interval, service_interval, max_queue_length):
    global_time = 0
    next_arrival = 2.0  # Primeiro cliente chega no tempo 2.0
    next_departure = float('inf')  # Inicialmente, sem clientes para atender
    queue = []
    events = []  # Lista para armazenar tempos de chegada e saída
    lost_customers = 0  # Contador de clientes perdidos
    accumulated_times = [0] * (max_queue_length + 1)  # Tempos acumulados para cada estado da fila
    
    while num_events > 0:
        # Determina o próximo evento
        if next_arrival < next_departure:
            global_time = next_arrival
            events.append((global_time, 'arrival'))
            num_events -= 1
            
            # Tratamento do evento de chegada
            if len(queue) < max_queue_length:
                queue.append(global_time)
                if len(queue) == 1:
                    # Cliente começa a ser atendido imediatamente
                    service_time = next_random() * (service_interval[1] - service_interval[0]) + service_interval[0]
                    next_departure = global_time + service_time
            else:
                # Cliente é perdido, pois a fila está cheia
                lost_customers += 1
            
            # Agendar próxima chegada
            interarrival_time = next_random() * (arrival_interval[1] - arrival_interval[0]) + arrival_interval[0]
            next_arrival = global_time + interarrival_time
            
        else:
            global_time = next_departure
            events.append((global_time, 'departure'))
            num_events -= 1
            
            # Tratamento do evento de saída
            queue.pop(0)
            if len(queue) > 0:
                # Próximo cliente começa a ser atendido
                service_time = next_random() * (service_interval[1] - service_interval[0]) + service_interval[0]
                next_departure = global_time + service_time
            else:
                # Fila vazia, sem cliente para atender
                next_departure = float('inf')
        
        # Atualizar tempos acumulados para cada estado da fila
        if len(queue) <= max_queue_length:
            accumulated_times[len(queue)] += global_time - events[-2][0] if len(events) > 1 else global_time
    
    # Calcular probabilidades dos estados da fila
    total_time = sum(accumulated_times)
    probabilities = [t / total_time for t in accumulated_times]
    
    return accumulated_times, probabilities, lost_customers, global_time

# Parâmetros de entrada
num_events = 100000
arrival_interval = (2.0, 5.0)
service_interval = (3.0, 5.0)
max_queue_length = 5

# Executar a simulação
times, probabilities, lost_customers, global_time = simulate_queue(num_events, arrival_interval, service_interval, max_queue_length)

# Resultados
print("# Tempos acumulados por estado:", times)
print("# ")
print("# Probabilidades dos estados:", probabilities)
print("# ")
print("# Clientes perdidos:", lost_customers)
print("# ")
print("# Tempo total de simulação:", global_time)
print("#######################################################################################")
