from intputer import Intputer

class Cabinet:

    def __init__(self, filename):
        '''Create the arcade cabinet, and load up the file.'''
        self.input_buffer = list()
        self.output_buffer = list()
        self.intputer = Intputer(self.input_buffer, self.output_buffer)
        self.intputer.load_program(filename)
        self.tiles = dict()
    
    def run(self):
        '''Run the game'''
        while self.intputer.running:
            self.intputer.run(pause_for_input=True)
            while len(self.output_buffer) >= 3:
                self.process_tilebuffer()

    def process_tilebuffer(self):
        '''Pull the next 3 ints out of the output buffer and update the tiles.'''
        if len(self.output_buffer) < 3:
            raise RuntimeError('Not enough values in the buffer to process a tile.')
        col, row, tile = self.output_buffer[:3]
        self.output_buffer = self.output_buffer[3:]
        self.tiles[(row, col)] = tile

if __name__ == "__main__":
    cab = Cabinet('a13_input.txt')
    cab.run()
    number_of_blocks = len([x for x in cab.tiles if cab.tiles[x]==2])
    print(f'Number of blocks: {number_of_blocks}')


