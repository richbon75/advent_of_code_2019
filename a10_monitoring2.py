def dist(a, b):
    '''Distance between points a and b'''
    return math.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)

import math

asteroids = []

with open('a10_input.txt','r') as f:
    data = f.read()

y=0
for row in data.split('\n'):
    row = row.strip()
    x = 0
    for char in row:
        if char == '#':
            asteroids.append((x,y))
        x += 1
    y += 1

# print(asteroids)

max_bearings = 0
best_station = None
for station in asteroids:
    bearings = set()
    for asteroid in asteroids:
        if station == asteroid:
            continue
        bearing = math.atan2(station[0]-asteroid[0], station[1]-asteroid[1])
        # print(f'from {station} to {asteroid}: {bearing}')
        bearings.add(bearing)
    if len(bearings) > max_bearings:
        max_bearings = len(bearings)
        best_station = station
print(f"Station {best_station} can see {max_bearings} asteroids.")

station = best_station
bearings = {}
for asteroid in asteroids:
    if station == asteroid:
        continue
    bearing = math.atan2(station[0]-asteroid[0], station[1]-asteroid[1])
    if bearing not in bearings:
        bearings[bearing] = list()
    bearings[bearing].append(asteroid)

# sort all the asteroid chains nearest-to-farthest
for b in bearings:
    bearings[b].sort(key=lambda x: dist(station, x))

vaporized = 0  # number of asteroids destroyed
done = False
while not done:
    # Get a sorted list of the remaining bearings in rotational order
    bs = sorted(bearings, key=lambda x: -x if x<=0 else 10-x)
    for b in bs:
        asteroid = bearings[b].pop(0)
        vaporized += 1
        # print(f'{vaporized} Vaporized {asteroid} at bearing {b}')
        if vaporized == 200:
            print(f'200th asteroid vaporized: {asteroid}  Second star code: {asteroid[0]*100+asteroid[1]}')
            done = True
            break
        # if there are no more asteroids on this bearing, delete the bearing entry.
        if not bearings[b]:
            del bearings[b]



