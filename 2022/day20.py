#!/usr/bin/python3

import AoC

def parse_list(txt):
    l = []
    for n in txt.splitlines():
        v = n.strip()
        if v == "":
            continue
        l.append(int(v))
    return l

def part1(inp):
    l = parse_list(inp)
    N = len(l)
    s = [False] * len(l)
    i = 0
    AoC.tprint("Initial arrangement:")
    AoC.tprint(", ".join(str(n) for n in l))
    AoC.tprint("")
    for j in range(N):
        v = l.pop(i)
        b = s.pop(i)
        p = i + v
        while p > (N-1):
            p -= (N-1)
        while p <= 0:
            p += (N-1)
        if v == 0:
            AoC.tprint("0 does not move")
        else:
            peek1 = l[p-1]
            peek2 = l[p if p < len(l) else 0]
            AoC.tprint(f"{v} moves between {peek1} and {peek2}")
        l.insert(p,v)
        s.insert(p,True)
        AoC.tprint(", ".join(str(n) for n in l))
        AoC.tprint("")
        while i < N and s[i]:
            i += 1
    zero_p = -1
    for i in range(N):
        if l[i] == 0:
            zero_p = i
            break
    a = (zero_p + 1000) % N
    b = (zero_p + 2000) % N
    c = (zero_p + 3000) % N
    print(f"The 1000th number after 0 is {l[a]}, the 2000th is {l[b]} and the 3000th is {l[c]}; adding these together produces {sum([l[a],l[b],l[c]])}.")
        

def part2(inp):
    pass

def main():
    AoC.set_day("20")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("== Part 1 ==")
    part1(inp)
    print("== Part 2 ==")
    part2(inp)

if __name__ == "__main__":
    main()
