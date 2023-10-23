#!/usr/bin/python3

import sys

TEST = False
DAY = "6"

def tprint(msg):
    if TEST:
        print(msg)

def uniq(seq):
    s = set()
    for i in seq:
        if i in s:
            return False
        s.add(i)
    return True

def findMarker(data,l):
    rb = []
    for i in range(l):
        rb.append(data[i])
    rb_i = 0
    i += 1
    while not uniq(rb) and i < len(data):
        rb[rb_i] = data[i]
        i += 1
        rb_i = (rb_i + 1) % l
    if uniq(rb):
        return i
    return -1

def part1(inp):
    for line in inp.splitlines():
        line = line.strip()
        if len(line) < 4:
            continue
        mi = findMarker(line,4)
        tprint(line)
        tprint(line[mi-4:mi])
        print("Marker index: {}".format(mi))

def part2(inp):
    for line in inp.splitlines():
        line = line.strip()
        if len(line) < 14:
            continue
        mi = findMarker(line,14)
        tprint(line)
        tprint(line[mi-4:mi])
        print("Marker index: {}".format(mi))

def main():
    global TEST
    if len(sys.argv) > 1 and (sys.argv[1] == "-t" or sys.argv[1] == "--test"):
        TEST = True
    filename = "inputs/day{}.{}input".format(DAY,"test." if TEST else "")
    inp = None
    with open(filename,'r') as fp:
        inp = fp.read()
    print("--- Part 1 ---")
    part1(inp)
    print("--- Part 2 ---")
    part2(inp)

if __name__ == "__main__":
    main()
