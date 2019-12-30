import random
from intputer import Intputer

class Droidmap:

    movemap = {
        'N': {"dircode": 1, "dirmove": (-1, 0)},
        'S': {"dircode": 2, "dirmove": ( 1, 0)},
        'W': {"dircode": 3, "dirmove": ( 0,-1)},
        'E': {"dircode": 4, "dirmove": ( 0, 1)}
    }

    directions = ('N', 'E', 'S', 'W')

    map_symbols = {
        None: ' ',
        0: '#',
        1: '.',
        2: '0'
    }

    def __init__(self, data):
        self.droid_loc = (0,0)
        self.last_move = 0
        self.map = {(0,0):1}
        self.input_buffer = list()
        self.output_buffer = list()
        self.intputer = Intputer(input_buffer=self.input_buffer, output_buffer=self.output_buffer, name="Droid")
        self.intputer.load_program(data)
        self.move_count = 1
        self.o2at = None
        self.current_direction = 0
    
    def rightside_explore(self):
        '''Traverse the entire map keeping the wall to our right.
        Assuming the maze is a closed space, we'll eventually loop
        back to the starting point after having explored the entire maze.'''
        while not (self.droid_loc == (0,0) and self.move_count > 20):
            # Try to move forward.
            result = self.one_move(self.directions[self.current_direction])
            # Blocked? Turn left.
            if not result:
                self.current_direction = (self.current_direction - 1) % 4
            # Free? Turn right.
            else:
                self.current_direction = (self.current_direction + 1) % 4
    
    def one_move(self, move):
        self.move_count += 1
        self.last_move = move
        self.input_buffer.append(self.movemap[move]["dircode"])
        self.intputer.run(pause_for_input=True)
        if self.output_buffer:
            result = self.handle_output()
            return result
        return None 

    def run_random(self):
        '''Not used - makes random moves until it finds the O2'''
        self.random_move()
        while self.intputer.running and self.move_count > 0:
            self.intputer.run(pause_for_input=True)
            if self.output_buffer:
                self.handle_output()
            if self.o2at:
                self.move_count -= 1
            else:
                self.move_count += 1
            self.random_move()
    
    def move_input(self):
        '''Not used. Originally for manual exploration of the map.'''
        move = input('Enter a move: N, S, E, W: ')
        move = move.upper()
        self.last_move = move
        self.input_buffer.append(self.movemap[move]["dircode"])
    
    def random_move(self):
        '''Not used, but this was a first method to test exploring the map.
        It works, but takes too long.'''
        move = random.choice(['N','S','E','W'])
        self.last_move = move
        self.input_buffer.append(self.movemap[move]["dircode"])

    def handle_output(self):
        while self.output_buffer:
            status = self.output_buffer.pop(0)
            newloc = (self.droid_loc[0] + self.movemap[self.last_move]["dirmove"][0],
                      self.droid_loc[1] + self.movemap[self.last_move]["dirmove"][1])
            if status == 0:
                self.map[newloc] = 0
            elif status == 1:
                self.map[newloc] = 1
                self.droid_loc = newloc
            elif status == 2:
                self.map[newloc] = 2
                self.droid_loc = newloc
                if not self.o2at:
                    self.o2at = newloc
                    print(f"OXYGEN FOUND AT LOCATION {newloc} on move {self.move_count}")
            else:
                raise RuntimeError(f"Unexpected status value encountered: {status}")
            return status

    def print_map(self):
        print('========')
        min_row, max_row, min_col, max_col = 0, 0, 0, 0
        for loc in self.map:
            min_row = min(loc[0], min_row)
            max_row = max(loc[0], max_row)
            min_col = min(loc[1], min_col)
            max_col = max(loc[1], max_col)
        for i in range(min_row, max_row+1):
            output_row = []
            for j in range(min_col, max_col+1):
                if (i, j) == self.droid_loc:
                    output_row.append('D')
                elif (i, j) == (0, 0):
                    output_row.append('X')
                else:
                    output_row.append(self.map_symbols[self.map.get((i,j), None)])
            print(''.join(output_row))
        print(f'Number of moves to explore maze: {self.move_count}')
    
    def possible_moves(self, loc):
        for move in self.movemap.values():
            tryloc = (loc[0] + move['dirmove'][0], loc[1] + move['dirmove'][1])
            if self.map.get(tryloc, 0):
                yield tryloc

    def minmoves_to_o2(self):
        shell_counts = 0
        move_shell = set([self.o2at])
        visited_locations = set([self.o2at])
        while move_shell:
            shell_counts += 1
            next_move_shell = set()
            for loc in move_shell:
                for tryloc in self.possible_moves(loc):
                    if tryloc not in visited_locations:
                        if tryloc == (0,0):
                            print(f'Path to (0,0) found in {shell_counts} moves')
                            return
                        next_move_shell.add(tryloc)
                        visited_locations.add(tryloc)
            move_shell = next_move_shell
        raise RuntimeError('Never found the origin.')

    

if __name__ == "__main__":
    
    droid = Droidmap(data='a15_input.txt')
    # droid.run()
    droid.rightside_explore()
    droid.print_map()
    droid.minmoves_to_o2()

