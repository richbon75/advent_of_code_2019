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





