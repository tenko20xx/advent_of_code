#!/usr/bin/python3

import AoC
from functools import cmp_to_key

def compare_lists(l1,l2):
    i = 0
    for i in range(min(len(l1),len(l2))):
        v1, v2 = l1[i], l2[i]
        if type(v1) is int and type(v2) is int:
            if v1 > v2:
                return -1
            elif v1 < v2:
                return 1
            continue
        else:
            if type(v1) is int:
                v1 = [v1]
            if type(v2) is int:
                v2 = [v2]
            cmpr = compare_lists(v1,v2)
            if cmpr != 0:
                return cmpr
    if len(l1) > len(l2):
        return -1
    elif len(l1) < len(l2):
        return 1
    return 0

def parse_list(line):
    l = eval(line)
    return l

def part1(inp):
    out_of_order = []
    pair = []
    pair_ind = 1
    for line in inp.splitlines():
        if line.strip() == "":
            if len(pair) == 0:
                continue
            else:
                raise Exception("Parsing Error: Got blank line when expecting another list for a pair")
        l = parse_list(line)
        pair.append(l)
        if len(pair) == 2:
            cmpr = compare_lists(pair[0],pair[1])
            if cmpr == 1:
                out_of_order.append(pair_ind)
            pair = []
            pair_ind += 1
    print("Sum of indices: {}".format(sum(out_of_order)))


def part2(inp):
    signals = [[[2]],[[6]]]
    for line in inp.splitlines():
        if line.strip() == "":
            continue
        l = parse_list(line)
        signals.append(l)
    signals.sort(key=cmp_to_key(compare_lists),reverse=True)
    if AoC.TEST:
        i = 1
        for s in signals:
            print("{}: {}".format(i,s))
            i += 1
    i1 = signals.index([[2]]) + 1
    i2 = signals.index([[6]]) + 1
    print("Decoder key is: {}".format(i1*i2))

def main():
    AoC.set_day("13")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("== Part 1 ==")
    part1(inp)
    print("== Part 2 ==")
    part2(inp)

if __name__ == "__main__":
    main()
