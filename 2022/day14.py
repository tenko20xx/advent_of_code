#!/usr/bin/python3

import AoC
from collections import namedtuple

Point = namedtuple("Point", ["x","y"])

class Scene:
    def __init__(self,sand_pos,floor=None):
        self.sand_pos = sand_pos
        self.resting_sand = 0
        self.floor = floor
        self.units = {sand_pos:"+"}
        self.min_x = sand_pos.x
        self.min_y = sand_pos.y
        self.max_x = sand_pos.x
        self.max_y = sand_pos.y
        if floor is not None:
            self.max_y += floor
    def add_obj(self,p,o):
        self.units[p] = o
        if p.x < self.min_x:
            self.min_x = p.x
        if p.y < self.min_y:
            self.min_y = p.y
        if p.x > self.max_x:
            self.max_x = p.x
        if p.y > self.max_y:
            self.max_y = p.y
        if p == self.sand_pos:
            self.sand_pos = None
    def add_sand(self,p):
        self.add_obj(p,"o")
        self.resting_sand += 1
    def add_rock(self,p):
        #print("add_rock({})".format(p))
        self.add_obj(p,"#")
        if self.floor is not None:
            if p.y + self.floor > self.max_y:
                self.max_y = p.y + self.floor
    def add_rock_line(self,from_p,to_p):
        if from_p.x != to_p.x:
            step = 1 if from_p.x < to_p.x else -1
            y = from_p.y
            for x in range(from_p.x,to_p.x+step,step):
                self.add_rock(Point(x,y))
        elif from_p.y != to_p.y:
            step = 1 if from_p.y < to_p.y else -1
            x = from_p.x
            for y in range(from_p.y,to_p.y+step,step):
                self.add_rock(Point(x,y))
    def drop_sand(self):
        if self.sand_pos is None:
            return False
        sand = Point(self.sand_pos.x,self.sand_pos.y)
        resting = False
        while not resting and sand.y < self.max_y:
            sx, sy = sand
            try_p = [ Point(sx,sy+1), Point(sx-1,sy+1), Point(sx+1,sy+1) ]
            resting = True
            for p in try_p:
                if p not in self.units:
                    sand = p
                    resting = False
                    break
        if self.floor is None:
            if sand.y > self.max_y:
                resting = False
        else:
            resting = True
        if resting:
            self.add_sand(sand)
            return True
        return False

    def __str__(self):
        lines = []
        w = len(str(self.max_y))+1
        for y in range(self.min_y,self.max_y+1):
            lines.append(("{: "+str(w)+"} {}").format(y,"".join(self.units.get((x,y),".") for x in range(self.min_x-1,self.max_x+2))))
        if self.floor:
            lines.append(("{: "+str(w)+"} {}").format(self.max_y+1,"#"*((self.max_x - self.min_x)+3)))
        lines.append("="*((self.max_x - self.min_x)+w+4))
        return "\n".join(lines)

def part1(inp):
    scene = Scene(Point(500,0))
    for line in inp.splitlines():
        p1 = None
        p2 = None
        for pair in line.split(" -> "):
            p = tuple(int(n) for n in pair.split(","))
            p = Point(p[0],p[1])
            if p2 is None:
                p2 = p
                continue
            p1 = p2
            p2 = p
            scene.add_rock_line(p1,p2)
    AoC.tprint(scene)
    while scene.drop_sand():
        AoC.tprint(scene)
    print("Total units of sand: {}".format(scene.resting_sand))

def part2(inp):
    scene = Scene(Point(500,0),floor=1)
    for line in inp.splitlines():
        p1 = None
        p2 = None
        for pair in line.split(" -> "):
            p = tuple(int(n) for n in pair.split(","))
            p = Point(p[0],p[1])
            if p2 is None:
                p2 = p
                continue
            p1 = p2
            p2 = p
            scene.add_rock_line(p1,p2)
    AoC.tprint(scene)
    while scene.drop_sand():
        AoC.tprint(scene)
    print("Total units of sand: {}".format(scene.resting_sand))

def main():
    AoC.set_day("14")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("== Part 1 ==")
    part1(inp)
    print("== Part 2 ==")
    part2(inp)

if __name__ == "__main__":
    main()
