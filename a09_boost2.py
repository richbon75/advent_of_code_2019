from intputer import Intputer

program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
program = [1102,34915192,34915192,7,4,7,99,0]
program = [104,1125899906842624,99]
program = 'a09_input.txt'
input_buffer = [2]
output_buffer = []
intputer = Intputer(input_buffer=input_buffer, output_buffer=output_buffer)
# intputer = Intputer(output_buffer=output_buffer)
intputer.load_program(program)
intputer.run()
print(output_buffer)
