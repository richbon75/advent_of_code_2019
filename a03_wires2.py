# Let's convert the wire directions to a series of lines defined by start and end points.
# Then we can compare all the line segments of one wire to all the line segments of the other wire
# and see where we have crossings.

import pprint

def is_vertical(line):
    '''A vertical line segment will have the same X value for both points.'''
    if line[0][0] == line[1][0]:
        return True
    return False

def point_in_segment(point, line):
    '''Check if a point (x, y) is within a line segment ((x1, y1),(x2, y2)).
    Assumes the point is known to be on the line, just checking the segment bounds.'''
    return ((min(line[0][0], line[1][0]) <= point[0] <= max(line[0][0], line[1][0])) and
           (min(line[0][1], line[1][1]) <= point[1] <= max(line[0][1], line[1][1])))

def intersection(line1, line2):
    '''Return the intersection point of the horizontal and vertical segments,
    else None if there is no intersection.  Assumes segments are exactly 
    vertical or horizontal.'''
    if is_vertical(line1) == is_vertical(line2):
        # Both lines can't be vertical, and both lines can't be horizontal
        return None
    # Get candidate (x,y) intersection
    if is_vertical(line1):
        x = line1[0][0]
        y = line2[0][1]
    else:
        x = line2[0][0]
        y = line1[0][1]
    # Check if it is within the segments
    if point_in_segment((x,y), line1) and point_in_segment((x,y), line2):
        return (x,y)
    return None

def segment_length(line):
    '''How long is the segment?'''
    return abs(line[0][0] - line[1][0]) + abs(line[0][1] - line[1][1])

wireroutes = []
wires = []

with open('a03_input.txt', 'r') as f:
# f = "R8,U5,L5,D3\nU7,R6,D4,L4"
# f = "R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83"
# f = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
# f = f.split('\n')
    for line in f:
        line = line.strip()
        if line:
            moves = line.split(',')
            wireroutes.append(moves)

def convert_to_pairs(wireroute):
    '''Convert a set of wireroutes (starting at the origin) into co-ordinate pairs
    as (x1, y1, x2, y2) tuples.'''
    wire = []
    current_pos = (0, 0)
    directions = (0, 0)
    for segment in wireroute:
        if segment[0] == 'R':
            directions = (1, 0)
        elif segment[0] == 'L':
            directions = (-1, 0)
        elif segment[0] == 'U':
            directions = (0, 1)
        else:
            directions = (0, -1)
        distance = int(segment[1:])
        to_pos = (current_pos[0] + (directions[0] * distance),
                current_pos[1] + (directions[1] * distance))
        wire.append((current_pos, to_pos))
        current_pos = to_pos
    return wire

for wireroute in wireroutes:
    wires.append(convert_to_pairs(wireroute))

import pprint
pprint.pprint(wires)

# Find all the intersections
intersections = []
shortest_point = None
shortest_distance = float("inf")

line1_distance = 0
for line1 in wires[0]:
    
    line2_distance = 0
    for line2 in wires[1]:
        point = intersection(line1, line2)
        if point and point != (0,0):
            intersections.append(point)
            print(f'Intersection found: {intersections[-1]} between {line1} and {line2}')
            point_distance = (line1_distance + line2_distance +
                segment_length((line1[0], point)) + segment_length((line2[0], point)))
            if point_distance < shortest_distance:
                print("It's a shorter distance!")
                shortest_point = point
                shortest_distance = point_distance
        line2_distance += segment_length(line2)
    line1_distance += segment_length(line1)

pprint.pprint(intersections)

# Find the intersection closest to the origin (via Manhattan distance)
closest_point = None
closest_distance = float("inf")

for point in intersections:
    if abs(point[0]) + abs(point[1]) < closest_distance:
        closest_distance = abs(point[0]) + abs(point[1])
        closest_point = point

print(f'Closest intersection: {closest_point}')
print(f"Its distance is: {closest_distance}")

print(f'Shortest intersecton: {shortest_point}')
print(f"Shortest distance: {shortest_distance}")
