#!/usr/bin/python3

import AoC

def adjust_tail(h,t):
    if abs(h[0]-t[0]) <= 1 and abs(h[1] - t[1]) <= 1:
        return 
    if h[0] > t[0]:
        t[0] += 1
    elif h[0] < t[0]:
        t[0] -= 1
    if h[1] > t[1]:
        t[1] += 1
    elif h[1] < t[1]:
        t[1] -= 1

def draw_visited(tv,rang=None):
    if rang is None: 
        mx = min(p[0] for p in tv)
        Mx = max(p[0] for p in tv)
        my = min(p[1] for p in tv)
        My = max(p[1] for p in tv)
    else:
        mx, Mx, my, My = rang
    mat = []
    for y in range(my,My+1):
        row = []
        for x in range(mx,Mx+1):
            row.append(".")
        mat.append(row)
    for p in tv:
        if p[0] < mx or p[0] > Mx or p[1] < my or p[1] > My:
            continue
        r = (My - my) - (p[1] - my)
        c = p[0] - mx
        mat[r][c] = "#"
    mat[(My-my)-(-my)][-mx] = "s"
    for row in mat:
        print("".join(row))

def draw_rope(rope,rang=None):
    if rang is None: 
        mx = min(p[0] for p in ([[0,0]] + rope))
        Mx = max(p[0] for p in ([[0,0]] + rope))
        my = min(p[1] for p in ([[0,0]] + rope))
        My = max(p[1] for p in ([[0,0]] + rope))
    else:
        mx, Mx, my, My = rang
    mat = []
    for y in range(my,My+1):
        row = []
        for x in range(mx,Mx+1):
            row.append(".")
        mat.append(row)
    mat[(My-my)-(-my)][-mx] = "s"
    i = 0
    for p in rope:
        if p[0] < mx or p[0] > Mx or p[1] < my or p[1] > My:
            continue
        r = (My - my) - (p[1] - my)
        c = p[0] - mx
        sym = "H"
        if i > 0:
            if i == len(rope) -1:
                sym = "T"
            else:
                sym = str(i)
        mat[r][c] = sym
        i += 1
    for row in mat:
        print("".join(row))


def part1(inp,draw=False):
    head = [0,0]
    tail = [0,0]
    tail_visited = set([(0,0)])
    for move in inp.splitlines():
        move = move.strip()
        AoC.tprint(move)
        d, n = move.split()
        for i in range(int(n)):
            if d == "R":
                head[0] += 1
            elif d == "L":
                head[0] -= 1
            elif d == "U":
                head[1] += 1
            elif d == "D":
                head[1] -= 1
            else:
                raise Exception("Invalid move: {}".format(d))
            adjust_tail(head,tail)
            if draw:
                draw_rope([head,tail],(-11,14,-5,15))
                print("-"*20)
            #print("h:{}".format(head))
            #print("t:{}".format(tail))
            tail_visited.add(tuple(tail))
    if AoC.TEST:
        draw_visited(tail_visited,(-11,14,-5,15))
    print("Tail visited {} positions".format(len(tail_visited)))

def part2(inp,draw=False):
    rope = []
    for i in range(10):
        rope.append([0,0])
    tail_visited = set([(0,0)])
    for move in inp.splitlines():
        move = move.strip()
        AoC.tprint(move)
        d, n = move.split()
        for i in range(int(n)):
            if d == "R":
                rope[0][0] += 1
            elif d == "L":
                rope[0][0] -= 1
            elif d == "U":
                rope[0][1] += 1
            elif d == "D":
                rope[0][1] -= 1
            else:
                raise Exception("Invalid move: {}".format(d))
            for i in range(1,len(rope)):
                adjust_tail(rope[i-1],rope[i])
            if draw:
                draw_rope(rope,(-11,14,-5,15))
                print("-"*20)
            #print("h:{}".format(head))
            #print("t:{}".format(tail))
            tail_visited.add(tuple(rope[-1]))
    if AoC.TEST:
        draw_visited(tail_visited,(-11,14,-5,15))
    print("Tail visited {} positions".format(len(tail_visited)))

def main():
    AoC.set_day("9")
    parser = AoC.get_default_argparse()
    parser.add_argument("--draw-positions",action="store_true")
    args = AoC.parse_args(parser)

    inp = AoC.get_input()
    print("== Part 1 ==")
    part1(inp,args.draw_positions)
    print("== Part 2 ==")
    part2(inp,args.draw_positions)

if __name__ == "__main__":
    main()
