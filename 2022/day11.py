#!/usr/bin/python3

import AoC

VERBOSE = False

class PrimeFactorizor:
    def __init__(self):
        self.primes = [2,3]
        self.k = 1
        self.a = -1
    def next(self):
        while not self.check_prime(c := 6*self.k + self.a):
            if self.a == -1:
                self.a = 1
            else:
                self.a = -1
                self.k += 1
        self.primes.append(c)
        print(self.primes)
        return c
    def check_prime(self,n):
        for i in self.primes[1:]:
            if n % i == 0:
                return False
        return True
    def get_prime(self,n):
        if n < len(self.primes):
            p = self.primes[n]
        while n >= len(self.primes):
            p = self.next()
        return p
    def factorize(self,n):
        if n == 0 or n == 1:
            return []
        f = set()
        pr_i = 0
        while n > 1:
            p = self.get_prime(pr_i)
            pr_i += 1
            while n % p == 0:
                f.add(p)
                n = n // p
        return f

class Item:
    def __init__(self,iv):
        self.value = iv
        self.mod = {}
    def include_mod(self,m):
        self.mod[m] = self.value % m
    def add(self,v):
        if type(v) is int:
            v = Item(v)
            for m in self.mod:
                v.include_mod(m)
        if len(self.mod) > 0:
            for m in self.mod:
                self.mod[m] = (self.mod[m] + v.mod[m]) % m
        else:
            self.value += v.value
    def mul(self,v):
        if type(v) is int:
            v = Item(v)
            for m in self.mod:
                v.include_mod(m)
        if len(self.mod) > 0:
            for m in self.mod:
                self.mod[m] = (self.mod[m] * v.mod[m]) % m
        else:
            self.value *= v.value
    def set(self,v):
        if len(self.mod) > 0:
            for m in self.mod:
                self.mod[m] = v % m
        else:
            self.value = v
    def __str__(self):
        return "Item<{}>".format(self.value)

class ItemTest:
    def __init__(self,div,div_true,div_false):
        self.div = div
        self.div_true = div_true
        self.div_false = div_false
    def test(self,item):
        if self.div in item.mod:
            if item.mod[self.div] == 0:
                if VERBOSE: AoC.tprint("    Current worry level is divisible by {}.".format(self.div))
                return self.div_true
            if VERBOSE: AoC.tprint("    Current worry level is NOT divisible by {}.".format(self.div))
            return self.div_false

        if item.value % self.div == 0:
            if VERBOSE: AoC.tprint("    Current worry level is divisible by {}.".format(self.div))
            return self.div_true
        if VERBOSE: AoC.tprint("    Current worry level is NOT divisible by {}.".format(self.div))
        return self.div_false

class Monkey:
    def __init__(self,test,starting_items=[],operation=[],boredom=True):
        self.items = starting_items
        self.operation = operation
        self.test = test
        self.inspections = 0
        self.boredom = boredom
    def has_item(self):
        return len(self.items) > 0
    def hold_item(self,item):
        self.items.append(item)
    def inspect(self):
        self.inspections += 1
        item = self.items.pop(0)
        if self.test.div in item.mod:
            if VERBOSE: AoC.tprint("  Monkey inspects an item with a worry level of {}.".format(item.mod[self.test.div]))
            #if VERBOSE: AoC.tprint("  Monkey inspects an item with a worry level of {}.".format(item.mod[23]))
        else:
            if VERBOSE: AoC.tprint("  Monkey inspects an item with a worry level of {}.".format(item.value))
        if len(self.operation) > 0:
            if len(self.operation) != 3:
                raise Exception("Invalid operation: {}".format(" ".join(self.operation)))
            v1 = self.operation[0]
            v2 = self.operation[2]
            op = self.operation[1]
            if v1 == "old":
                v1 = item
            elif v1.isnumeric():
                v1 = int(v1)
            else:
                raise Exception("Invalid value: {}".format(v1))
            if v2 == "old":
                v2 = item
            elif v2.isnumeric():
                v2 = int(v2)
            else:
                raise Exception("Invalid value: {}".format(v2))
            if op == "+":
                item.add(v2)
            elif op == "*":
                item.mul(v2)
            else:
                raise Exception("Invalid operator: {}".format(op))
        if self.test.div in item.mod:
            if VERBOSE: AoC.tprint("    Worry level changes by {} to {}.".format(" ".join(self.operation),item.mod[self.test.div]))
            #if VERBOSE: AoC.tprint("    Worry level changes by {} to {}.".format(" ".join(self.operation),item.mod[23]))
        else:
            if VERBOSE: AoC.tprint("    Worry level changes by {} to {}.".format(" ".join(self.operation),item.value))
        if self.boredom:
            item.value = item.value // 3
            if VERBOSE: AoC.tprint("    Monkey gets bored with item. Worry level is divided by {} to {}".format(3,item.value))
        thr = self.test.test(item)
        if self.test.div in item.mod:
            if VERBOSE: AoC.tprint("    Item with worry level {} is thrown to monkey {}.".format(item.mod[self.test.div],thr))
            #if VERBOSE: AoC.tprint("    Item with worry level {} is thrown to monkey {}.".format(item.mod[23],thr))
        else:
            if VERBOSE: AoC.tprint("    Item with worry level {} is thrown to monkey {}.".format(item.value,thr))
        return item, thr

