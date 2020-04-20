"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    pass

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256    # Total RAM 
        self.pc = 0             # Program Counter: address of the currently executing instruction
        self.ir = [0] * 8       # Instruction Register: copy of the currently executing instruction
        self.mar = [0] * 8      # Memory Address Registry: holds the memory address we're reading or writing
        self.mdr = [0] * 8      # Memory Data Register: holds the value to write or read
        self.fl = [0] * 8       # Flags: hold current "flag" status
      

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")


    def ram_read(self, address):
        # return value at given address
        return self.ram[address] 


    def ram_write(self, address, value):
        self.ram[address] = value


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

    def run(self):
        """Run the CPU."""
        # I assume this will get more robust... should load a particular thing...
        self.load()

        # Make a copy of current instruction (Instruction Registry)
        ir = self.ram_read(self.pc)

        running = True

        While running:
            # In case "instruction" need up to 3 bytes...
            operand_a = ram_read(self.pc + 1)
            operand_b = ram_read(self.pc + 2)

            #



