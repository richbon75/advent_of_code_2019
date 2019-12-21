from intputer import Intputer

class Cabinet:

    tilemap = {
        0: ' ',
        1: '#',
        2: '@',
        3: '=',
        4: 'o'
    }

    def __init__(self, filename):
        '''Create the arcade cabinet, and load up the file.'''
        self.input_buffer = list()
        self.output_buffer = list()
        self.intputer = Intputer(self.input_buffer, self.output_buffer)
        self.intputer.load_program(filename)
        self.tiles = dict()
        self.score = 0
    
    def coindrop(self):
        self.intputer.memory[0] = 2
    
    def run(self):
        '''Run the game'''
        while self.intputer.running:
            self.intputer.run(pause_for_input=True)
            while len(self.output_buffer) >= 3:
                self.process_tilebuffer()
            self.make_move()
            # self.print_screen()
    
    def make_move(self):
        '''Figure out what move we should make, and make it.'''
        # Compare the columns of the ball and paddle
        ball_col = [pos for pos, tile in self.tiles.items() if tile==4][0][1]
        paddle_col = [pos for pos, tile in self.tiles.items() if tile==3][0][1]
        move = 0
        if ball_col < paddle_col:
            move = -1
        elif ball_col > paddle_col:
            move = 1
        self.input_buffer.append(move)

    def process_tilebuffer(self):
        '''Pull the next 3 ints out of the output buffer and update the tiles.'''
        if len(self.output_buffer) < 3:
            raise RuntimeError('Not enough values in the buffer to process a tile.')
        col = self.output_buffer.pop(0)
        row = self.output_buffer.pop(0)
        tile = self.output_buffer.pop(0)
        if col == -1 and row == 0:
            self.score = tile
        else:
            self.tiles[(row, col)] = tile
    
    def print_screen(self):
        '''Print out the screen memory'''
        print(f'Score: {self.score}')
        min_row = 0
        max_row = 0
        min_col = 0
        max_col = 0
        for loc in self.tiles:
            min_row = min(min_row, loc[0])
            max_row = max(max_row, loc[0])
            min_col = min(min_col, loc[1])
            max_col = max(max_col, loc[1])
        for row in range(min_row, max_row+1):
            output_row = []
            for col in range(min_col, max_col+1):
                tile = self.tiles.get((row, col), 0)
                output_row.append(self.tilemap[tile])
            print(''.join(output_row))


if __name__ == "__main__":
    cab = Cabinet('a13_input.txt')
    cab.coindrop()
    cab.run()
    cab.print_screen()
    print(f'Final Score: {cab.score}')


