from intputer import Intputer

input_buffer = []
output_buffer = []

intputer = Intputer(input_buffer=input_buffer, output_buffer=output_buffer)
intputer.load_program('a11_input.txt')

panels = dict()
panels_painted = set()
robot_direction = 0
robot_location = (0,0)
moves = [(1,0),(0,1),(-1,0),(0,-1)]

def readPanel(pos):
    return panels.get(pos, 0)

def paintPanel(pos, color):
    panels_painted.add(pos)
    panels[pos] = color

def rotate(direction):
    global robot_direction
    if direction:
        robot_direction += 1
    else:
        robot_direction -= 1
    robot_direction = robot_direction % 4

def move():
    global robot_location
    robot_location = (robot_location[0] + moves[robot_direction][0], 
                      robot_location[1] + moves[robot_direction][1])

def process_output():
    while output_buffer:
        paintPanel(robot_location, output_buffer.pop(0))
        rotate(output_buffer.pop(0))
        move()

def read_camera():
    input_buffer.append(readPanel(robot_location))

paintPanel((0,0), 1) # Second star - starting panel is white
read_camera()
while intputer.running:
    intputer.run(pause_for_input=True)
    process_output()
    if intputer.running:
        read_camera()

# How big is the resulting message?
min_row = min([pos[0] for pos in panels])
max_row = max([pos[0] for pos in panels])
min_col = min([pos[1] for pos in panels])
max_col = max([pos[1] for pos in panels])

print('Second star answer: ')
for i in range(max_row, min_row-1, -1):
    outline = []
    for j in range(min_col, max_col+1):
        outline.append('#' if panels.get((i,j),0) else ' ')
    print(''.join(outline))


    