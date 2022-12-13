#!/usr/bin/python3

import AoC

class GridNode:
    def __init__(self,h):
        self.h = h
        self.visited = False

class HeightMap:
    def __init__(self):
        self.nodes = {}
        self.start = None
        self.end = None
        self.width = 0
        self.height = 0
    def add_node(self,x,y,h):
        if (x,y) in self.nodes:
            raise Exception("Node already exists at ({},{})".format(x,y))
        node = GridNode(h)
        self.nodes[(x,y)] = node
        if x > self.width:
            self.width = x
        if y > self.height:
            self.height = y
    def __str__(self):
        lines = []
        l = ""
        p = (0,0)
        while p in self.nodes:
            if p == self.start:
                l = l + "S"
            elif p == self.end:
                l = l + "E"
            else:
                l = l + chr((self.nodes[p].h - 1) + ord('a'))
            p = (p[0]+1,p[1])
            if p not in self.nodes:
                lines.append(l)
                l = ""
                p = (0,p[1]+1)
        return "\n".join(lines)

def parse_height_map(text):
    hm = HeightMap()
    y = 0
    for line in text.splitlines():
        line = line.strip()
        x = 0
        for c in line:
            if c == 'S':
                hm.start = (x,y)
                c = 'a'
            if c == 'E':
                hm.end = (x,y)
                c = 'z'
            hm.add_node(x,y,(ord(c) - ord('a'))+1)
            x += 1
        y += 1
    return hm

def print_path(path,se,dim):
    start, end = se
    mat = []
    for y in range(dim[1]+1):
        row = []
        for x in range(dim[0]+1):
            row.append(".")
        mat.append(row)
    p = start
    for n in path:
        c = ''
        if n == "n":
            c = '^'
            np = (p[0],p[1]-1)
        elif n == "e":
            c = '>'
            np = (p[0]+1,p[1])
        elif n == "s":
            c = 'v'
            np = (p[0],p[1]+1)
        elif n == "w":
            c = '<'
            np = (p[0]-1,p[1])
        mat[p[1]][p[0]] = c
        p = np
    mat[end[1]][end[0]] = 'E'
    print("\n".join("".join(row) for row in mat))

def part1(inp):
    hm = parse_height_map(inp)
    frontier = [hm.start]
    paths = {hm.start: []}
    while frontier:
        #print(frontier)
        p = frontier.pop(0)
        node = hm.nodes[p]
        if node.visited:
            #print("already visited {}".format(p))
            #print("path[{}]: {}".format(p,paths[p]))
            continue
        node.visited = True
        if p == hm.end:
            break
        next_p = {"n": (p[0],p[1]-1), "e": (p[0]+1,p[1]), "s": (p[0],p[1]+1), "w": (p[0]-1,p[1])}
        for d in next_p:
            np = next_p[d]
            if np in hm.nodes:
                if hm.nodes[np].visited:
                    continue
                nn = hm.nodes[np]
                if nn.h <= (node.h + 1):
                    frontier.append(np)
                    paths[np] = list(paths[p]) + [d]
        #print("path[{}]: {}".format(p,paths[p]))
    #print(paths)
    if hm.end not in paths:
        print("No path to goal")
    if AoC.TEST:
        print_path(paths[hm.end],(hm.start,hm.end),(hm.width,hm.height))
    print("Shortest path to goal: {} steps".format(len(paths[hm.end])))

def reverse_path(path):
    rpath = []
    for d in path[-1::-1]:
        if d == "n":
            rpath.append("s")
        elif d == "e":
            rpath.append("w")
        elif d == "s":
            rpath.append("n")
        elif d == "w":
            rpath.append("e")
    return rpath

def part2(inp):
    hm = parse_height_map(inp)
    frontier = [hm.end]
    paths = {hm.end: []}
    start = None
    while frontier:
        #print(frontier)
        p = frontier.pop(0)
        node = hm.nodes[p]
        if node.visited:
            #print("already visited {}".format(p))
            #print("path[{}]: {}".format(p,paths[p]))
            continue
        node.visited = True
        if node.h == 1:
            start = p
            break
        next_p = {"n": (p[0],p[1]-1), "e": (p[0]+1,p[1]), "s": (p[0],p[1]+1), "w": (p[0]-1,p[1])}
        for d in next_p:
            np = next_p[d]
            if np in hm.nodes:
                if hm.nodes[np].visited:
                    continue
                nn = hm.nodes[np]
                if nn.h >= (node.h - 1):
                    frontier.append(np)
                    paths[np] = list(paths[p]) + [d]
        #print("path[{}]: {}".format(p,paths[p]))
    #print(paths)
    if start is None:
        print("No path to goal")
    goal_path = reverse_path(paths[start])
    if AoC.TEST:
        print_path(goal_path,(start,hm.end),(hm.width,hm.height))
    print("Shortest path to goal: {} steps".format(len(goal_path)))

def main():
    AoC.set_day("12")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("== Part 1 ==")
    part1(inp)
    print("== Part 2 ==")
    part2(inp)

if __name__ == "__main__":
    main()
