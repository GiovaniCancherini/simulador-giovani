a = 1664525
c = 1013904223
M = 2**32
seed = 12345

def next_random():
    global seed
    seed = (a * seed + c) % M
    return seed / M

random_numbers = [next_random() for _ in range(10)]
print(random_numbers)