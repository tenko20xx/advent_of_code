#!/usr/bin/python3

import re
import AoC

from itertools import permutations

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
        return "Valve_{}<{}> -> ({})".format(n,f,t)

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

def find_best_move(valves,frv,timer,open_valves=set()):
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
                next_best_move = find_best_move(valves,nxt,nxt_timer,open_valves.union(set([nxt])))
                pr = nxt.flow * nxt_timer
                if pr + next_best_move[1] > best_move[1]:
                    best_move = (path + ["<open>"] + next_best_move[0], pr + next_best_move[1])

    #print("find_best_move({},{}):{}".format(frv.name,timer,best_move))
    return best_move

def find_best_move2(valves,frv,timer,closed_valves=None):
    if timer <= 0:
        return (0, [])
    if closed_valves is None:
        closed_valves = set(valves)
    targets = []
    for vname in closed_valves:
        v = valves[vname]
        if v.flow == 0:
            continue
        #print(v)
        path = find_path(valves,frv,v)
        #print(path)
        gain = v.flow * ((timer - 1) - len(path))
        target = (v,gain,path)
        targets.append(target)
    best_move = (0, ["<>"] * timer)
    if targets:
        for t in targets:
            new_timer = timer - (len(t[2]) + 1)
            new_move = find_best_move2(valves,t[0],new_timer,closed_valves - set([t[0].name]))
            #print(new_move)
            if new_move[0] + t[1] > best_move[0]:
                best_move = (new_move[0] + t[1], t[2] + ["<open>"] + new_move[1])
        #print(best_move)
    return best_move

def find_best_move3(valves,mfrv,efrv,timer,closed_valves=None,mtargetv=None,etargetv=None):
    if timer <= 0:
        return (0, [], True)
    if closed_valves is None:
        closed_valves = set(valves)
    targets = set()
    best_move = (0, [("<>","<>")] * timer, False)
    mact = None
    eact = None

    #print(f"{mtargetv=},{etargetv=}")
    if mtargetv is None:
        new_target = False
        for v in sorted(closed_valves,reverse=True):
            if valves[v].flow == 0:
                continue
            new_target = True
            new_move = find_best_move3(valves,mfrv,efrv,timer,closed_valves,v,etargetv)
            if new_move[0] > best_move[0]:
                best_move = new_move
                #if best_move[2]:
                #    return best_move
        if not new_target:
            #print("m wait")
            mact = "<>"
    if etargetv is None:
        new_target = False
        for v in sorted(closed_valves,reverse=True):
            if valves[v].flow == 0:
                continue
            new_target = True
            new_move = find_best_move3(valves,mfrv,efrv,timer,closed_valves,mtargetv,v)
            if new_move[0] > best_move[0]:
                best_move = new_move
                #if best_move[2]:
                #    return best_move
        if not new_target:
            #print("e wait")
            eact = "<>"
    if mact == "<>" and eact == "<>":
        return (0,[("<>","<>")]*timer,True)

    new_closed_valves = closed_valves.copy()
    gain = 0
    if mtargetv:
        if mtargetv not in closed_valves:
            return (0, [], False)
        if mtargetv == etargetv:
            return (0, [], False)
        mpath = find_path(valves,mfrv,valves[mtargetv])
        if mpath:
            mact = mpath[0]
            mfrv = mact
        else:
            mact = "<open>"
            gain += mfrv.flow * (timer - 1)
            new_closed_valves = new_closed_valves - set([mtargetv])
            mtargetv = None
    if etargetv:
        if etargetv not in closed_valves:
            return (0, [], False)
        epath = find_path(valves,efrv,valves[etargetv])
        if epath:
            eact = epath[0]
            efrv = eact
        else:
            eact = "<open>"
            gain += efrv.flow * (timer - 1)
            new_closed_valves = new_closed_valves - set([etargetv])
            etargetv = None
    new_move = find_best_move3(valves,mfrv,efrv,timer-1,new_closed_valves,mtargetv,etargetv)
    #print(f"{new_move=}")
    if new_move[0] + gain > best_move[0]:
        best_move = (new_move[0] + gain,[(mact,eact)] + new_move[1], False)
    return best_move

def find_best_move_elephant(valves,frv,timer,open_valves=set()):
    #print("find_best_move({},{})".format(frv.name,timer))
    if timer <= 0:
        return ([],[], 0)
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
                next_best_move = find_best_move(valves,nxt,nxt_timer,open_valves.union(set([nxt])))
                pr = nxt.flow * nxt_timer
                if pr + next_best_move[1] > best_move[1]:
                    best_move = (path + ["<open>"] + next_best_move[0], pr + next_best_move[1])

    #print("find_best_move({},{}):{}".format(frv.name,timer,best_move))
    return best_move

