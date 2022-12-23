#!/usr/bin/python3

import re
import AoC

class Valve:
    def __init__(self,name,flow):
        self.name = name
        self.flow = flow
        self.tunnels = []
    def add_tunnel(self,valve):
        self.tunnels.append(valve)
    def __str__(self):
        return repr(self)
    def __repr__(self):
        n = self.name
        f = self.flow
        t = ", ".join(v.name for v in self.tunnels)
        return "Valve_{}<{}> -> {}".format(n,f,t)

re_prog = None
def parse_valve(txt):
    global re_prog
    if re_prog is None:
        pattern = r'^Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? (.+)$'
        re_prog = re.compile(pattern)
    m = re_prog.match(txt)
    name, flow, connects = m.groups()
    flow = int(flow)
    connects = connects.split(", ")
    return Valve(name, flow), connects
    
find_path_memo = {}
def find_path(valves,frv,tov):
    if (frv,tov) in find_path_memo:
        return find_path_memo[(frv,tov)]
    search = [[frv]]
    visited = set()
    while search:
        #print(search)
        path = search.pop(0)
        v = path[-1]
        if v == tov:
            find_path_memo[(frv,tov)] = path[1:]
            return path[1:]
        visited.add(v)
        for t in v.tunnels:
            if t not in visited:
                search.append(path + [t])
    return None

def find_best_move(valves,frv,timer,open_valves=set(),elephant=False):
    #print("find_best_move({},{})".format(frv.name,timer))
    if timer <= 0:
        return ([], 0)
    best_move = (["<>"]*timer, 0)
    if set(valves.keys()) == open_valves:
        return best_move
    for nxt in valves.values():
        nxt_timer = timer - 1
        if nxt not in open_valves and nxt.flow > 0:
            if nxt == frv:
                path = []
            else:
                path = find_path(valves,frv,nxt)
            if path is None:
                print("No path from {} to {}".format(frv.name,nxt.name))
                continue
            nxt_timer -= len(path)
            if nxt_timer > 0:
                next_best_move = find_best_move(valves,nxt,nxt_timer,open_valves.union(set([nxt])),elephant=elephant)
                pr = nxt.flow * nxt_timer
                if pr + next_best_move[1] > best_move[1]:
                    best_move = (path + ["<open>"] + next_best_move[0], pr + next_best_move[1])

    #print("find_best_move({},{}):{}".format(frv.name,timer,best_move))
    return best_move

def print_schedule(sch):
    timer = len(sch)
    open_valves = []
    location = None
    minute = 1
    while minute <= len(sch):
        print("== Minute {} ==".format(minute))
        if len(open_valves) == 0:
            print("No valves are open.")
        else:
            pr = sum(v.flow for v in open_valves)
            pl = len(open_valves) > 1
            str_valves = "{} and {}".format(", ".join(v.name for v in open_valves[0:-1]),open_valves[-1].name) if pl else open_valves[0].name
            print("Valve{} {} {} open, releasing {} pressure.".format("s" if pl else "", str_valves, "are" if pl else "is",pr))
        act = sch[minute-1]
        if act == "<open>":
            print("You open valve {}.".format(location.name))
            open_valves.append(location)
            open_valves.sort(key=lambda x: x.name)
        elif type(act) is Valve:
            print("You move to valve {}.".format(act.name))
            location = act
        print()
        minute += 1

def part1(inp):
    valves = {}
    connections = {}
    for line in inp.splitlines():
        line = line.strip()
        valve, conn = parse_valve(line)
        valves[valve.name] = valve
        connections[valve.name] = conn
    for v in valves:
        for c in connections[v]:
            valves[v].add_tunnel(valves[c])
    
    #print(valves)
    schedule, pressure = find_best_move(valves,valves['AA'],30)
    if AoC.TEST or True:
        print_schedule(schedule)
    print("The total released pressure is: {}".format(pressure))

def part2(inp):
    valves = {}
    connections = {}
    for line in inp.splitlines():
        line = line.strip()
        valve, conn = parse_valve(line)
        valves[valve.name] = valve
        connections[valve.name] = conn
    for v in valves:
        for c in connections[v]:
            valves[v].add_tunnel(valves[c])
    
    #print(valves)
    schedule, pressure = find_best_move(valves,valves['AA'],30,elephant=True)
    if AoC.TEST or True:
        print_schedule(schedule)
    print("The total released pressure is: {}".format(pressure))

def main():
    AoC.set_day("16")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("== Part 1 ==")
    part1(inp)
    print("== Part 2 ==")
    part2(inp)

if __name__ == "__main__":
    main()
