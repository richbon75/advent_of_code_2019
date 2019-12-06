class Intputer(object):
    '''This is a model of a computer that can run Intcode programs'''

    def __init__(self):
        '''Set up the Intputer'''
        self.memory = list()
        self.pc = 0
        self.counter = 0
        self.running = False
        self.param_mode = 0
        self.instruction = {
            1: self.op1,
            2: self.op2,
            3: self.op3,
            4: self.op4,
            99: self.op99
        }
    
    def pm(self, p):
        '''Return the parameter mode for parameter p'''
        if p == 1:
            return self.param_mode % 10
        if p == 2:
            return self.param_mode // 10 % 10
        if p == 3:
            return self.param_mode // 100 % 10
        raise ValueError(f"Unknown parameter mode position: {p}")

    def load_program(self, filename):
        '''Load a program into the memory of the Intputer'''
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                self.memory.extend([int(x) for x in line.split(',')])
    
    def reset(self):
        '''Reset the Intputer.'''
        self.memory = list()
        self.pc = 0
        self.counter = 0
    
    def readDirect(self, loc):
        '''Directly read the value at memory location loc'''
        return self.memory[loc]
    
    def readRef(self, loc, pm):
        '''Return the value stored at memory location referenced by loc'''
        if pm == 0:
            location = self.memory[loc]
            return self.memory[location]
        if pm == 1:
            return self.memory[loc]
        raise ValueError(f"Unknown parameter mode: {pm}")
    
    def writeRef(self, loc, value):
        '''Write a value to the memory location referenced by loc'''
        # Parameters that an instruction writes to will never be in immediate mode
        location = self.memory[loc]
        self.memory[location] = value
        return
    
    def jumpTo(self, loc):
        '''Move pc to new location'''
        self.pc = loc
    
    def run(self):
        '''Run the Intputer.'''
        self.running = True
        while self.running:
            # Get the raw instruction
            op = self.readDirect(self.pc)
            # Peel out the param modes
            self.param_mode = op // 100
            # Run the base instruction
            self.instruction[op % 100]()
            self.counter += 1
    
    def op1(self):
        '''adding'''
        pc = self.pc
        operand1 = self.readRef(pc+1, self.pm(1))
        operand2 = self.readRef(pc+2, self.pm(2))
        result = operand1 + operand2
        self.writeRef(pc+3, result)
        self.pc += 4
    
    def op2(self):
        '''multiplying'''
        pc = self.pc
        operand1 = self.readRef(pc+1, self.pm(1))
        operand2 = self.readRef(pc+2, self.pm(2))
        result = operand1 * operand2
        self.writeRef(pc+3, result)
        self.pc += 4
    
    def op3(self):
        '''takes a single integer as input and saves it
        to the location given by that same integer.'''
        pc = self.pc
        result = int(input("Op3 requests an integer input: "))
        self.writeRef(pc+1, result)
        self.pc += 2
    
    def op4(self):
        '''outputs the value of its only parameter.'''
        pc = self.pc
        operand1 = self.readRef(pc+1, self.pm(1))
        print(f'Op4 output: {operand1}')
        self.pc += 2
    
    def op99(self):
        '''Perform op99 - Halt'''
        self.running = False
    
    def set1202(self):
        '''Restore error state'''
        self.memory[1] = 12
        self.memory[2] = 2


intputer = Intputer()
intputer.load_program('a05_input.txt')
print('Reminder: For the first part of this program, when you are prompted for a value, enter 1')
intputer.run()



