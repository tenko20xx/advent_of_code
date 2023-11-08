#!/usr/bin/python3

import re
import AoC

class Blueprint:
    def __init__(self,name):
        self.name = name
        self.ore_cost = (0,0,0)
        self.clay_cost = (0,0,0)
        self.obsidian_cost = (0,0,0)
        self.geode_cost = (0,0,0)
        self.demand = (0,0,0)
    def set_robot_cost(self,robot,ore=0,clay=0,obsidian=0):
        cost = (ore,clay,obsidian)
        if robot == "ore":
            self.ore_cost = cost
        elif robot == "clay":
            self.clay_cost = cost
        elif robot == "obsidian":
            self.obsidian_cost = cost
        elif robot == "geode":
            self.geode_cost = cost
        else:
            raise ValueError("Invalid robot type: {}".format(robot))
        demand = (0,0,0)
        for c in [self.ore_cost, self.clay_cost, self.obsidian_cost, self.geode_cost, self.geode_cost]:
            demand = (demand[0] + c[0], demand[1] + c[1], demand[2] + c[2])
        self.demand = demand
    
    def can_afford_robot(self,robot,mats):
        ore, clay, obs = mats
        if robot == "ore":
            cost = self.ore_cost
        elif robot == "clay":
            cost = self.clay_cost
        elif robot == "obsidian":
            cost = self.obsidian_cost
        elif robot == "geode":
            cost = self.geode_cost
        else:
            raise ValueError("Invalid robot type: {}".format(robot))
        return all(mats[n] >= cost[n] for n in range(len(cost))) > 0

    def score_inv(self,inv):
        return (min(self.geode_cost[0],inv[0]) / self.geode_cost[2]) + (min(self.geode_cost[2],inv[2]) / self.geode_cost[0])
        #sd = sum(self.demand)
        #return sum(inv[n] * (self.demand[n] / sd) for n in range(len(inv)))

    def __repr__(self):
        s = f"Blueprint{self.name}<ore:{self.ore_cost},clay:{self.clay_cost},obsidian:{self.obsidian_cost},geode:{self.geode_cost}>"
        return s
    def __str__(self):
        s = f"Blueprint {self.name}:\n"
        s += f"  Ore robot costs:      {self.ore_cost[0]: 2} ore, {self.ore_cost[1]: 2} clay and {self.ore_cost[2]: 2} obsidian\n"
        s += f"  Clay robot costs:     {self.clay_cost[0]: 2} ore, {self.clay_cost[1]: 2} clay and {self.clay_cost[2]: 2} obsidian\n"
        s += f"  Obsidian robot costs: {self.obsidian_cost[0]: 2} ore, {self.obsidian_cost[1]: 2} clay and {self.obsidian_cost[2]: 2} obsidian\n"
        s += f"  Geode robot costs:    {self.geode_cost[0]: 2} ore, {self.geode_cost[1]: 2} clay and {self.geode_cost[2]: 2} obsidian\n"
        return s

bp_re_prog = None
def read_blueprints(txt):
    global bp_re_prog
    blueprints = {}
    if bp_re_prog is None:
        bp_re_prog = re.compile("^Blueprint (\d+): *Each ore robot costs (\d+) ore. *Each clay robot costs (\d+) ore. *Each obsidian robot costs (\d+) ore and (\d+) clay. *Each geode robot costs (\d+) ore and (\d+) obsidian.$")
    for line in txt.splitlines():
        line = line.strip()
        prop = bp_re_prog.match(line).groups()
        if prop[0] in blueprints:
            raise Exception("Blueprint {} is already defined".format(prop[0]))
        bp = Blueprint(int(prop[0]))
        bp.set_robot_cost("ore",ore=int(prop[1]))
        bp.set_robot_cost("clay",ore=int(prop[2]))
        bp.set_robot_cost("obsidian",ore=int(prop[3]),clay=int(prop[4]))
        bp.set_robot_cost("geode",ore=int(prop[5]),obsidian=int(prop[6]))
        blueprints[int(prop[0])] = bp
    return blueprints

