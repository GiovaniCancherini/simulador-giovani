from simulador import simulate_tandem_queues

# Parâmetros de entrada para a primeira simulação (G/G/2/3)
num_events = 100000
arrival_interval_gg23 = (1.0, 4.0)
service_interval1_gg23 = (3.0, 4.0)
service_interval2_gg23 = (3.0, 4.0)
max_queue_length1_gg23 = 3
max_queue_length2_gg23 = 3
num_servers1_gg23 = 2
num_servers2_gg23 = 2

# Parâmetros de entrada para a segunda simulação (G/G/1/5)
service_interval1_gg15 = (2.0, 3.0)
service_interval2_gg15 = (2.0, 3.0)
max_queue_length1_gg15 = 5
max_queue_length2_gg15 = 5
num_servers1_gg15 = 1
num_servers2_gg15 = 1

print("#######################################################################################")

# Simulação G/G/2/3, chegadas entre 1..4, atendimento entre 3..4
print("___Simulação G/G/2/3, chegadas entre 1..4, atendimento entre 3..4:")
times1_gg23, times2_gg23, lost_customers1_gg23, lost_customers2_gg23, global_time_gg23, num_chegadas_1_4, num_atendimentos_3_4, _ = simulate_tandem_queues(
    num_events, arrival_interval_gg23, service_interval1_gg23, service_interval2_gg23,
    max_queue_length1_gg23, max_queue_length2_gg23, num_servers1_gg23, num_servers2_gg23
)
print("Tempos acumulados por estado - Fila 1:", times1_gg23)
print("Tempos acumulados por estado - Fila 2:", times2_gg23)
print("Clientes perdidos na Fila 1:", lost_customers1_gg23)
print("Clientes perdidos na Fila 2:", lost_customers2_gg23)
print("Número de chegadas entre 1..4:", num_chegadas_1_4)
print("Número de atendimentos entre 3..4:", num_atendimentos_3_4)
print("Tempo global de simulação:", global_time_gg23)
print("#######################################################################################")

# Simulação G/G/1/5, chegadas entre 1..4, atendimento entre 2..3
print("___Simulação G/G/1/5, chegadas entre 1..4, atendimento entre 2..3:")
times1_gg15, times2_gg15, lost_customers1_gg15, lost_customers2_gg15, global_time_gg15, _, _, num_atendimentos_2_3 = simulate_tandem_queues(
    num_events, arrival_interval_gg23, service_interval1_gg15, service_interval2_gg15,
    max_queue_length1_gg15, max_queue_length2_gg15, num_servers1_gg15, num_servers2_gg15
)
print("Tempos acumulados por estado - Fila 1:", times1_gg15)
print("Tempos acumulados por estado - Fila 2:", times2_gg15)
print("Clientes perdidos na Fila 1:", lost_customers1_gg15)
print("Clientes perdidos na Fila 2:", lost_customers2_gg15)
print("Número de atendimentos entre 2..3:", num_atendimentos_2_3)
print("Tempo global de simulação:", global_time_gg15)
print("#######################################################################################")
