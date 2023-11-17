#!/usr/bin/python3

import heapq
import AoC

class Map:
    def __init__(self):
        self.map_data = []
        self.all_states = None
        self.states_init = False
        self.current_state = None

    def add_row(self,row):
        rdata = []
        for c in row:
            if c == ".":
                rdata.append([])
            else:
                rdata.append([c])
        self.map_data.append(rdata)
    def width(self):
        return len(self.map_data[0])
    def height(self):
        return len(self.map_data)
    
    def get(self,x,y):
        if y < 0 or y > len(self.map_data):
            return "X"
        if x < 0 or x > len(self.map_data[y]):
            return "X"
        o = self.map_data[y][x]
        if len(o) == 0:
            return '.'
        elif len(o) > 1:
            return str(len(o))
        return o[0]

    def __copy_map_data(self):
        map_data = []
        for row in self.map_data:
            r = []
            for objs in row:
                r.append(objs.copy())
            map_data.append(r)
        return map_data

    def init_states(self):
        self.all_states = [self.__copy_map_data()]
        for i in range(gcd(self.width(),self.height())):
            self.advance()
            self.all_states.append(self.__copy_map_data())
        self.map_data = self.all_states[0]
        self.current_state = 0
        self.states_init = True

    def reset(self):
        if self.all_states is not None:
            self.map_data = self.all_states[0]

    def load_state(self,n):
        self.map_data = self.all_states[n % len(self.all_states)]

    def advance(self):
        if self.states_init:
            self.current_state += 1
            self.map_data = self.all_states[self.current_state]
            return
        if self.all_states is None:
            self.all_states = [self.__copy_map_data()]
        new_map = []
        for row in self.map_data:
            r = []
            for objs in row:
                r.append([])
            new_map.append(r)
        y = 0
        for row in self.map_data:
            x = 0
            for objs in row:
                for obj in objs:
                    if obj == ">":
                        if "#" in self.map_data[y][x+1]:
                            new_map[y][1].append(obj)
                        else:
                            new_map[y][x+1].append(obj)
                    elif obj == "v":
                        if "#" in self.map_data[y+1][x]:
                            new_map[1][x].append(obj)
                        else:
                            new_map[y+1][x].append(obj)
                    elif obj == "<":
                        if "#" in self.map_data[y][x-1]:
                            new_map[y][len(new_map[y])-2].append(obj)
                        else:
                            new_map[y][x-1].append(obj)
                    elif obj == "^":
                        if "#" in self.map_data[y-1][x]:
                            new_map[len(new_map)-2][x].append(obj)
                        else:
                            new_map[y-1][x].append(obj)
                    else:
                        new_map[y][x].append(obj)
                x += 1
            y += 1
        self.map_data = new_map

    def __str__(self):
        s = ""
        for row in self.map_data:
            for objs in row:
                if len(objs) == 0:
                    s += "."
                elif len(objs) > 1:
                    s += str(len(objs))
                else:
                    s += objs[0]
            s += "\n"
        return s

def gcd(a,b):
    h,l = (a,b) if a > b else (b,a)
    if h % l == 0:
        return l
    return h * l

def draw_elephant(m,e):
    draw = str(m)
    lines = []
    y = 0
    for line in draw.splitlines():
        if e[1] == y:
            line = line[:e[0]] + "E" + line[e[0]+1:]
        lines.append(line)
        y += 1
    print("\n".join(lines))
    print("")

def parse_map(txt):
    start = None
    goal = None
    width = None
    height = None
    themap = Map()
    y = 0
    for line in txt.splitlines():
        x = 0
        for c in line:
            if x == 0:
                if c != "#":
                    raise Exception(f"Line {y+1} did not start with '#'")
            if y == 0:
                if c not in ("#","."):
                    raise Exception(f"Invalid char on line 1: {c} (expected '#' or '.'")
                if c == ".":
                    if start is None:
                        start = (x,y)
                    else:
                        raise Exception("Two start positions defined")
            x += 1
        if c != "#":
            raise Exception(f"Line {y+1} did not end with '#'")
        if width is None:
            width = x-1
        elif width != x-1:
            raise Exception(f"Line {y+1} did not match width {width}")
        themap.add_row(line)
        y += 1
    x = 0
    for c in line:
        if c not in ("#","."):
            raise Exception(f"Invalid char on last line ({y}): {c} (expected '#' or '.'")
        if c == ".":
            if goal is None:
                goal = (x,y-1)
            else:
                raise Exception("Two goal positions defined")
        x += 1
    if start is None:
        raise Exception("Unable to determine starting point")
    if goal is None:
        raise Exception("Unable to determine goal point")
    return themap, start, goal

def dist(p1,p2):
    return abs(p2[0] - p1[1]) + abs(p2[1] - p1[1])

