#!/usr/bin/python3

import sys

TEST = False
DAY = 4

def tprint(msg):
    if TEST:
        print(msg)

def getSections(assign):
    return tuple(tuple(int(x) for x in y.split("-")) for y in assign.strip().split(","))

def contains(secA,secB):
    return secA[0] <= secB[0] and secA[1] >= secB[1]

def overlaps(secA,secB):
    return (
            (secA[0] >= secB[0] and secA[0] <= secB[1]) or
            (secA[1] >= secB[0] and secA[1] <= secB[1]) or
            (secB[0] >= secA[0] and secB[0] <= secA[1]) or
            (secB[1] >= secA[0] and secB[1] <= secA[1])
    )

def part1(inp):
    total = 0
    for line in inp.splitlines():
        s1, s2 = getSections(line)
        if contains(s1, s2) or contains(s2,s1):
            tprint("Contains: {}".format(line))
            total += 1
    print("Total fully contained: {}".format(total))

def part2(inp):
    total = 0
    for line in inp.splitlines():
        s1, s2 = getSections(line)
        if overlaps(s1, s2):
            tprint("Overlaps: {}".format(line))
            total += 1
    print("Total overlaps: {}".format(total))

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
