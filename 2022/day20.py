#!/usr/bin/python3

import AoC

_DEBUG = False

class LinkedList:
    def __init__(self):
        self.head = Node(None)
        self.tail = Node(None)
        self.head.next = self.tail
        self.tail.prev = self.head
    def push(self,node):
        node.insert_before(self.tail)
    def insert(self,node):
        node.insert_after(self.head)
    def shift(self,node,n):
        if _DEBUG: print(f"ll->shift({node},{n})")
        shf_node = node
        if n < 0:
            shf_node = node.prev
            if shf_node == self.head:
                shf_node = self.tail.prev
            node.unlink()
            while (n := n + 1) < 0:
                if shf_node.prev == self.head:
                    shf_node = self.tail
                shf_node = shf_node.prev
            if shf_node.prev == self.head:
                shf_node = self.tail
            node.insert_before(shf_node)
        elif n > 0:
            shf_node = node.next
            if shf_node == self.tail:
                shf_node = self.head.next
            node.unlink()
            while (n := n - 1) > 0:
                if shf_node.next == self.tail:
                    shf_node = self.head
                shf_node = shf_node.next
            if shf_node.next == self.tail:
                shf_node = self.head
            node.insert_after(shf_node)

    def find(self,v):
        node = self.head.next
        while node != self.tail:
            if node.v == v:
                return node
            node = node.next
        return None

    def traverse(self,node,c):
        r = node
        if c > 0:
            while c > 0:
                r = r.next
                if r == self.tail:
                    r = self.head.next
                c -= 1
        elif c < 0:
            while c < 0:
                r = r.prev
                if r == self.head:
                    r = self.tail.prev
                c += 1
        return r

    def print(self):
        s = ""
        n = self.head.next
        while n.next:
            if len(s) > 0:
                s += ", "
            s += str(n.v)
            n = n.next
        print(s)

class Node:
    def __init__(self,v,p=None,n=None):
        self.v = v
        self.prev = p
        self.next = n
        
    def unlink(self):
        if self.prev is not None:
            self.prev.next = self.next
        if self.next is not None:
            self.next.prev = self.prev
        self.prev = None
        self.next = None

    def insert_after(self,node):
        if _DEBUG: print(f"({self})->insert_after({node})")
        self.next = node.next
        self.next.prev = self
        node.next = self
        self.prev = node

    def insert_before(self,node):
        if _DEBUG: print(f"({self})->insert_before({node})")
        self.prev = node.prev
        self.prev.next = self
        node.prev = self
        self.next = node

    def __str__(self):
        p = "Node<{}>".format(self.prev.v) if self.prev is not None else "None"
        n = "Node<{}>".format(self.next.v) if self.next is not None else "None"
        return f"{p} <- Node<{self.v}> -> {n}"

##########################################
#vvv UNUSED POSITIONAL LIST FUNCTIONS vvv#
##########################################
def swap(l,a,b):
    l[a], l[b] = l[b], l[a]

def shift(pa,i,v):
    if _DEBUG: print(f"shift({i},{v})")
    while v <= 0 - len(pa):
        v += len(pa)
    while v >= len(pa):
        v -= len(pa)
    if i + v <= 0:
        v += len(pa) - 1 
    elif i + v >= len(pa) - 1:
        v -= len(pa) - 1
    print(f"adjusted v: {v}")
    d = i + v
    if v < 0:
        # go backwards
        for j in range(i,d,-1):
            swap(pa,j,j-1)
    else:
        # go forwards
        for j in range(i,d):
            swap(pa,j,j+1)
    return d

def build_list(l,p):
    offsets = list(x for x in p)
    for i in range(len(offsets)):
        while offsets[i] <= 0 - len(offsets):
            offsets[i] += len(offsets)
        while offsets[i] >= len(offsets):
            offsets[i] -= len(offsets)
    for i in range(len(offsets)):
        for j in range(i,i+offsets[i]):
            pass
            
    r = [None] * len(l)
    for i in range(len(l)):
        offset = (i + p[i]) % len(l)
        r[offset] = l[i]
    return r
##########################################
#^^^ UNUSED POSITIONAL LIST FUNCTIONS ^^^#
##########################################

def parse_list(txt):
    l = []
    for n in txt.splitlines():
        v = n.strip()
        if v == "":
            continue
        l.append(int(v))
    return l

def build_nodelist(l):
    ll = LinkedList()
    nl = []
    for v in l:
        node = Node(v)
        nl.append(node)
        ll.push(node)
    return nl, ll

