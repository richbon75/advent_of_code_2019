from intputer import Intputer
from itertools import permutations

class Amplifier:

    def __init__(self, stages, program):
        self.buffers = [list()]
        self.intputers = []
        self.sequence = []

        # Create intputer array
        for i in range(0, stages):
            self.buffers.append(list())
            self.intputers.append(Intputer(input_buffer=self.buffers[-2], 
                                           output_buffer=self.buffers[-1], 
                                           name=str(chr(65+i))))
            self.intputers[-1].load_program(program)

    def reset(self):
        '''Reset amplifier for another run'''
        for buffer in self.buffers:
            buffer.clear()
        for intputer in self.intputers:
            intputer.reset()

    def program_sequence(self, sequence, initial_input=0):
        '''Program a sequence into the amplifiers'''
        self.sequence = sequence
        for i in range(len(self.sequence)):
            self.buffers[i].clear()
            self.buffers[i].append(self.sequence[i])
            if i == 0:
                self.buffers[i].append(initial_input)

    def run(self):
        # Run all intputers until they are all halted and return the output buffer
        while any(i.running for i in self.intputers):
            for intputer in self.intputers:
                intputer.op()
        return self.buffers[-1]

if __name__ == "__main__":
    stages = 5
    # program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    # program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    # program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    program = 'a07_input.txt'
    initial_input = 0
    max_output = 0
    max_settings = None    
    amp = Amplifier(stages=stages, program=program)

    for sequence in permutations([0,1,2,3,4]):
        print(sequence, end='')
        amp.reset()
        amp.program_sequence(sequence=sequence, initial_input=initial_input)
        output = amp.run()
        print(f' : {output[0]}')
        if output[0] > max_output:
            max_output = output[0]
            max_settings = sequence
        print(''.join([str(i) for i in sequence]) + ' : ' + str(output[0]))
    print('*'*25)
    print(f'Max thruster signal: {max_output}')
    print('From phase sequence: ' + ''.join([str(i) for i in max_settings]))
