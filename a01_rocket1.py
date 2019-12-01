masses = []
with open('a01_input.txt', 'r') as f:
    for line in f:
        masses.append(int(line.strip()))

fuel = 0
for mass in masses:
    fuel += mass // 3 - 2

print(fuel)