def count_possibilities(blueprint,timer,robots=(1,0,0,0),inv=(0,0,0)):
    bp = blueprint
    if timer <= 0:
        return 1
    p = 0
    if blueprint.can_afford_robot("geode",inv):
        trobots = (robots[0],robots[1],robots[2],robots[3]+1)
        tinv = tuple(inv[n] - bp.geode_cost[n] for n in range(len(inv)))
        tinv = tuple(inv[n] + robots[n] for n in range(len(inv)))
        p = count_possibilities(blueprint,timer-1,trobots,tinv)
    if blueprint.can_afford_robot("obsidian",inv):
        trobots = (robots[0],robots[1],robots[2]+1,robots[3])
        tinv = tuple(inv[n] - bp.obsidian_cost[n] for n in range(len(inv)))
        tinv = tuple(inv[n] + robots[n] for n in range(len(inv)))
        p = count_possibilities(blueprint,timer-1,trobots,tinv)
    if blueprint.can_afford_robot("clay",inv):
        trobots = (robots[0],robots[1]+1,robots[2],robots[3])
        tinv = tuple(inv[n] - bp.clay_cost[n] for n in range(len(inv)))
        tinv = tuple(inv[n] + robots[n] for n in range(len(inv)))
        p = count_possibilities(blueprint,timer-1,trobots,tinv)
    if blueprint.can_afford_robot("ore",inv):
        trobots = (robots[0]+1,robots[1],robots[2],robots[3])
        tinv = tuple(inv[n] - bp.obsidian_cost[n] for n in range(len(inv)))
        tinv = tuple(inv[n] + robots[n] for n in range(len(inv)))
        p = count_possibilities(blueprint,timer-1,trobots,tinv)
    inv = tuple(inv[n] + robots[n] for n in range(len(inv)))
    p += count_possibilities(blueprint,timer-1,robots,inv)
    return p

blueprint_cache = None
active_policies = {}
def find_optimal_policy(blueprint,timer,robots=(1,0,0,0),inv=(0,0,0),geodes=0):
    global blueprint_cache, active_policies
    if blueprint != blueprint_cache:
        blueprint_cache = blueprint
        active_policies = {}
    key = (timer,robots)
    if key in active_policies:
        this_score = blueprint.score_inv(inv)
        active_score = blueprint.score_inv(active_policies[key])
        if this_score > active_score:
            #print(f"{timer}:this score is better than the active policy ({inv}:{this_score} > {active_policies[key]}:{active_score})")
            active_policies.pop(key)
        else:
            #print(f"already got {(timer,robots,inv)}")
            return ([], -1)
    active_policies[key] = inv
    #print(f"fop({timer},{robots},{inv}):{geodes}")
    bp = blueprint
    if timer <= 0:
        return ([], geodes)
    try_policies = []
    geodes += robots[3]
    if blueprint.can_afford_robot("geode",inv):
        trobots = (robots[0],robots[1],robots[2],robots[3]+1)
        tinv = tuple(inv[n] - bp.geode_cost[n] for n in range(len(inv)))
        tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
        tpolicy = find_optimal_policy(blueprint,timer-1,trobots,tinv,geodes)
        try_policies.append((["geode"] + tpolicy[0],tpolicy[1]))
    if blueprint.can_afford_robot("obsidian",inv):
        trobots = (robots[0],robots[1],robots[2]+1,robots[3])
        tinv = tuple(inv[n] - bp.obsidian_cost[n] for n in range(len(inv)))
        tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
        tpolicy = find_optimal_policy(blueprint,timer-1,trobots,tinv,geodes)
        try_policies.append((["obsidian"] + tpolicy[0],tpolicy[1]))
        #try_policies.append(find_optimal_policy(blueprint,timer-1,trobots,tinv,geodes))
    if blueprint.can_afford_robot("clay",inv):
        trobots = (robots[0],robots[1]+1,robots[2],robots[3])
        tinv = tuple(inv[n] - bp.clay_cost[n] for n in range(len(inv)))
        tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
        tpolicy = find_optimal_policy(blueprint,timer-1,trobots,tinv,geodes)
        try_policies.append((["clay"] + tpolicy[0],tpolicy[1]))
        #try_policies.append(find_optimal_policy(blueprint,timer-1,trobots,tinv,geodes))
    if blueprint.can_afford_robot("ore",inv):
        trobots = (robots[0]+1,robots[1],robots[2],robots[3])
        tinv = tuple(inv[n] - bp.ore_cost[n] for n in range(len(inv)))
        tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
        tpolicy = find_optimal_policy(blueprint,timer-1,trobots,tinv,geodes)
        try_policies.append((["ore"] + tpolicy[0],tpolicy[1]))
        #try_policies.append(find_optimal_policy(blueprint,timer-1,trobots,tinv,geodes))
    inv = tuple(inv[n] + robots[n] for n in range(len(inv)))
    tpolicy = find_optimal_policy(blueprint,timer-1,robots,inv,geodes)
    try_policies.append(([None] + tpolicy[0],tpolicy[1]))
    p = ([None]*timer, 0)
    for tp in try_policies:
        if tp[1] > p[1]:
            p = tp
    return p