def find_best_move4(valves,frv,timer,avail=None):
    if timer <= 0:
        return (0, [])
    if avail is None:
        avail = set(valves)
    gains = []
    best_gain = (0, None)
    for v in avail:
        if valves[v].flow == 0:
            continue
        path = find_path(valves,frv,valves[v])
        new_timer = ((timer - 1) - len(path))
        gain = valves[v].flow * new_timer
        gains.append((gain,v,new_timer))
        if gain > best_gain[0]:
            best_gain = (gain, v)
    best_path = (0, ["<>"] * timer)
    for g in gains:
        if g[0] < best_gain[0]/2:
            continue
        new_path = find_best_move4(valves,valves[g[1]],g[2],avail - set([g[1]]))
        if new_path[0] + g[0] > best_path[0]:
            best_path = (new_path[0] + g[0], find_path(valves,frv,valves[g[1]]) + ["<open>"] + new_path[1])
    #print(f"{timer=},{best_path=}")
    return best_path

def find_best_move5(valves,mfrv,efrv,mtimer,etimer,avail=None):
    if avail is None:
        avail = set(valves)
    mgains = [(0, None, mtimer)]
    egains = [(0, None, etimer)]
    best_mgain = (0, None)
    best_egain = (0, None)
    for v in avail:
        if valves[v].flow == 0:
            continue
        mpath = find_path(valves,mfrv,valves[v])
        epath = find_path(valves,efrv,valves[v])
        new_mtimer = ((mtimer - 1) - len(mpath))
        new_etimer = ((etimer - 1) - len(epath))
        if new_mtimer > 0:
            mgain = valves[v].flow * new_mtimer
            mgains.append((mgain,v,new_mtimer))
            if mgain > best_mgain[0]:
                best_mgain = (mgain, v)
        if new_etimer > 0:
            egain = valves[v].flow * new_etimer
            egains.append((egain,v,new_etimer))
            if egain > best_egain[0]:
                best_egain = (egain, v)
    if len(mgains) == 1 and len(egains) == 1:
        return (0, [])
    best_path = (0, [])
    for mg in mgains:
        if mg[0] < best_mgain[0]/2:
            continue
        for eg in egains:
            if eg[0] < best_egain[0]/2:
                continue
            if eg[1] == mg[1]:
                continue
            new_avail = avail.copy()
            mv = mg[1]
            ev = eg[1]
            if mg[1] is not None:
                new_avail = new_avail - set([mg[1]])
            else:
                mv = mfrv.name
            if eg[1] is not None:
                new_avail = new_avail - set([eg[1]])
            else:
                ev = efrv.name
            gain = mg[0] + eg[0]
            new_path = find_best_move5(valves,valves[mv],valves[ev],mg[2],eg[2],new_avail)
            if new_path[0] + gain > best_path[0]:
                best_path = (new_path[0] + gain, [(mg[1],eg[1])] + new_path[1])
    #print(f"{timer=},{best_path=}")
    return best_path

def convert_to_schedule(valves, mstart, estart, timer, vschedule):
    mpath = []
    epath = []
    mv = mstart
    ev = estart
    for v in vschedule:
        if v[0] is not None:
            mpath.extend(find_path(valves,valves[mv],valves[v[0]]) + ["<open>"])
            mv = v[0]
        if v[1] is not None:
            epath.extend(find_path(valves,valves[ev],valves[v[1]]) + ["<open>"])
            ev = v[1]
    while len(mpath) < timer:
        mpath.append("<>")
    while len(epath) < timer:
        epath.append("<>")
    schedule = []
    for i in range(timer):
        schedule.append((mpath[i],epath[i]))
    return schedule

def print_schedule(sch):
    timer = len(sch)
    open_valves = []
    mlocation = None
    elocation = None
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
        if type(act) == tuple:
            act1, act2 = act
        else:
            act1 = act
            act2 = None
        if act1 == "<open>":
            print("You open valve {}.".format(mlocation.name))
            open_valves.append(mlocation)
            open_valves.sort(key=lambda x: x.name)
        elif type(act1) is Valve:
            print("You move to valve {}.".format(act1.name))
            mlocation = act1
        if act2 == "<open>":
            print("The elephant opens valve {}.".format(elocation.name))
            open_valves.append(elocation)
            open_valves.sort(key=lambda x: x.name)
        elif type(act2) is Valve:
            print("The elephant moves to valve {}.".format(act2.name))
            elocation = act2
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
    #schedule, pressure = find_best_move(valves,valves['AA'],30)
    pressure, schedule = find_best_move4(valves,valves['AA'],30)
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
    timer = 26
    pressure, vschedule = find_best_move5(valves,valves['AA'],valves['AA'],timer,timer)
    if AoC.TEST or True:
        schedule = convert_to_schedule(valves,'AA','AA',timer,vschedule)
        print_schedule(schedule)
    print("The total released pressure is: {}".format(pressure))

def main():
    AoC.set_day("16")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("--- Part 1 ---")
    part1(inp)
    print("--- Part 2 ---")
    part2(inp)

if __name__ == "__main__":
    main()
