#!/usr/bin/python3

import heapq

import AoC
from collections import namedtuple

Point = namedtuple("Point", ["x","y"])

def mdist(a,b):
    return abs(a.x - b.x) + abs(a.y - b.y)

class Sensor:
    def __init__(self,pos,beacon):
        self.pos = pos
        self.beacon = beacon
        self.dist = mdist(beacon, pos)
    def get_bdist(self):
        return self.dist
    def __str__(self):
        s = "Sensor<{},{}>".format(self.pos.x,self.pos.y)
        s = s + " -> Beacon<{},{}>".format(self.beacon.x,self.beacon.y)
        s = s + " (MD: {})".format(self.dist)
        return s

def parse_coords(txt):
    parts = tuple(p.strip() for p in txt.split(","))
    if not parts[0].startswith("x="):
        raise Exception("Cannot find x coordinate in text: {}".format(txt))
    if not parts[1].startswith("y="):
        raise Exception("Cannot find y coordinate in text: {}".format(txt))
    x = int(parts[0][2:])
    y = int(parts[1][2:])
    return Point(x,y)

def scan_xline(sensors,x):
    scanned = set()
    beacons = set(list(s.beacon.x for s in sensors if s.beacon.y == y))
    for s in sensors:
        d = s.dist - abs(y - s.pos.y)
        for x in range(s.pos.x-d,s.pos.x+d+1):
            scanned.add(x)
    return scanned.difference(beacons)

def scan_line(sensors,y):
    scanned = set()
    beacons = set(list(s.beacon.x for s in sensors if s.beacon.y == y))
    for s in sensors:
        d = s.dist - abs(y - s.pos.y)
        for x in range(s.pos.x-d,s.pos.x+d+1):
            scanned.add(x)
    return scanned.difference(beacons)

def merge_ranges(ranges):
    ranges = sorted(ranges,key=lambda x: x[0])
    i = 0
    while i < len(ranges)-1:
        m1,M1 = ranges[i]
        m2,M2 = ranges[i+1]
        if m2 <= (M1+1):
            if M2 > M1:
                ranges[i] = (m1,M2)
            ranges.pop(i+1)
        else:
            i += 1
    return ranges

def get_scan_ranges_y(sensors,y):
    ranges = []
    for s in sensors:
        yoff = abs(s.pos.y - y)
        r = s.get_bdist() - yoff
        if r < 0:
            continue
        ranges.append((s.pos.x - r, s.pos.x + r))
    return merge_ranges(ranges)
        
def parse_sensors(lines):
    sensors = []
    for line in lines:
        line = line.strip()
        s,b = tuple(t.strip() for t in line.split(":"))
        if s.startswith("Sensor at "):
            sp = parse_coords(s[s.find("x="):])
        else:
            raise Exception("Unable to find sensor coordinates on line {}: {}".format(ln,line))
        if b.startswith("closest beacon is at "):
            bp = parse_coords(b[b.find("x="):])
        else:
            raise Exception("Unable to find beacon coordinates on line {}: {}".format(ln,line))
        sensors.append(Sensor(sp,bp))
    return sensors

def part1(inp):
    ln = 1
    sensors = parse_sensors(inp.splitlines())
    if AoC.TEST:
        for s in sensors:
            print(s)

    scan_y = 2000000
    if AoC.TEST:
        scan_y = 10
        #scanned_x = scan_line(sensors,10)
        #print(scanned_x)
        ranges = get_scan_ranges_y(sensors,scan_y)
        print(f"Ranges: {ranges}")
    else:
        #scanned_x = scan_line(sensors,2000000)
        ranges = get_scan_ranges_y(sensors,2000000)
        #print(ranges)

    total = sum((r[1]+1)-r[0] for r in ranges)
    beacons = set()
    for s in sensors:
        beacons.add(s.beacon)
    for b in beacons:
        if b.y == scan_y:
            total -= 1
    #print("There are {} positions where a beacon cannot be present".format(len(scanned_x)))
    print(f"There are {total} positions where a beacon cannot be present")

def part2(inp):
    minx = 0
    miny = 0
    maxx = 4000000
    maxy = 4000000
    if AoC.TEST:
        maxx = 20
        maxy = 20
    sensors = parse_sensors(inp.splitlines())
    meanx = sum(s.pos.x for s in sensors)/len(sensors)
    meany = sum(s.pos.y for s in sensors)/len(sensors)
    if AoC.TEST:
        print(f"mean: ({meanx},{meany})")
    try_lines = [int(meany)]
    solution_ranges = None
    while try_lines:
        line = try_lines.pop(0)
        if AoC.TEST:
            print(f"scanning line {line}")
        ranges = get_scan_ranges_y(sensors,line)
        if AoC.TEST:
            print(ranges)
        if len(ranges) == 1:
            if line <= int(meany) and line >= miny:
                try_lines.append(line-1)
            if line >= int(meany) and line <= maxy:
                try_lines.append(line+1)
        else:
            solution_ranges = (line,ranges)
            break
    if AoC.TEST:
        print(solution_ranges)
    r = solution_ranges[1]
    if r[1][0] - r[0][1] == 2:
        tfreq = (r[0][1] + 1) * 4000000 + solution_ranges[0]
        print(f"Distress beacon found at ({r[0][1]+1},{solution_ranges[0]})")
        print(f"The tuning frequency for this distress beacon is {tfreq}")
    else:
        print(f"Ambiguous gap found at y={solution_ranges[0]}")
        print(r)


def part2_bad1():
    tried = set()
    try_next = []
    #P = [Point((maxx-minx)//2,(maxy-miny)//2)]
    P = [Point(int(meanx),int(meany))]
    found = None
    while found is None:
        for p in P:
            print(p)
            tried.add(p)
            dists = [mdist(s.pos,p) for s in sensors]
            #deltas = [sensors[i].get_bdist() - dists[i] for i in range(len(dists))]
            deltas = [max(-1,sensors[i].get_bdist() - dists[i]) for i in range(len(dists))]
            s = sum(deltas)
            print(f"{sum(dists)}:{dists}")
            print(f"{s}:{deltas}")
            heapq.heappush(try_next, (s,p))
            if all(d < 0 for d in deltas):
                found = p
                break
        if found is not None:
            break
        P = []
        tn = heapq.heappop(try_next)[1]
        print(tn)
        for y in range(-1,2):
            for x in range(-1,2):
                if x == 0 and y == 0:
                    continue
                new_p = Point(tn.x + x, tn.y + y)
                if new_p in tried:
                    #print(f"already tried {new_p}")
                    continue
                if new_p.x >= minx and new_p.y >= miny and new_p.x <= maxx and new_p.y <= maxy:
                    P.append(new_p)


def main():
    AoC.set_day("15")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("--- Part 1 ---")
    part1(inp)
    print("--- Part 2 ---")
    part2(inp)

if __name__ == "__main__":
    main()
