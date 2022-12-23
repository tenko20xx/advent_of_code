#!/usr/bin/python3

import AoC

def parse_elves(txt):
    elves = set()
    bb = (None, None, None, None)
    lines = txt.splitlines()
    y = len(lines)//2
    for line in lines:
        x = 0
        for c in line:
            if c == '#':
                elves.add((x,y))
                if bb[0] is None or x < bb[0]:
                    bb = (x, bb[1], bb[2], bb[3])
                if bb[1] is None or y < bb[1]:
                    bb = (bb[0], y, bb[2], bb[3])
                if bb[2] is None or x > bb[2]:
                    bb = (bb[0], bb[1], x, bb[3])
                if bb[3] is None or y > bb[3]:
                    bb = (bb[0], bb[1], bb[2], y)
            elif c != '.':
                raise Exception(f"Unknown object in input: {c}")
            x += 1
        y -= 1
    return elves

def check_clear(e,p):
    clear = []
    for y in [1,0,-1]:
        for x in [-1,0,1]:
            if x == 0 and y == 0:
                continue
            clear.append((p[0] + x, p[1] + y) not in e)
    return clear

def propose_moves(e,m):
    elf_to_move = {}
    move_to_elf = {}
    for p in e:
        cl = check_clear(e,p)
        #print(f"elf {p} -> clear: {cl}")
        if all(cl):
            continue
        this_pm = None
        for d in m:
            if d == 'N':
                if cl[0] and cl[1] and cl[2]:
                    #print("move N")
                    this_pm = (p[0],p[1]+1)
                else:
                    #print("can't move N")
                    pass
            elif d == 'E':
                if cl[2] and cl[4] and cl[7]:
                    #print("move E")
                    this_pm = (p[0]+1,p[1])
                else:
                    #print("can't move E")
                    pass
            elif d == 'S':
                if cl[5] and cl[6] and cl[7]:
                    #print("move S")
                    this_pm = (p[0],p[1]-1)
                else:
                    #print("can't move S")
                    pass
            elif d == 'W':
                if cl[0] and cl[3] and cl[5]:
                    #print("move W")
                    this_pm = (p[0]-1,p[1])
                else:
                    #print("can't move W")
                    pass
            else:
                raise Exception(f"Invalid direction: {d}")
            if this_pm is not None:
                break
        #print(this_pm)
        if this_pm is not None:
            if this_pm in move_to_elf:
                elf_to_move.pop(move_to_elf[this_pm])
            else:
                elf_to_move[p] = this_pm
                move_to_elf[this_pm] = p
    return elf_to_move

def get_bounds(e):
    b = (None, None, None, None)
    for x, y in e:
        if b[0] is None or x < b[0]:
            b = (x, b[1], b[2], b[3])
        if b[1] is None or y < b[1]:
            b = (b[0], y, b[2], b[3])
        if b[2] is None or x > b[2]:
            b = (b[0], b[1], x, b[3])
        if b[3] is None or y > b[3]:
            b = (b[0], b[1], b[2], y)
    return b

def print_elves(e,bounds=None):
    s = ""
    if bounds is None:
        bounds = get_bounds(e)
    for y in range(bounds[3],bounds[1]-1,-1):
        for x in range(bounds[0],bounds[2]+1):
            if (x,y) in e:
                s += "#"
            else:
                s += "."
        s += "\n"
    print(s)

def rotate_moves(moves):
    m1 = moves.pop(0)
    moves.append(m1)

def count_empty(e,bounds=None):
    count = 0
    if bounds is None:
        bounds = get_bounds(e)
    for y in range(bounds[3],bounds[1]-1,-1):
        for x in range(bounds[0],bounds[2]+1):
            if (x,y) not in e:
                count += 1
    return count

def part1(inp):
    elves = parse_elves(inp)
    moves = ['N','S','W','E']
    bounds = (-3,-6,10,5)
    if AoC.TEST:
        print_elves(elves)
    for i in range(10):
        AoC.tprint(f"== Round {i+1} ==")
        pm = propose_moves(elves,moves)
        if not pm:
            AoC.tprint("No more proposed moves to make")
            break
        for e in pm:
            elves.remove(e)
        for m in pm.values():
            elves.add(m)
        if AoC.TEST:
            print_elves(elves,bounds)
        rotate_moves(moves)
    nempty = count_empty(elves)
    print(f"The number of empty ground tiles is {nempty}")

def part2(inp):
    elves = parse_elves(inp)
    moves = ['N','S','W','E']
    bounds = (-3,-6,10,5)
    if AoC.TEST:
        print_elves(elves)
    rounds = 1
    while True:
        AoC.tprint(f"== Round {rounds} ==")
        pm = propose_moves(elves,moves)
        if not pm:
            AoC.tprint("No more proposed moves to make")
            break
        for e in pm:
            elves.remove(e)
        for m in pm.values():
            elves.add(m)
        if AoC.TEST:
            print_elves(elves,bounds)
        rotate_moves(moves)
        rounds += 1
    print(f"The firsrt round where no elf moves is round {rounds}")

def main():
    AoC.set_day("23")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("== Part 1 ==")
    part1(inp)
    print("== Part 2 ==")
    part2(inp)

if __name__ == "__main__":
    main()
