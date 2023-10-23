#!/usr/bin/python3

import AoC

class CPU:
    def __init__(self):
        self.X = 1
        self.instruction = None
        self.instruction_args = None
        self.instruction_end = 0
        self.cycle_count = 0
    def exec(self,instruction,args=None):
        if self.instruction is not None:
            raise Exception("Cannot execute an instruction while one is currently executing")
        if instruction == "noop":
            if args:
                raise Exception("noop does not take any arguments")
            self.instruction = instruction
            self.instruction_args = None
            self.instruction_end = self.cycle_count + 1
        elif instruction == "addx":
            if args is None or len(args) != 1:
                raise Exception("addx requires exactly 1 integer argument")
            self.instruction = instruction
            self.instruction_args = int(args[0])
            self.instruction_end = self.cycle_count + 2
    def start_cycle(self):
        if self.instruction:
            self.cycle_count += 1
    def end_cycle(self):
        if self.cycle_count >= self.instruction_end:
            if self.instruction == "addx":
                self.X += self.instruction_args
            self.instruction = None
    def ready(self):
        return self.instruction == None
        
def part1(inp):
    i = 0
    signal_strengths = []
    next_check = 20
    instructions = inp.splitlines()
    cpu = CPU()
    while i < len(instructions):
        inst = instructions[i].split()
        cpu.exec(inst[0],inst[1:])
        while not cpu.ready():
            cpu.start_cycle()
            if cpu.cycle_count == next_check:
                AoC.tprint("Cycle: {}, X: {}, SS: {}".format(cpu.cycle_count,cpu.X,cpu.cycle_count * cpu.X))
                signal_strengths.append(cpu.cycle_count * cpu.X)
                next_check += 40
            cpu.end_cycle()
        i += 1
    AoC.tprint(signal_strengths)
    print("Sum of signal strengths: {}".format(sum(signal_strengths)))

def part2(inp):
    i = 0
    scanlines = []
    sl_x = 0
    sl_y = 0
    instructions = inp.splitlines()
    cpu = CPU()
    while i < len(instructions):
        inst = instructions[i].split()
        cpu.exec(inst[0],inst[1:])
        while not cpu.ready():
            cpu.start_cycle()
            lit = "."
            if cpu.X >= sl_x - 1 and cpu.X <= sl_x + 1:
                lit = "#"
            AoC.tprint("Cycle: {}, X: {}, lit: {}".format(cpu.cycle_count,cpu.X,lit))
            if sl_x == 0:
                scanlines.append([])
            scanlines[sl_y].append(lit)
            cpu.end_cycle()
            sl_x += 1
            if sl_x >= 40:
                sl_x = 0
                sl_y += 1
        i += 1
    for line in scanlines:
        print("".join(line))

def main():
    AoC.set_day("10")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("--- Part 1 ---")
    part1(inp)
    print("--- Part 2 ---")
    part2(inp)

if __name__ == "__main__":
    main()
