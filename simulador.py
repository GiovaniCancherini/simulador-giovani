import yaml
from fila import Fila
from evento import Evento

class Simulador:
    def __init__(self, config_file, seed):
        self.global_time = 0
        self.iterations = 100000
        self.scheduler = []
        self.seed = seed
        self.queues = {}
        self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)

        for queue_name, queue_config in config['queues'].items():
            queue = Fila(
                name=queue_name,
                min_service=queue_config['service_time'][0],
                max_service=queue_config['service_time'][1],
                num_servers=queue_config['servers'],
                capacity=queue_config['capacity']
            )
            self.queues[queue_name] = queue

        for queue_name, queue_config in config['queues'].items():
            for dest, prob in queue_config['transitions'].items():
                self.queues[queue_name].transitions[dest] = prob

        self.initial_queue = config['initial_queue']
        self.initial_arrival_time = config['initial_arrival_time']
        self.min_arrival = config['arrival_time'][0]
        self.max_arrival = config['arrival_time'][1]

    def next_random(self):
        self.iterations -= 1
        a, M, c = 1103515245, 2**31, 12345
        self.seed = (a * self.seed + c) % M
        return self.seed / M

    def random_between(self, a, b):
        return a + (b - a) * self.next_random()

    def insert_event(self, event):
        for i, scheduled_event in enumerate(self.scheduler):
            if scheduled_event.time > event.time:
                self.scheduler.insert(i, event)
                return
        self.scheduler.append(event)

    def update_queues_time(self, time):
        for queue in self.queues.values():
            queue.times[queue.population] += (time - self.global_time)
        self.global_time = time

    def choose_next_queue(self, current_queue):
        rand = self.next_random()
        cumulative_prob = 0
        for dest, prob in current_queue.transitions.items():
            cumulative_prob += prob
            if rand < cumulative_prob:
                return dest
        return 'exit'

    def schedule_service(self, queue_name):
        queue = self.queues[queue_name]
        service_time = self.random_between(queue.min_service, queue.max_service)
        next_queue = self.choose_next_queue(queue)
        
        if next_queue == 'exit':
            event = Evento('exit', self.global_time + service_time, queue_source=queue_name)
        else:
            event = Evento('passage', self.global_time + service_time, queue_source=queue_name, queue_destiny=next_queue)
        
        self.insert_event(event)

    def arrival(self, queue_name, time):
        self.update_queues_time(time)
        queue = self.queues[queue_name]

        if queue.capacity == 0 or queue.population < queue.capacity:
            queue.population += 1
            if queue.population <= queue.num_servers:
                self.schedule_service(queue_name)
        else:
            queue.loss += 1

        next_arrival_time = self.global_time + self.random_between(self.min_arrival, self.max_arrival)
        self.insert_event(Evento('arrival', next_arrival_time, queue_destiny=self.initial_queue))

    def exit(self, event):
        self.update_queues_time(event.time)
        queue = self.queues[event.queue_source]
        queue.population -= 1
        if queue.population >= queue.num_servers:
            self.schedule_service(event.queue_source)

    def passage(self, event):
        self.update_queues_time(event.time)
        source_queue = self.queues[event.queue_source]
        dest_queue = self.queues[event.queue_destiny]

        source_queue.population -= 1
        if source_queue.population >= source_queue.num_servers:
            self.schedule_service(event.queue_source)

        if dest_queue.capacity == 0 or dest_queue.population < dest_queue.capacity:
            dest_queue.population += 1
            if dest_queue.population <= dest_queue.num_servers:
                self.schedule_service(event.queue_destiny)
        else:
            dest_queue.loss += 1

    def run(self):
        self.insert_event(Evento('arrival', self.initial_arrival_time, queue_destiny=self.initial_queue))

        while self.iterations > 0 and self.scheduler:
            event = self.scheduler.pop(0)
            if event.event_type == 'arrival':
                self.arrival(event.queue_destiny, event.time)
            elif event.event_type == 'exit':
                self.exit(event)
            elif event.event_type == 'passage':
                self.passage(event)

    def print_results(self):
        for queue_name, queue in self.queues.items():
            print('*' * 40)
            print(f'Queue {queue_name}: (G/G/{queue.num_servers}/{queue.capacity if queue.capacity > 0 else "∞"})')
            print(f'Service time: {queue.min_service} - {queue.max_service}')
            print('Transitions:')
            for dest, prob in queue.transitions.items():
                print(f'  {dest}: {prob:.2f}')
            print('-' * 40)
            print(f'{"State":<10}{"Times":<15}{"Probability":<15}')
            total_time = sum(queue.times.values())
            for state in sorted(queue.times.keys()):
                time = queue.times[state]
                prob = time / total_time if total_time > 0 else 0
                print(f'{state:<10}{time:<15.4f}{prob:.2%}')
            print(f'\nNumber of losses: {queue.loss}')

        print('=' * 40)
        print(f'Simulation time: {self.global_time:.2f}')
        print('=' * 40)