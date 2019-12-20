from itertools import combinations
from pprint import pprint

data = '''<x=-2, y=9, z=-5>
<x=16, y=19, z=9>
<x=0, y=3, z=6>
<x=11, y=0, z=11>'''

positions = []
velocities = []
steps = 0

# Turn the raw data into an array of values
for line in data.splitlines():
    line = ''.join([c for c in line if c not in '<xyz=>'])
    positions.append([int(i) for i in line.split(',')])
    velocities.append([0 for i in range(len(positions[-1]))])

def gravity():
    '''Apply gravity to the velocities'''
    # for each axis, compare every pair of planets and adjust
    for a in range(0,len(velocities[0])):
        for i, j in combinations(range(0,4), 2):
            if positions[i][a] > positions[j][a]:
                velocities[i][a] -= 1
                velocities[j][a] += 1
            elif positions[i][a] < positions[j][a]:
                velocities[i][a] += 1
                velocities[j][a] -= 1

def velocity():
    '''Apply velocity to every position'''
    for i in range(0,len(velocities)):
        for j in range(0,len(velocities[i])):
            positions[i][j] += velocities[i][j]

def step(s=1):
    '''Go forward this many steps'''
    global steps
    for _ in range(0,s):
        steps += 1
        gravity()
        velocity()

def output():
    print(f'Situation at step {steps}')
    pprint(positions)
    pprint(velocities)

def energy():
    '''Calculate the "energy" in the system'''
    return sum([sum([abs(a) for a in p])*sum([abs(b) for b in v]) for p, v in zip(positions, velocities)])

# output()
step(1000)
# output()
print(f'Energy: {energy()}')





