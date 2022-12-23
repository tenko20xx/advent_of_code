#!/usr/bin/python3

import AoC

def read_monkeys(txt):
    monkeys = {}
    for line in txt.splitlines():
        line = line.strip()
        parts = line.split(":")
        monkey = parts[0]
        val = parts[1].strip()
        if val.isnumeric():
            val = int(val)
        else:
            val = tuple(val.split())
        monkeys[monkey] = val
    return monkeys

OPERATION = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y
}

OPPOSITE_OPERATION = {
        "+": "-",
        "-": "+",
        "*": "/",
        "/": "*"
}

def resolve_values(m,k):
    if type(m[k]) is not tuple:
        return m[k]
    v1, op, v2 = m[k]
    if type(v1) is str:
        if v1 in m:
            v1 = resolve_values(m,v1)
        else:
            raise Exception(f"No monkey named '{v1}' found")
    if type(v2) is str:
        if v2 in m:
            v2 = resolve_values(m,v2)
        else:
            raise Exception(f"No monkey named '{v1}' found")
    if op not in OPERATION:
        raise Exception(f"Unknown operator: {op}")
    r = OPERATION[op](v1,v2)
    if r == round(r):
        r = int(r)
    m[k] = r
    return r

def expand_terms(m,k):
    if type(m[k]) is not tuple:
        return m[k]
    v1, op, v2 = m[k]
    if type(v1) is str:
        if v1 in m:
            v1 = expand_terms(m,v1)
        else:
            raise Exception(f"No monkey named '{v1}' found")
    if type(v2) is str:
        if v2 in m:
            v2 = expand_terms(m,v2)
        else:
            raise Exception(f"No monkey named '{v1}' found")
    if type(v1) in (int,float) and type(v2) in (int,float):
        if op not in OPERATION:
            raise Exception(f"Unknown operator: {op}")
        r = OPERATION[op](v1,v2)
        if r == round(r):
            r = int(r)
        m[k] = r
        return r
    return (v1,op,v2)
    
def solve(terms):
    #print(f"solve({terms})")
    if type(terms) is not tuple:
        return terms
    v1, op, v2 = terms
    if op != "=":
        return terms
    if v1 == "x":
        return v2
    elif v2 == "x":
        return v1
    if type(v1) is tuple and type(v2) is tuple:
        return terms
    if type(v1) is tuple:
        xterm = v1
        vterm = v2
    else:
        xterm = v2
        vterm = v1
    xv1, xop, xv2 = xterm
    if type(xv1) is tuple and type(xv2) is tuple:
        return terms
    if type(xv2) in (int, float):
        opop = OPPOSITE_OPERATION[xop]
        vterm = OPERATION[opop](vterm,xv2)
        if vterm == round(vterm):
            vterm = int(vterm)
        return solve((xv1,op,vterm))
    elif type(xv1) in (int, float):
        if xop in ("-","/"):
            vterm = OPERATION[xop](xv1,vterm)
            if vterm == round(vterm):
                vterm = int(vterm)
            return solve((vterm,op,xv2))
        opop = OPPOSITE_OPERATION[xop]
        vterm = OPERATION[opop](vterm,xv1)
        if vterm == round(vterm):
            vterm = int(vterm)
        return solve((xv2,op,vterm))
    return terms

def part1(inp):
    monkeys = read_monkeys(inp)
    resolve_values(monkeys,"root")
    print(f"root: {monkeys['root']}")

def part2(inp):
    monkeys = read_monkeys(inp)
    root = monkeys["root"]
    root = (root[0],"=",root[2])
    monkeys["root"] = root
    monkeys["humn"] = "x"
    root_terms = expand_terms(monkeys,"root")
    #print(root_terms)
    x = solve(root_terms)
    print(f"humn: {x}")

def main():
    AoC.set_day("21")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("== Part 1 ==")
    part1(inp)
    print("== Part 2 ==")
    part2(inp)

if __name__ == "__main__":
    main()
