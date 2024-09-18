from simulador import simulate_tandem_queues

# Parâmetros para G/G/2/3
num_events = 100000
arrival_interval = (1.0, 4.0)
service_interval1 = (3.0, 4.0)
max_queue_length1 = 3
num_servers1 = 2

print("#######################################################################################")
print("# FILA G/G/2/3:")
times1, _, lost_customers1, _, global_time = simulate_tandem_queues(
    num_events, arrival_interval, service_interval1, (0, 0), max_queue_length1, 0, num_servers1, 0
)
print("# Tempos acumulados por estado - Fila 1:", times1)
print("# Clientes perdidos na Fila 1:", lost_customers1)
print("# Tempo total de simulação:", global_time)
print("#")

# Parâmetros para G/G/1/5
service_interval2 = (2.0, 3.0)
max_queue_length2 = 5
num_servers2 = 1

print("# FILA G/G/1/5:")
times2, _, lost_customers2, _, global_time = simulate_tandem_queues(
    num_events, arrival_interval, service_interval2, (0, 0), max_queue_length2, 0, num_servers2, 0
)
print("# Tempos acumulados por estado - Fila 2:", times2)
print("# Clientes perdidos na Fila 2:", lost_customers2)
print("# Tempo total de simulação:", global_time)
print("#######################################################################################")
