from intputer import Intputer
from itertools import permutations

class Amplifier:

    def __init__(self, stages, program, loopback=False):
        '''The buffers are shared - the output buffer of one stage is the 
        input buffer of the next stage.'''
        self.buffers = [list()]
        self.intputers = []
        self.sequence = []
        self.loopback = loopback

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
        lastloopvalue = None
        while any(i.running for i in self.intputers):
            for intputer in self.intputers:
                intputer.op()
            if self.loopback:
                if self.buffers[-1]:
                    lastloopvalue = self.buffers[-1].pop(0)
                    self.buffers[0].append(lastloopvalue)
        if self.loopback:
            return [lastloopvalue,]
        else:
            return self.buffers[-1]

if __name__ == "__main__":
    stages = 5
    # program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    # program = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    program = 'a07_input.txt'
    initial_input = 0
    max_output = 0
    max_settings = None    
    amp = Amplifier(stages=stages, program=program, loopback=True)

    for sequence in permutations([5,6,7,8,9]):
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
