#!/usr/bin/python3

import AoC

def cube_to_index(c,m,M):
    rng = tuple((M[i] - m[i])+1 for i in range(len(c)))
    rx = c[0] - m[0]
    ry = c[1] - m[1]
    rz = c[2] - m[2]
    return rx + ry*rng[0] + rz*rng[0]*rng[1]

def index_to_cube(ind,m,M):
    rng = tuple((M[i] - m[i])+1 for i in range(len(m)))
    rz = ind // (rng[0] * rng[1])
    ry = (ind - rz * rng[0] * rng[1]) // rng[0]
    rx = ind - (rz * rng[0] * rng[1] + ry * rng[0])
    return (rx + m[0],ry + m[1],rz + m[2])

def out_of_bounds(scene,coord):
    _, mins, maxs = scene
    for d in range(3):
        if coord[d] < mins[d] or coord[d] > maxs[d]:
            return True
    return False

def fill(scene,startp,val):
    units, mins, maxs = scene
    search = [startp]
    while search:
        c = search.pop(0)
        if out_of_bounds(scene,c):
            continue
        i = cube_to_index(c,mins,maxs)
        if units[i] != 0:
            continue
        units[i] = val
        search.append((c[0]-1,c[1],c[2]))
        search.append((c[0]+1,c[1],c[2]))
        search.append((c[0],c[1]-1,c[2]))
        search.append((c[0],c[1]+1,c[2]))
        search.append((c[0],c[1],c[2]-1))
        search.append((c[0],c[1],c[2]+1))

def parse_scene(txt):
    cubes = []
    units = []
    mins = None
    maxs = None
    for line in txt.splitlines():
        line = line.strip()
        cube = tuple(int(n) for n in line.split(","))
        if len(cube) != 3:
            print("ERROR: Invalid cube dimension: {}. Cube: {}".format(cube.length,cube))
        cubes.append(tuple(int(n) for n in line.split(",")))
        if mins == None:
            mins = list(cube)
        else:
            for i in range(3):
                if cube[i] < mins[i]:
                    mins[i] = cube[i]
        if maxs == None:
            maxs = list(cube)
        else:
            for i in range(3):
                if cube[i] > maxs[i]:
                    maxs[i] = cube[i]
    for d in range(3):
        mins[d] -= 1
        maxs[d] += 1

    for i in range(mins[0],maxs[0]+1):
        for j in range(mins[1],maxs[1]+1):
            for k in range(mins[2],maxs[2]+1):
                units.append(0)

    for cube in cubes:
        i = cube_to_index(cube,mins,maxs)
        units[i] = 1
    fill((units,mins,maxs),mins,-1)
    return units, mins, maxs

def count_sides(cube,scene):
    """check for adjacent cubes, and remove a side for each one"""
    units, mins, maxs = scene
    nsides = 6
    check = [ 
            (cube[0]-1,cube[1],cube[2]),
            (cube[0]+1,cube[1],cube[2]),
            (cube[0],cube[1]-1,cube[2]),
            (cube[0],cube[1]+1,cube[2]),
            (cube[0],cube[1],cube[2]-1),
            (cube[0],cube[1],cube[2]+1)
            ]
    for c2 in check:
        if out_of_bounds(scene,c2):
            continue
        j = cube_to_index(c2,mins,maxs)
        if j < 0 or j >= len(units):
            continue
        if units[j] == 1:
            nsides -= 1
    return nsides

def part1(inp):
    scene = parse_scene(inp)
    units, mins, maxs = scene
    sides = []
    for i in range(len(units)):
        if units[i] == 1:
            # check for adjacent cubes, and remove a side for each one
            c = index_to_cube(i,mins,maxs)
            nsides = count_sides(c,scene)
            AoC.tprint("Cube {} sides: {}".format(c,nsides))
            sides.append(nsides)
    print("Total unconnected sides: {}".format(sum(sides)))

def part2(inp):
    scene = parse_scene(inp)
    units, mins, maxs = scene
    sides = []
    for i in range(len(units)):
        if units[i] == 1:
            c = index_to_cube(i,mins,maxs)
            nsides = count_sides(c,scene)
            AoC.tprint("Cube {} sides: {}".format(c,nsides))
            sides.append(nsides)
        elif units[i] == 0:
            c = index_to_cube(i,mins,maxs)
            AoC.tprint("Bubble at {}".format(c))
            nsides = count_sides(c,scene) - 6
            sides.append(nsides)
            
    print("Total unconnected sides: {}".format(sum(sides)))

def main():
    AoC.set_day("18")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("== Part 1 ==")
    part1(inp)
    print("== Part 2 ==")
    part2(inp)

if __name__ == "__main__":
    main()
