#!/usr/bin/python3

import AoC
from collections import namedtuple

Point = namedtuple("Point", ["x","y"])

class Sensor:
    def __init__(self,pos,beacon):
        self.pos = pos
        self.beacon = beacon
        self.dist = abs(beacon.x - pos.x) + abs(beacon.y - pos.y)
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

def part1(inp):
    ln = 1
    sensors = []
    for line in inp.splitlines():
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
    if AoC.TEST:
        for s in sensors:
            print(s)

    if AoC.TEST:
        scanned_x = scan_yline(sensors,10)
        print(scanned_x)
    else:
        scanned_x = scan_line(sensors,2000000)
    print("There are {} positions where a beacon cannot be present".format(len(scanned_x)))

def part2(inp):
    pass

def main():
    AoC.set_day("15")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("== Part 1 ==")
    part1(inp)
    print("== Part 2 ==")
    part2(inp)

if __name__ == "__main__":
    main()
