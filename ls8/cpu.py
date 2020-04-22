"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # Total RAM 
        self.pc = 0
        self.registry = [0] * 8

        # Program Counter: address of the currently executing instruction
        # self.ir = [0]  # self.ram[pc]     # Instruction Register: copy of the currently executing instruction
        # self.mar = [0] * 8      # Memory Address Registry: holds the memory address we're reading or writing
        # self.mdr = [0] * 8      # Memory Data Register: holds the value to write or read
        # self.fl = [0] * 8       # Flags: hold current "flag" status
      

    def load(self): # , program_filename):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
	        for line in f:
		        line = line.split('#')
		        line = line[0].strip()

		        if line == '':
			        continue

		        self.ram[address] = int(line, 2)

		        address += 1
        
        # hardcoded program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")


    def ram_read(self, address):
        # return value at given address
        return self.ram[int(address)] 


    def ram_write(self, address, value):
        self.ram[address] = value

    # def HLT():
    #     # HLT = 0b00000001
    #     # if self.ir == 0b00000001:
    #     #     return running = False
    #     pass

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self): #, program_filename):
        """Run the CPU."""
        # I assume this will get more robust... should load a particular thing...
        # self.load(sys.argv[1]) #program_filename)
        
        self.pc = 0

        # Stack Pointer (SP) value lives at registry[7]
        SP = 7
        self.registry[SP] = 0xF4 # starts at the top less extra room for other stuff

        # For now, put the Opcode values direction in the run function...
        # Maybe eventually store them in a dictionary(?) / hashtable?
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        running = True

        while running:
            # Make a copy of current instruction (Instruction Registry)
            ir = self.ram[self.pc]

            # In case instructions needs up to 3 bytes...
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # Simple for now, just three Opcode options...
            if ir == LDI:
                self.registry[operand_a] = operand_b
                self.pc += 3

            elif ir == PRN:
                print(self.registry[operand_a])
                self.pc += 2

            elif ir == MUL:
                self.registry[operand_a] *= self.registry[operand_b]
                self.pc += 3

            elif ir == PUSH:
                # decriment the stack pointer
                self.registry[SP] -= 1

                # Copy value from registry (called at PC + 1) into stack/RAM/memory
                value = self.registry[operand_a] # value from PC+1 from program
                address = self.registry[SP]      # index of stack to push value to

                self.ram[address] = value        # Write/push value to stack in ram/memory

                # Move pointer up through program
                self.pc += 2

            elif ir == POP:
                # Copy value from stack/RAM/memory to registry
                address = self.registry[SP] # looking for the address SP is at

                value = self.ram[address] # get value at SP address

                self.registry[operand_a] = value # set registry from PC+1 to value from mem

                self.registry[SP] += 1 # Oh yeah... this. XD

                self.pc += 2 # etc...

            elif ir == HLT:
                running = False

            else:
                print('Error: unknown instructions')
                running = False


# print(sys.argv[1])
# thing = CPU()

# thing.run(sys.argv[1])