def pq_best_path(themap,start,goal):
    themap.init_states()
    search = []
    heapq.heappush(search, (dist(start,goal),[start]) )
    while True:
        print(f"searches: {len(search)}")
        _, path = heapq.heappop(search)
        themap.load_state(len(path))
        lp = path[-1]
        options = []
        if themap.get(lp[0],lp[1]) == ".":
            options.append((lp[0],lp[1]))
        if lp[0] > 0 and themap.get(lp[0]-1,lp[1]) == ".":
            options.append((lp[0]-1,lp[1]))
        if lp[1] > 0 and themap.get(lp[0],lp[1]-1) == ".":
            options.append((lp[0],lp[1]-1))
        if lp[0] < themap.width() - 1 and themap.get(lp[0]+1,lp[1]) == ".":
            options.append((lp[0]+1,lp[1]))
        if lp[1] < themap.height() - 1 and themap.get(lp[0],lp[1]+1) == ".":
            options.append((lp[0],lp[1]+1))
        print(f"options: {options}")
        for opt in options:
            if opt == goal:
                return path + [opt]
            heapq.heappush(search,(dist(opt,goal) + len(path), path + [opt]))
        #print(f"search: {search}")

def visit_once_best_path(themap,start,goals):
    themap.reset()
    if not type(goals) == list:
        goals = [goals]
    search_from = start
    search = []
    paths = []
    minute = 0
    while goals:
        if search_from:
            #print(f"new search from {search_from} to {goals[0]}")
            search = [[search_from]]
            search_from = None
        minute += 1
        themap.advance()
        #print(f"minute: {minute}, searches: {len(search)}")
        #print(themap)
        new_search = []
        visited = set()
        while search:
            path = search.pop()
            lp = path[-1]
            if lp in visited:
                continue
            visited.add(lp)
            options = []
            N, E, S, W = (lp[0],lp[1]-1), (lp[0]+1,lp[1]), (lp[0],lp[1]+1), (lp[0]-1,lp[1])
            if themap.get(lp[0],lp[1]) == ".":
                options.append((lp[0],lp[1]))
            if lp[0] > 0 and themap.get(lp[0]-1,lp[1]) == ".":
                options.append((lp[0]-1,lp[1]))
            if lp[1] > 0 and themap.get(lp[0],lp[1]-1) == ".":
                options.append((lp[0],lp[1]-1))
            if lp[0] < themap.width() - 1 and themap.get(lp[0]+1,lp[1]) == ".":
                options.append((lp[0]+1,lp[1]))
            if lp[1] < themap.height() - 1 and themap.get(lp[0],lp[1]+1) == ".":
                options.append((lp[0],lp[1]+1))
            #print(f"X {lp} -> {themap.get(lp[0],lp[1])}")
            #print(f"N {N} -> {themap.get(lp[0],lp[1]-1)}")
            #print(f"E {E} -> {themap.get(lp[0]+1,lp[1])}")
            #print(f"S {S} -> {themap.get(lp[0],lp[1]+1)}")
            #print(f"W {W} -> {themap.get(lp[0]-1,lp[1])}")
            #print(f"path: {path}")
            #print(f"options: {options}")
            for opt in options:
                if opt == goals[0]:
                    #print("found")
                    paths.append(path + [opt])
                    path = []
                    new_search = []
                    search = []
                    search_from = goals.pop(0)
                    break
                else:
                    new_search.append(path + [opt])
        search = new_search
    return [x for p in paths for x in p]

def part1(inp):
    themap, start, goal = parse_map(inp)
    #best_path = pq_best_path(themap,start,goal)
    best_path = visit_once_best_path(themap,start,goal)
    if AoC.TEST:
        themap.reset()
        print("Initial State:")
        draw_elephant(themap,best_path[0])
        lp = best_path[0]
        m = 1
        for p in best_path[1:]:
            if lp == p:
                action = "wait"
            elif lp == (p[0]-1,p[1]):
                action = "move right"
            elif lp == (p[0],p[1]-1):
                action = "move down"
            elif lp == (p[0]+1,p[1]):
                action = "move left"
            elif lp == (p[0],p[1]+1):
                action = "move up"
            else:
                action = "jump?"
            print(f"Minute {m}, {action}:")
            themap.advance()
            draw_elephant(themap,p)
            lp = p
            m += 1

    print(f"Best path minutes: {len(best_path)-1}")

def part2(inp):
    themap, start, goal = parse_map(inp)
    #best_path = pq_best_path(themap,start,goal)
    best_path = visit_once_best_path(themap,start,[goal,start,goal])
    if AoC.TEST:
        themap.reset()
        print("Initial State:")
        draw_elephant(themap,best_path[0])
        lp = best_path[0]
        m = 1
        for p in best_path[1:]:
            if lp == p:
                action = "wait"
            elif lp == (p[0]-1,p[1]):
                action = "move right"
            elif lp == (p[0],p[1]-1):
                action = "move down"
            elif lp == (p[0]+1,p[1]):
                action = "move left"
            elif lp == (p[0],p[1]+1):
                action = "move up"
            else:
                action = "jump?"
            print(f"Minute {m}, {action}:")
            themap.advance()
            draw_elephant(themap,p)
            lp = p
            m += 1

    # i don't feel great about the -3, it's possible i just got lucky
    print(f"Best path minutes: {len(best_path)-3}")

def main():
    AoC.set_day("24")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("--- Part 1 ---")
    part1(inp)
    print("--- Part 2 ---")
    part2(inp)

if __name__ == "__main__":
    main()
