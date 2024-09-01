a = 1664525
c = 1013904223
M = 2**32
seed = 12345

def next_random():
    global seed
    seed = (a * seed + c) % M
    return seed / M

random_numbers = [next_random() for _ in range(10)]

"""
- /G/1/5, chegadas entre 2...5, atendimento entre 3...5;
- G/G/2/5, chegadas entre 2...5, atendimento entre 3…5.

int count = 100000;
...
while (count > 0) {
	evento = NextEvent();
	if (evento == tipo_chegada) {
		CHEGADA (evento);
	} else if (evento == tipo_saida) {
		SAIDA (evento);
	}
}
"""
def simulate_queue(num_events, arrival_interval, service_interval, max_queue_length):
    global_time = 0
    next_arrival = 2.0  # Primeiro cliente chega no tempo 2.0
    next_departure = 0
    queue = []
    events = []  
    lost_customers = 0 
    
    while num_events > 0:
        # Determina o próximo evento
        if next_arrival < next_departure:
            global_time = next_arrival
            events.append((global_time, 'arrival'))
            num_events -= 1
            
            if len(queue) < max_queue_length:
                queue.append(global_time)
                
            else:
                lost_customers += 1
            
            interarrival_time = next_random() * (arrival_interval[1] - arrival_interval[0]) + arrival_interval[0]
            next_arrival = global_time + interarrival_time
            
        else:
            global_time = next_departure
            events.append((global_time, 'departure'))
            num_events -= 1
            
            if len(queue) > 0:
                service_time = next_random() * (service_interval[1] - service_interval[0]) + service_interval[0]
                next_departure = global_time + service_time
            else:
                next_departure = float('inf')
        
        
    # Calcular probabilidades dos estados da fila
    
    return global_time

# Parâmetros de entrada
num_events = 10
arrival_interval = (2.0, 5.0)
service_interval = (3.0, 5.0)
max_queue_length = 5

global_time = simulate_queue(num_events, arrival_interval, service_interval, max_queue_length)

print("Tempo total de simulação:", global_time)
