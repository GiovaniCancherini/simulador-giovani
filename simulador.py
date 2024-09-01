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
num_events = 100000
arrival_interval = (2.0, 5.0)
service_interval = (3.0, 5.0)
max_queue_length = 5


def simulate_queue():
    global_time = 0
    