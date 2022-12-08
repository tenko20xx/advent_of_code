#!/usr/bin/python3

import sys

TEST = False
DAY = "5"

def tprint(msg):
    if TEST:
        print(msg)

def parse_crates(lines):
    stacks = {}
    stack_nums = []
    for stack_num in lines[-1].split():
        #print(stack_num)
        stacks[stack_num] = []
        stack_nums.append(stack_num)
    for line in lines[-2::-1]:
        i = 0
        for sn in stack_nums:
            crate = line[i:i+3]
            if crate[0] == "[" and crate[2] == "]":
                stacks[sn].append(crate[1])
            i += 4
    return stacks

def parse_moves(lines):
    moves = []
    for line in lines:
        parts = line.split()
        moves.append((int(parts[1]),parts[3],parts[5]))
    return moves

def parse_crates_and_moves(lines):
    crate_lines = []
    move_lines = []
    getting_crates = True
    for line in lines.splitlines():
        if line.strip() == "":
            getting_crates = False
            continue
        if getting_crates:
            crate_lines.append(line)
        else:
            move_lines.append(line)
    crates = parse_crates(crate_lines)
    moves = parse_moves(move_lines)
    return crates, moves

def repr_crates(crates):
    s = " ".join(" {} ".format(x) for x in sorted(crates.keys()))
    for i in range(max([len(v) for v in crates.values()])):
        these_crates = []
        for k in sorted(crates.keys()):
            if len(crates[k]) > i:
                these_crates.append("[" + crates[k][i] + "]")
            else:
                these_crates.append("   ")
        s = " ".join(these_crates) + "\n" + s
    return s


def part1(inp):
    crates, moves = parse_crates_and_moves(inp)
    #print(crates)
    #print(moves)
    for m in moves:
        for x in range(m[0]):
            tprint("{} -> {}".format(m[1],m[2]))
            crates[m[2]].append(crates[m[1]].pop())
    tprint(repr_crates(crates))
    tops = []
    for k in sorted(crates.keys()):
        tops.append(crates[k][-1])
    print("".join(tops))

def part2(inp):
    crates, moves = parse_crates_and_moves(inp)
    #print(crates)
    #print(moves)
    for m in moves:
        add_crates = []
        for x in range(m[0]):
            add_crates.append(crates[m[1]].pop())
        add_crates.reverse()
        for a in add_crates:
            crates[m[2]].append(a)
    tprint(repr_crates(crates))
    tops = []
    for k in sorted(crates.keys()):
        tops.append(crates[k][-1])
    print("".join(tops))

def main():
    global TEST
    filename = "inputs/day{}.input".format(DAY)
    if len(sys.argv) > 1 and (sys.argv[1] == "-t" or sys.argv[1] == "--test"):
        TEST = True
        filename = "inputs/day{}.test.input".format(DAY)
    inp = None
    with open(filename,'r') as fp:
        inp = fp.read()
    print("== Part 1 ==")
    part1(inp)
    print("== Part 2 ==")
    part2(inp)

if __name__ == "__main__":
    main()