def find_optimal_policy2(blueprint,timer,robots=(1,0,0,0),inv=(0,0,0),geodes=0):
    #print(f"fop2({timer},{robots},{inv}):{geodes}")
    bp = blueprint
    best_policy = ([None] * timer, 0)
    search = [([],timer, robots, inv, geodes)]
    while search:
        p, t, r, i, g = search.pop(0)
        print(p,t,r,i,g)
        if t <= 0:
            if g > best_policy[1]:
                best_policy = (p, g)
                continue
        g += r[3]
        if blueprint.can_afford_robot("geode",i):
            trobots = (r[0],r[1],r[2],r[3]+1)
            tinv = tuple(i[n] - bp.geode_cost[n] for n in range(len(i)))
            tinv = tuple(tinv[n] + r[n] for n in range(len(i)))
            search = [(p + ["geode"], t - 1, trobots, tinv, g)]
            continue
        if blueprint.can_afford_robot("obsidian",i):
            trobots = (r[0],r[1],r[2]+1,r[3])
            tinv = tuple(i[n] - bp.obsidian_cost[n] for n in range(len(i)))
            tinv = tuple(tinv[n] + r[n] for n in range(len(i)))
            search.append((p + ["obsidian"], t - 1, trobots, tinv, g))
        if blueprint.can_afford_robot("clay",i):
            trobots = (r[0],r[1]+1,r[2],r[3])
            tinv = tuple(i[n] - bp.clay_cost[n] for n in range(len(i)))
            tinv = tuple(tinv[n] + r[n] for n in range(len(i)))
            search.append((p + ["clay"], t - 1, trobots, tinv, g))
        if blueprint.can_afford_robot("ore",i):
            trobots = (r[0]+1,r[1],r[2],r[3])
            tinv = tuple(i[n] - bp.ore_cost[n] for n in range(len(i)))
            tinv = tuple(tinv[n] + r[n] for n in range(len(i)))
            search.append((p + ["ore"], t - 1, trobots, tinv, g))
        i = tuple(i[n] + r[n] for n in range(len(i)))
        search.append((p + [None], t - 1, r, i, g))
    return best_policy 
    
