masses = []
with open('a01_input.txt', 'r') as f:
    for line in f:
        masses.append(int(line.strip()))

def fuel_needed(mass):
    if mass // 3 - 2 <= 0:
        return 0
    return (mass // 3 - 2) + fuel_needed(mass // 3 - 2)

fuel = 0
for mass in masses:
    fuel += fuel_needed(mass)

print(fuel)


