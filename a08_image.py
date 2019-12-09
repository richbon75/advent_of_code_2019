
def getinput():
    with open('a08_input.txt', 'r') as f:
        for line in f:
            line=line.strip()
    return line

def allDigits(line):
    for char in line:
        yield(int(char))

# main

layers = []
layer_stats = []
width = 25
height = 6
digits = allDigits(getinput())

try:
    while(True):
        current_layer = list()
        stats = [0,0,0]
        for i in range(height):
            current_row = list()
            for j in range(width):
                digit = digits.__next__()
                stats[digit] += 1
                current_row.append(digit)
            current_layer.append(current_row)
        layers.append(current_layer)
        layer_stats.append(stats)
except StopIteration as e:
    pass

min_zeros = float("inf")
min_stats = None
for stats in layer_stats:
    if stats[0] < min_zeros:
        min_zeros = stats[0]
        min_stats = stats[:]

print(f'First star answer: {min_stats[1] * min_stats[2]}')