def find_optimal_policy3(blueprint,timer,robots=(1,0,0,0),inv=(0,0,0),geodes=0):
    print(f"fop3({timer},{robots},{inv}):{geodes}")
    bp = blueprint
    if timer <= 0:
        return ([], (robots,inv,geodes))
    try_policies = []
    geodes += robots[3]
    if blueprint.can_afford_robot("geode",inv):
        trobots = (robots[0],robots[1],robots[2],robots[3]+1)
        tinv = tuple(inv[n] - bp.geode_cost[n] for n in range(len(inv)))
        tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
        return (["geode"],(trobots,inv,geodes))
    if blueprint.can_afford_robot("obsidian",inv):
        trobots = (robots[0],robots[1],robots[2]+1,robots[3])
        tinv = tuple(inv[n] - bp.obsidian_cost[n] for n in range(len(inv)))
        tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
        tpolicy = find_optimal_policy3(blueprint,timer-1,trobots,tinv,geodes)
        try_policies.append((["obsidian"] + tpolicy[0],tpolicy[1]))
        #try_policies.append(find_optimal_policy(blueprint,timer-1,trobots,tinv,geodes))
    if blueprint.can_afford_robot("clay",inv):
        trobots = (robots[0],robots[1]+1,robots[2],robots[3])
        tinv = tuple(inv[n] - bp.clay_cost[n] for n in range(len(inv)))
        tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
        tpolicy = find_optimal_policy3(blueprint,timer-1,trobots,tinv,geodes)
        try_policies.append((["clay"] + tpolicy[0],tpolicy[1]))
        #try_policies.append(find_optimal_policy(blueprint,timer-1,trobots,tinv,geodes))
    if blueprint.can_afford_robot("ore",inv):
        trobots = (robots[0]+1,robots[1],robots[2],robots[3])
        tinv = tuple(inv[n] - bp.ore_cost[n] for n in range(len(inv)))
        tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
        tpolicy = find_optimal_policy3(blueprint,timer-1,trobots,tinv,geodes)
        try_policies.append((["ore"] + tpolicy[0],tpolicy[1]))
        #try_policies.append(find_optimal_policy(blueprint,timer-1,trobots,tinv,geodes))
    inv = tuple(inv[n] + robots[n] for n in range(len(inv)))
    tpolicy = find_optimal_policy3(blueprint,timer-1,robots,inv,geodes)
    try_policies.append(([None] + tpolicy[0],tpolicy[1]))
    p = ([None]*timer, (robots,inv,geodes))
    for tp in try_policies:
        if len(tp[0]) > len(p[0]):
            p = tp
        elif len(tp[0]) == len(p[0]) and tp[1][2] > p[1][2]:
            p = tp
    rem = find_optimal_policy3(bp, timer - len(p[0]), p[1][0], p[1][1], p[1][2])
    return (p[0] + rem[0], rem[1])

def find_optimal_policy4(blueprint,timer,robots=(1,0,0,0),inv=(0,0,0)):
    # not crazy about this solution, but it gets the job done (eventually)
    #print(f"fop4({timer},{robots},{inv})")
    bp = blueprint
    if timer <= 0:
        return ([], 0)
    geodes = robots[3]
    best_policy = ([None]*timer, geodes * timer)
    can_buy_ore = all(bp.ore_cost[n] == 0 or robots[n] > 0 for n in range(len(inv)))
    can_buy_clay = all(bp.clay_cost[n] == 0 or robots[n] > 0 for n in range(len(inv)))
    can_buy_obsidian = all(bp.obsidian_cost[n] == 0 or robots[n] > 0 for n in range(len(inv)))
    can_buy_geode = all(bp.geode_cost[n] == 0 or robots[n] > 0 for n in range(len(inv)))
    max_ore = max(c[0] for c in (bp.ore_cost, bp.clay_cost, bp.obsidian_cost, bp.geode_cost))
    max_clay = max(c[1] for c in (bp.ore_cost, bp.clay_cost, bp.obsidian_cost, bp.geode_cost))
    max_obsidian = max(c[2] for c in (bp.ore_cost, bp.clay_cost, bp.obsidian_cost, bp.geode_cost))
    if can_buy_ore and (robots[0]) <= (max_ore/2)+1:
        ticks = 1
        tinv = inv
        while not bp.can_afford_robot("ore",tinv):
            ticks += 1
            tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
        if timer - ticks > 0:
            trobots = (robots[0]+1,robots[1],robots[2],robots[3])
            tinv = tuple(tinv[n] - bp.ore_cost[n] for n in range(len(inv)))
            tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
            tpolicy = find_optimal_policy4(blueprint,timer-ticks,trobots,tinv)
            new_geodes = geodes * ticks + tpolicy[1]
            if new_geodes > best_policy[1]:
                best_policy = ([None] * (ticks-1) + ["ore"] + tpolicy[0], new_geodes)
    if can_buy_clay and (robots[1]) <= (max_clay/2)+1:
        ticks = 1
        tinv = inv
        while not bp.can_afford_robot("clay",tinv):
            ticks += 1
            tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
        if timer - ticks > 0:
            trobots = (robots[0],robots[1]+1,robots[2],robots[3])
            tinv = tuple(tinv[n] - bp.clay_cost[n] for n in range(len(inv)))
            tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
            tpolicy = find_optimal_policy4(blueprint,timer-ticks,trobots,tinv)
            new_geodes = geodes * ticks + tpolicy[1]
            if new_geodes > best_policy[1]:
                best_policy = ([None] * (ticks-1) + ["clay"] + tpolicy[0], new_geodes)
    if can_buy_obsidian and (robots[2]) < max_obsidian:
        ticks = 1
        tinv = inv
        while not bp.can_afford_robot("obsidian",tinv):
            ticks += 1
            tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
        if timer - ticks > 0:
            trobots = (robots[0],robots[1],robots[2]+1,robots[3])
            tinv = tuple(tinv[n] - bp.obsidian_cost[n] for n in range(len(inv)))
            tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
            tpolicy = find_optimal_policy4(blueprint,timer-ticks,trobots,tinv)
            new_geodes = geodes * ticks + tpolicy[1]
            if new_geodes > best_policy[1]:
                best_policy = ([None] * (ticks-1) + ["obsidian"] + tpolicy[0], new_geodes)
    if can_buy_geode:
        ticks = 1
        tinv = inv
        while not bp.can_afford_robot("geode",tinv):
            ticks += 1
            tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
        if timer - ticks > 0:
            trobots = (robots[0],robots[1],robots[2],robots[3]+1)
            tinv = tuple(tinv[n] - bp.geode_cost[n] for n in range(len(inv)))
            tinv = tuple(tinv[n] + robots[n] for n in range(len(inv)))
            tpolicy = find_optimal_policy4(blueprint,timer-ticks,trobots,tinv)
            new_geodes = geodes * ticks + tpolicy[1]
            if new_geodes > best_policy[1]:
                best_policy = ([None] * (ticks-1) + ["geode"] + tpolicy[0], new_geodes)
    return best_policy

