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
    next_departure = float('inf')  # Inicialmente, sem clientes para atender
    queue = []
    events = []  # Lista para armazenar tempos de chegada e saída
    lost_customers = 0  # Contador de clientes perdidos
    
    while num_events > 0:
        if next_arrival < next_departure:
            global_time = next_arrival
            events.append((global_time, 'arrival'))
            num_events -= 1
            
            # Tratamento do evento de chegada
            if len(queue) < max_queue_length:
                #   
                
            # Agendar próxima chegada
        
        else:
            # else
    return global_time
            

num_events = 10
arrival_interval = (2.0, 5.0)
service_interval = (3.0, 5.0)
max_queue_length = 5

global_time = simulate_queue(num_events, arrival_interval, service_interval, max_queue_length)

print("Tempo total de simulação:", global_time)
