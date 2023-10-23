#!/usr/bin/python3

import AoC

def snafu_to_int(s):
    n = 0
    for i in range(len(s)):
        d = s[(len(s) - i) - 1]
        v = 0
        if d == "-":
            v = -1
        elif d == "=":
            v = -2
        else:
            v = int(d)
        n += v * 5 ** i
    return n

def list_add(d,i,v):
    while i >= len(d):
        d.append(0)
    d[i] += v
    if d[i] > 2:
        d[i] -= 5
        list_add(d,i+1,1)
def list_val(d):
    i = 0
    val = 0
    for n in d:
        val += n * (5**i)
        i += 1
    return val

def int_to_snafu(n):
    digits = [0]
    di = 0
    base = 1
    while n / (base * 5) > 1:
        base *= 5
        digits.append(0)
        di += 1
    while n - list_val(digits) != 0:
        #print(base,digits)
        d = (n - list_val(digits)) // base
        digits[di] = d
        if d > 2:
            digits[di] -= 5
            list_add(digits,di+1,1)
        base = base // 5
        di -= 1
    s = ""
    for v in digits:
        if v == -2:
            s = "=" + s
        elif v == -1:
            s = "-" + s
        else:
            s = str(v) + s
    return s


def part1(inp):
    print(f" {'SANFU': >20} {'Decimal': >20}")
    total = 0
    for line in inp.splitlines():
        val = snafu_to_int(line)
        print(f" {line: >20} {val: >20}")
        total += val
    snafu = int_to_snafu(total)
    print(f" {snafu: >20} {total: >20}")

def part2(inp):
    pass

def main():
    AoC.set_day("25")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("--- Part 1 ---")
    part1(inp)
    print("--- Part 2 ---")
    part2(inp)

if __name__ == "__main__":
    main()