def repr_cost(cost):
    l = []
    if cost[0] > 0:
        l.append(f"{cost[0]} ore")
    if cost[1] > 0:
        l.append(f"{cost[1]} clay")
    if cost[2] > 0:
        l.append(f"{cost[2]} obsidian")
    if len(l) == 0:
        return "nothing"
    elif len(l) == 1:
        return l[0]
    return ", ".join(l[:-1]) + " and " + l[-1]

def run_policy(bp,policy):
    geodes = 0
    robots = (1,0,0,0)
    inv = (0,0,0)
    minute = 1
    while minute <= len(policy):
        AoC.tprint(f"== Minute {minute} ==")
        new_robots = (0,0,0,0)
        action = policy[minute-1]
        if action == "geode":
            if bp.can_afford_robot("geode",inv):
                new_robots = (new_robots[0],new_robots[1],new_robots[2],new_robots[3]+1)
                inv = tuple(inv[n] - bp.geode_cost[n] for n in range(len(inv)))
                AoC.tprint(f"Spend {repr_cost(bp.geode_cost)} to start building a geode-cracking robot.")
            else:
                raise Exception("Cannot afford geode right now")
        elif action == "obsidian":
            if bp.can_afford_robot("obsidian",inv):
                new_robots = (new_robots[0],new_robots[1],new_robots[2]+1,new_robots[3])
                inv = tuple(inv[n] - bp.obsidian_cost[n] for n in range(len(inv)))
                AoC.tprint(f"Spend {repr_cost(bp.obsidian_cost)} to start building a obsidian-collecting robot.")
            else:
                raise Exception("Cannot afford obsidian right now")
        elif action == "clay":
            if bp.can_afford_robot("clay",inv):
                new_robots = (new_robots[0],new_robots[1]+1,new_robots[2],new_robots[3])
                inv = tuple(inv[n] - bp.clay_cost[n] for n in range(len(inv)))
                AoC.tprint(f"Spend {repr_cost(bp.clay_cost)} to start building a clay-collecting robot.")
            else:
                raise Exception("Cannot afford clay right now")
        elif action == "ore":
            if bp.can_afford_robot("ore",inv):
                new_robots = (new_robots[0]+1,new_robots[1],new_robots[2],new_robots[3])
                inv = tuple(inv[n] - bp.ore_cost[n] for n in range(len(inv)))
                AoC.tprint(f"Spend {repr_cost(bp.ore_cost)} to start building a ore-collecting robot.")
            else:
                raise Exception("Cannot afford ore right now")
        elif action is not None:
            raise Exception(f"Unknown action: {action}")
        
        inv = (inv[0] + robots[0], inv[1] + robots[1], inv[2] + robots[2])

        if robots[0] > 0:
            AoC.tprint(f"{robots[0]} ore-collecting robot{'s' if robots[0] > 1 else ''} collects {robots[0]} ore; you now have {inv[0]} ore.")
        if robots[1] > 0:
            AoC.tprint(f"{robots[1]} clay-collecting robot{'s' if robots[1] > 1 else ''} collects {robots[1]} clay; you now have {inv[1]} clay.")
        if robots[2] > 0:
            AoC.tprint(f"{robots[2]} obsidian-collecting robot{'s' if robots[2] > 1 else ''} collects {robots[2]} obsidian; you now have {inv[2]} obsidian.")
        geodes += robots[3]
        if robots[3] > 0:
            AoC.tprint(f"{robots[3]} geode-cracking robot{'s' if robots[3] > 1 else ''} cracks {robots[3]} geode{'s' if robots[3] > 1 else ''}; you now have {geodes} open geode{'s' if robots[3] > 1 else ''}.")
        
        minute += 1
        
        if new_robots[0] > 0:
            robots = (robots[0] + new_robots[0], robots[1], robots[2], robots[3])
            AoC.tprint(f"The new ore-collecting robot{'s are' if new_robots[0] > 1 else ' is'} ready; you now have {robots[0]} of them.")
        if new_robots[1] > 0:
            robots = (robots[0], robots[1] + new_robots[1], robots[2], robots[3])
            AoC.tprint(f"The new clay-collecting robot{'s are' if new_robots[1] > 1 else ' is'} ready; you now have {robots[1]} of them.")
        if new_robots[2] > 0:
            robots = (robots[0], robots[1], robots[2] + new_robots[2], robots[3])
            AoC.tprint(f"The new obsidian-collecting robot{'s are' if new_robots[2] > 1 else ' is'} ready; you now have {robots[2]} of them.")
        if new_robots[3] > 0:
            robots = (robots[0], robots[1], robots[2], robots[3] + new_robots[3])
            AoC.tprint(f"The new geode-cracking robot{'s are' if new_robots[3] > 1 else ' is'} ready; you now have {robots[3]} of them.")
        AoC.tprint("")
    return geodes