def printll(l,c):
    v = []
    n = l
    while c > 0:
        v.append(n.v)
        n = n.next
        c -= 1
    print(", ".join(str(x) for x in v))

def nsuffix(n):
    s = str(n)
    if s[-1] == "1":
        return "st"
    if s[-1] == "2":
        return "nd"
    if s[-1] == "3":
        return "rd"
    return "th"

def part1(inp):
    l = parse_list(inp)
    nl, ll = build_nodelist(l)
    N = len(l)
    s = [False] * len(l)
    i = 0
    AoC.tprint("Initial arrangement:")
    AoC.tprint(", ".join(str(n) for n in l))
    AoC.tprint("")
    for j in range(N):
        if _DEBUG: print(f"{j}:{l[i]}|{nl[j]}")
        v = l.pop(i)
        vn = nl[j].v
        if v != vn:
            print(f"ALERT: Values are not equal at step {j} (list val: {v}, node val: {vn})")
        b = s.pop(i)
        p = i + v
        if vn > N:
            vn = vn % (N-1)
        if vn < (0-N):
            vn = (vn % (N-1)) - (N-1)
        ll.shift(nl[j],vn)
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
            npeek1 = nl[j].prev.v
            npeek2 = nl[j].next.v
            AoC.tprint(f"{vn} moves between {npeek1} and {npeek2}")
            if peek1 != npeek1:
                print(f"ALERT: at step {j}, node {v} moves after {peek1} in list, but {npeek1} in nodes")
            if peek2 != npeek2:
                print(f"ALERT: at step {j}, node {v} moves before {peek2} in list, but {npeek2} in nodes")
        l.insert(p,v)
        s.insert(p,True)
        if AoC.TEST:
            print(", ".join(str(n) for n in l))
            ll.print()
            print("")
        while i < N and s[i]:
            i += 1
    zero_p = -1
    for i in range(N):
        if l[i] == 0:
            zero_p = i
            break
    i1 = 1000
    i2 = 2000
    i3 = 3000
    a = l[(zero_p + i1) % N]
    b = l[(zero_p + i2) % N]
    c = l[(zero_p + i3) % N]
    print(f"The {i1}{nsuffix(i1)} number after 0 is {a}, the {i2}{nsuffix(i2)} is {b} and the {i3}{nsuffix(i3)} is {c}; adding these together produces {sum([a,b,c])}.")
    zero_node = ll.find(0)
    a = ll.traverse(zero_node,i1 % N)
    b = ll.traverse(zero_node,i2 % N)
    c = ll.traverse(zero_node,i3 % N)
    print(f"The {i1}{nsuffix(i1)} number after 0 is {a.v}, the {i2}{nsuffix(i2)} is {b.v} and the {i3}{nsuffix(i3)} is {c.v}; adding these together produces {sum([a.v,b.v,c.v])}.")
        

def part2(inp):
    l = parse_list(inp)
    N = len(l)
    lm = {}
    for i in range(len(l)):
        l[i] *= 811589153
        lm[l[i]] = l[i]
        if l[i] > N:
            lm[l[i]] = l[i] % (N-1)
        elif l[i] < (0-N):
            lm[l[i]] = (l[i] % (N-1)) - (N-1)
    nl, ll = build_nodelist(l)
    AoC.tprint("Initial arrangement:")
    AoC.tprint(", ".join(str(n) for n in l))
    AoC.tprint("")
    for round in range(10):
        for i in range(N):
            if _DEBUG: print(f"{i}:{nl[i]}")
            v = lm[nl[i].v]
            ll.shift(nl[i],v)
        if AoC.TEST:
            print(f"After {round+1} round{'s' if round != 1 else ''} of mixing:")
            ll.print()
            print("")
    i1 = 1000
    i2 = 2000
    i3 = 3000
    zero_node = ll.find(0)
    a = ll.traverse(zero_node,i1 % N)
    b = ll.traverse(zero_node,i2 % N)
    c = ll.traverse(zero_node,i3 % N)
    print(f"The {i1}{nsuffix(i1)} number after 0 is {a.v}, the {i2}{nsuffix(i2)} is {b.v} and the {i3}{nsuffix(i3)} is {c.v}; adding these together produces {sum([a.v,b.v,c.v])}.")

def main():
    AoC.set_day("20")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("--- Part 1 ---")
    part1(inp)
    print("--- Part 2 ---")
    part2(inp)

if __name__ == "__main__":
    main()
