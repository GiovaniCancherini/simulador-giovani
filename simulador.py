from fila import Fila
from evento import Evento
from escalonador import Escalonador

# Parâmetros globais do gerador de números aleatórios
a = 1664525
c = 1013904223
M = 2**32
seed = 12345

def next_random():
    global seed
    seed = (a * seed + c) % M
    return seed / M

def simulate_tandem_queues(num_events, arrival_interval, service_interval1, service_interval2, max_queue_length1, max_queue_length2, num_servers1, num_servers2):
    global_time = 1.5
    queue1 = Fila(num_servers1, max_queue_length1, arrival_interval[0], arrival_interval[1], service_interval1[0], service_interval1[1])
    queue2 = Fila(num_servers2, max_queue_length2, 0, 0, service_interval2[0], service_interval2[1])  # Fila 2 sem chegada externa
    escalonador = Escalonador()
    
    # Inicializa o primeiro evento de chegada
    escalonador.add_event(Evento("arrival", global_time))
    
    while num_events > 0:
        current_event = escalonador.get_next_event()
        if not current_event:
            break
        global_time = current_event.tempo
        num_events -= 1
        
        if current_event.tipo == "arrival":
            chegada_fila1(queue1, escalonador, global_time, arrival_interval)
        
        elif current_event.tipo == "departure":
            saida_fila1(queue1, queue2, escalonador, global_time, service_interval1)
        
        elif current_event.tipo == "passage":
            passagem_fila1_fila2(queue1, queue2, escalonador, global_time, service_interval2)
    
    # Retornar dados de simulação
    return queue1.accumulated_times, queue2.accumulated_times, queue1.loss, queue2.loss, global_time

def chegada_fila1(queue1, escalonador, global_time, arrival_interval):
    if queue1.status() < queue1.get_capacity():
        queue1.in_queue()
        # Planejar a próxima chegada
        interarrival_time = next_random() * (arrival_interval[1] - arrival_interval[0]) + arrival_interval[0]
        escalonador.add_event(Evento("arrival", global_time + interarrival_time))
    else:
        queue1.add_loss()
    
def saida_fila1(queue1, queue2, escalonador, global_time, service_interval1):
    if queue1.status() > 0:
        queue1.out_queue()
        # Planejar passagem para a Fila 2
        service_time = next_random() * (service_interval1[1] - service_interval1[0]) + service_interval1[0]
        escalonador.add_event(Evento("passage", global_time + service_time))

def passagem_fila1_fila2(queue1, queue2, escalonador, global_time, service_interval2):
    if queue2.status() < queue2.get_capacity():
        queue2.in_queue()
        # Planejar saída da Fila 2
        service_time = next_random() * (service_interval2[1] - service_interval2[0]) + service_interval2[0]
        escalonador.add_event(Evento("departure", global_time + service_time))
    else:
        queue2.add_loss()