def manual_policy(bp,timer):
    geodes = 0
    robots = (1,0,0,0)
    inv = (0,0,0)
    minute = 1
    while timer > 0:
        AoC.tprint(f"== Minute {minute} ==")
        new_robots = (0,0,0,0)
        while bp.can_afford_robot("geode",inv):
            print(inv)
            new_robots = (new_robots[0],new_robots[1],new_robots[2],new_robots[3]+1)
            inv = tuple(inv[n] - bp.geode_cost[n] for n in range(len(inv)))
            AoC.tprint(f"Spend {repr_cost(bp.geode_cost)} to start building a geode-cracking robot.")
        while bp.can_afford_robot("obsidian",inv):
            new_robots = (new_robots[0],new_robots[1],new_robots[2]+1,new_robots[3])
            inv = tuple(inv[n] - bp.obsidian_cost[n] for n in range(len(inv)))
            AoC.tprint(f"Spend {repr_cost(bp.obsidian_cost)} to start building a obsidian-collecting robot.")
        while bp.can_afford_robot("clay",inv):
            new_robots = (new_robots[0],new_robots[1]+1,new_robots[2],new_robots[3])
            inv = tuple(inv[n] - bp.clay_cost[n] for n in range(len(inv)))
            AoC.tprint(f"Spend {repr_cost(bp.clay_cost)} to start building a clay-collecting robot.")
        while bp.can_afford_robot("ore",inv):
            new_robots = (new_robots[0]+1,new_robots[1],new_robots[2],new_robots[3])
            inv = tuple(inv[n] - bp.ore_cost[n] for n in range(len(inv)))
            AoC.tprint(f"Spend {repr_cost(bp.ore_cost)} to start building a ore-collecting robot.")
        inv = (inv[0] + robots[0], inv[1] + robots[1], inv[2] + robots[2])
        if robots[0] > 0:
            AoC.tprint(f"{robots[0]} ore-collecting robot{'s' if robots[0] > 1 else ''} collects {robots[0]} ore; you now have {inv[0]} ore.")
        if robots[1] > 0:
            AoC.tprint(f"{robots[1]} clay-collecting robot{'s' if robots[1] > 1 else ''} collects {robots[1]} clay; you now have {inv[1]} clay.")
        if robots[2] > 0:
            AoC.tprint(f"{robots[2]} obsidian-collecting robot{'s' if robots[2] > 1 else ''} collects {robots[2]} obsidian; you now have {inv[2]} obsidian.")
        geodes += robots[3]
        if robots[3] > 0:
            AoC.tprint(f"{robots[3]} geode-cracking robot{'s' if robots[3] > 1 else ''} cracks {robots[3]} geode{'s' if robots[3] > 1 else ''}; you now have {geodes} open geode{'s' if robots[3] > 1 else ''}.")
        minute += 1
        timer -= 1
        if new_robots[0] > 0:
            robots = (robots[0] + new_robots[0], robots[1], robots[2], robots[3])
            AoC.tprint(f"The new ore-collecting robot{'s are' if new_robots[0] > 1 else ' is'} ready. you now have {robots[0]} of them.")
        if new_robots[1] > 0:
            robots = (robots[0], robots[1] + new_robots[1], robots[2], robots[3])
            AoC.tprint(f"The new clay-collecting robot{'s are' if new_robots[1] > 1 else ' is'} ready. you now have {robots[1]} of them.")
        if new_robots[2] > 0:
            robots = (robots[0], robots[1], robots[2] + new_robots[2], robots[3])
            AoC.tprint(f"The new obsidian-collecting robot{'s are' if new_robots[2] > 1 else ' is'} ready. you now have {robots[2]} of them.")
        if new_robots[3] > 0:
            robots = (robots[0], robots[1], robots[2], robots[3] + new_robots[3])
            AoC.tprint(f"The new geode-cracking robot{'s are' if new_robots[3] > 1 else ' is'} ready. you now have {robots[3]} of them.")
        AoC.tprint("")
    return geodes
        