def factorize(n,factors):
    res = set()
    for f in factors:
        if n % f == 0:
            res.add(f)
    #print("factors (from {}) of {}: {}".format(factors, n,res))
    return res

def numerize(factors):
    p = 1
    for f in factors:
        p *= f
    #print("numerized {}: {}".format(factors,p))
    return p

def parse_monkeys(txt):
    monkeys = {}
    order = []
    state = None
    ln = -1
    mn = None
    si = None
    op = None
    test_check = None
    test_true = None
    test_false = None
    lines = txt.splitlines()
    while ln + 1 < len(lines):
        ln += 1
        line = lines[ln]
        if line.strip() == "":
            continue
        if line.startswith("Monkey "):
            if line.endswith(":"):
                mn = line.split()[1][:-1]
                ln += 1
                line = lines[ln]
                if not line.startswith("  "):
                    raise Exception("Parsing error on line {}: expected line to start indented\n{}".format(ln+1,line))
                parts = line[2:].split(":")
                if parts[0] == "Starting items":
                    si = [Item(int(n.strip())) for n in parts[1].split(',')]
                else:
                    raise Exception("Parsing error: Expected Starting items on line {}".format(ln+1))
                ln += 1
                line = lines[ln]
                if not line.startswith("  "):
                    raise Exception("Parsing error on line {}: expected line to start indented\n{}".format(ln+1,line))
                parts = line[2:].split(":")
                if parts[0] == "Operation":
                    op = parts[1].split("=")[1].strip().split()
                else:
                    raise Exception("Parsing error: Expected Operation on line {}".format(ln+1))
                ln += 1
                line = lines[ln]
                if not line.startswith("  "):
                    raise Exception("Parsing error on line {}: expected line to start indented\n{}".format(ln+1,line))
                parts = line[2:].split(":")
                if parts[0] == "Test":
                    if parts[1].strip().startswith("divisible by "):
                        test_check = int(parts[1].strip().split()[2])
                        ln += 1
                        line = lines[ln]
                        if not line.startswith("    If true:"):
                            raise Exception("Parsing error on line {}: Expected true case for Test property\n{}".format(ln+1,line))
                        parts = [p.strip() for p in line.strip().split(":")]
                        if parts[1].startswith("throw to monkey "):
                            test_true = parts[1].split()[3]
                        else:
                            raise Exception("Parsing error on line {}: Unknown Test action: {}".format(ln,parts[1]))
                        ln += 1
                        line = lines[ln]
                        if not line.startswith("    If false:"):
                            raise Exception("Parsing error on line {}: Expected false case for Test property\n{}".format(ln+1,line))
                        parts = [p.strip() for p in line.strip().split(":")]
                        if parts[1].startswith("throw to monkey "):
                            test_false = parts[1].split()[3]
                    else:
                        raise Exception("Parsing error on line {}: Unknown Test action: {}".format(ln,parts[1]))
                else:
                    raise Exception("Parsing error: Expected Test on line {}".format(ln+1))
                monkeys[mn] = Monkey(ItemTest(test_check,test_true,test_false),si,op)
                order.append(mn)
    return monkeys, order

def print_monkeys(monkeys,order):
    for m in order:
        print("Monkey {}: {}".format(m,", ".join(str(i) for i in monkeys[m].items)))
    print("")

def part1(inp):
    monkeys, order = parse_monkeys(inp)
    all_factors = set()
    for m in monkeys.values():
        all_factors.add(m.test.div)
    for r in range(20):
        AoC.tprint("- Round: {}".format(r + 1))
        for m in order:
            if VERBOSE: AoC.tprint("Monkey {}:".format(m))
            while monkeys[m].has_item():
                i, a = monkeys[m].inspect()
                monkeys[a].hold_item(i)
        if AoC.TEST:
            print_monkeys(monkeys,order)
    inspections = []
    for m in order:
        AoC.tprint("Monkey {} inpected items {} times.".format(m,monkeys[m].inspections))
        inspections.append(monkeys[m].inspections)
    inspections.sort(reverse=True)
    print("Monkey business: {}".format(inspections[0] * inspections[1]))

def part2(inp):
    monkeys, order = parse_monkeys(inp)
    all_factors = set()
    all_items = []
    for m in monkeys.values():
        m.boredom = False
        all_factors.add(m.test.div)
        for i in m.items:
            all_items.append(i)
    for i in all_items:
        for f in all_factors:
            i.include_mod(f)
    for r in range(10000):
    #for r in range(20):
        if r == 0 or r == 19 or ((r+1) % 1000 == 0):
            AoC.tprint("- Round: {}".format(r + 1))
        for m in order:
            while monkeys[m].has_item():
                i, a = monkeys[m].inspect()
                monkeys[a].hold_item(i)
            if r == 0 or r == 19 or ((r+1) % 1000 == 0):
                AoC.tprint("Monkey {} inpected items {} times.".format(m,monkeys[m].inspections))
    inspections = []
    for m in order:
        inspections.append(monkeys[m].inspections)
    inspections.sort(reverse=True)
    print("Monkey business: {}".format(inspections[0] * inspections[1]))

def main():
    AoC.set_day("11")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("--- Part 1 ---")
    part1(inp)
    print("--- Part 2 ---")
    part2(inp)

if __name__ == "__main__":
    main()
