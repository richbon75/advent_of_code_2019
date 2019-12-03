import sys

class Intputer(object):
    '''This is a model of a computer that can run Intcode programs'''

    def __init__(self):
        '''Set up the Intputer'''
        self.memory = list()
        self.program_backup = list()
        self.pc = 0
        self.counter = 0
        self.running = False
        self.instruction = {
            1: self.op1,
            2: self.op2,
            99: self.op99
        }
    
    def load_program(self, filename='a02_input.txt'):
        '''Load a program into the memory of the Intputer'''
        self.program_backup = list()
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                self.program_backup.extend([int(x) for x in line.split(',')])
        self.memory = self.program_backup[:]
    
    def reset(self):
        '''Reset the Intputer.'''
        self.memory = self.program_backup[:]
        self.pc = 0
        self.counter = 0
        self.running = False
    
    def readLoc(self, loc):
        '''Directly read the value at memory location loc'''
        return self.memory[loc]
    
    def readRef(self, loc):
        '''Return the value stored at memory location referenced by loc'''
        location = self.memory[loc]
        return self.memory[location]
    
    def writeRef(self, loc, value):
        '''Write a value to the memory location referenced by loc'''
        location = self.memory[loc]
        self.memory[location] = value
    
    def jumpTo(self, loc):
        '''Move pc to new location'''
        self.pc = loc
    
    def run(self):
        '''Run the Intputer.'''
        self.running = True
        while self.running:
            self.instruction[self.readLoc(self.pc)]()
            self.counter += 1
    
    def op1(self):
        '''Perform op1 - adding'''
        pc = self.pc
        operand1 = self.readRef(pc+1)
        operand2 = self.readRef(pc+2)
        result = operand1 + operand2
        self.writeRef(pc+3, result)
        self.pc += 4
    
    def op2(self):
        '''Perform op2 - multiplying'''
        pc = self.pc
        operand1 = self.readRef(pc+1)
        operand2 = self.readRef(pc+2)
        result = operand1 * operand2
        self.writeRef(pc+3, result)
        self.pc += 4
    
    def op99(self):
        '''Perform op99 - Halt'''
        self.running = False
    
    def set1202(self):
        '''Restore error state'''
        self.memory[1] = 12
        self.memory[2] = 2
    
    def setNounVerb(self, noun, verb):
        '''Set the noun and the verb values'''
        self.memory[1] = noun
        self.memory[2] = verb

if __name__ == "__main__":
    intputer = Intputer()
    intputer.load_program()
    success = False
    for noun in range(0,100):
        for verb in range(0,100):
            intputer.reset()
            intputer.setNounVerb(noun, verb)
            intputer.run()
            if intputer.memory[0] == 19690720:
                print(f'Answer: {100 * noun + verb}')
                success = True
                break
        if success:
            break