def part1(inp):
    blueprints = read_blueprints(inp)
    #print(blueprints)
    #print(count_possibilities(blueprints["1"],5))
    s = 0
    for bp in blueprints:
        optimal_policy = find_optimal_policy4(blueprints[bp],24)
        #print(optimal_policy)
        s += bp * optimal_policy[1]
        if AoC.TEST:
            print(f"** Blueprint {bp} **")
            run_policy(blueprints[bp],optimal_policy[0])
    print(f"Sum of quality level of each blueprint is: {s}")

def part2(inp):
    blueprints = read_blueprints(inp)
    #print(blueprints)
    #print(count_possibilities(blueprints["1"],5))
    p = 1
    for bpi in range(3):
        if bpi >= len(blueprints):
            break
        bp = bpi+1
        optimal_policy = find_optimal_policy4(blueprints[bp],32)
        #print(optimal_policy)
        p *= optimal_policy[1]
        if AoC.TEST:
            print(f"** Blueprint {bp} **")
            run_policy(blueprints[bp],optimal_policy[0])
    print(f"Product of each blueprint collection is: {p}")

def main():
    AoC.set_day("19")
    args = AoC.parse_args()

    inp = AoC.get_input()
    if AoC.exec_part1:
        print("--- Part 1 ---")
        part1(inp)
    if AoC.exec_part2:
        print("--- Part 2 ---")
        part2(inp)

if __name__ == "__main__":
    main()
