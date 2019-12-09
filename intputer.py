# Notes: Could a deque be faster than lists for the buffers?  Maybe,
# but the buffers are going to be very short so it probably doesn't matter.

class Intputer(object):
    '''This is a model of a computer that can run Intcode programs.
    This new modified version has an input buffer and an output buffer.
    '''

    def __init__(self, input_buffer=None, output_buffer=None, name="Intputer"):
        '''Set up the Intputer
        input_buffer - You can queue up some values for input at creation time if you want.
          Note that if you pass this as a list, it is held BY REFERENCE to the original list.
        output_buffer - again, lists will be held BY REFERENCE
        name - You can name this instance of the Intputer if it helps.
        '''
        if input_buffer is None:
            input_buffer = list()
        else:
            self.input_buffer = input_buffer
        if output_buffer is None:
            output_buffer = list()
        else:
            self.output_buffer = output_buffer
        self.name = name
        self.memory = list()
        self.backup = list()
        self.pc = 0
        self.counter = 0
        self.running = False
        self.param_mode = 0
        self.instruction = {
            1: self.op1,
            2: self.op2,
            3: self.op3,
            4: self.op4,
            5: self.op5,
            6: self.op6,
            7: self.op7,
            8: self.op8,
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

    def load_program(self, data):
        '''Load a program into the memory of the Intputer'''
        self.reset()
        self.memory = list()
        if isinstance(data, list):
            self.memory.extend(data[:])
        elif isinstance(data, str):
            with open(data, 'r') as f:
                for line in f:
                    line = line.strip()
                    self.memory.extend([int(x) for x in line.split(',')])
        else:
            raise ValueError('Unknown data - expected a list or a filename')
        self.backup = list(self.memory[:])
    
    def reset(self):
        '''Reset the Intputer.  Resets program memory to original loaded program.'''
        self.memory = list(self.backup[:])
        self.pc = 0
        self.counter = 0
        self.running = True
    
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
            # Execute one instruction
            self.op()
    
    def op(self):
        '''Execute a single instruction.'''
        if self.running:
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
        if self.input_buffer:
            result = self.input_buffer.pop(0)
            self.writeRef(pc+1, result)
        else:
            self.pc -= 2 # force this command to re-run until there is input to process
        # result = int(input("Op3 requests an integer input: "))
        self.pc += 2
    
    def op4(self):
        '''outputs the value of its only parameter.'''
        pc = self.pc
        operand1 = self.readRef(pc+1, self.pm(1))
        # print(f'Op4 output: {operand1}')
        self.output_buffer.append(operand1)
        self.pc += 2
    
    def op5(self):
        '''jump-if-true if first param is non-zero, jump to location in second param'''
        pc = self.pc
        operand1 = self.readRef(pc+1, self.pm(1))
        if operand1:
            self.pc = self.readRef(pc+2, self.pm(2))
        else:
            self.pc += 3
    
    def op6(self):
        '''jump-if-false if first param is zero, jump to location in second param'''
        pc = self.pc
        operand1 = self.readRef(pc+1, self.pm(1))
        if not operand1:
            self.pc = self.readRef(pc+2, self.pm(2))
        else:
            self.pc += 3
    
    def op7(self):
        '''less-than if param1 < param2 then write 1 to param3 else write 0'''
        pc = self.pc
        operand1 = self.readRef(pc+1, self.pm(1))
        operand2 = self.readRef(pc+2, self.pm(2))
        self.writeRef(pc+3, int(operand1 < operand2))
        self.pc += 4

    def op8(self):
        '''equals if param1 == param2 then write 1 to param3 else write 0'''
        pc = self.pc
        operand1 = self.readRef(pc+1, self.pm(1))
        operand2 = self.readRef(pc+2, self.pm(2))
        self.writeRef(pc+3, int(operand1 == operand2))
        self.pc += 4
    
    def op99(self):
        '''Perform op99 - Halt'''
        self.running = False
