#!/usr/bin/python3

import AoC

def print_mat(m):
    M = 1
    for row in m:
        for el in row:
            if M < len(str(el)):
                M = len(str(el))
    for row in m:
        if M == 1:
            print("".join([str(x) for x in row]))
        else:
            print(" ".join([("{: >"+str(M)+"}").format(x) for x in row]))

def calc_vis(trees,r,c):
    if r == 0 or c == 0 or r == len(trees)-1 or c == len(trees[r])-1:
        return 'V'
    row = trees[r]
    if max(row[:c]) < row[c] or max(row[c+1:]) < row[c]:
        return 'V'
    col = [row[c] for row in trees]
    if max(col[:r]) < col[r] or max(col[r+1:]) < col[r]:
            return 'V'
    return 'N'

def calc_view_score(trees,r,c):
    if r == 0 or c == 0 or r == len(trees)-1 or c == len(trees[r])-1:
        return 0
    h = trees[r][c]
    scores = []
    prod = 1

    row = trees[r]
    col = [row[c] for row in trees]

    left = row[c-1::-1]
    up = col[r-1::-1]
    right = row[c+1:]
    down = col[r+1:]
    for d in (left,up,right,down):
        s = 0
        for th in d:
            s += 1
            if th >= h:
                break
        scores.append(s)
        prod *= s
    AoC.tprint(scores)
    return prod

def parse_trees(inp):
    trees = []
    for line in inp.splitlines():
        line = line.strip()
        row = []
        for c in line:
            row.append(int(c))
        trees.append(row)
    return trees

def part1(inp):
    trees = parse_trees(inp)
    visibility = []
    total_vis = 0
    for i in range(len(trees)):
        row = []
        for j in range(len(trees[i])):
            v = calc_vis(trees,i,j)
            row.append(v)
            if v == 'V':
                total_vis += 1
        visibility.append(row)
    if AoC.TEST:
        print_mat(trees)
        print("-----")
        print_mat(visibility)
    print("Total number of visible trees is: {}".format(total_vis))

def part2(inp):
    trees = parse_trees(inp)
    view_scores = []
    best_vs = 0
    for i in range(len(trees)):
        row = []
        for j in range(len(trees[i])):
            vs = calc_view_score(trees,i,j)
            row.append(vs)
            if vs > best_vs:
                best_vs = vs
        view_scores.append(row)
    if AoC.TEST:
        print_mat(trees)
        print("-----")
        print_mat(view_scores)
    print("Best view score is: {}".format(best_vs))

def main():
    AoC.parse_args()
    inp = AoC.get_input("8")
    print("--- Part 1 ---")
    part1(inp)
    print("--- Part 2 ---")
    part2(inp)

if __name__ == "__main__":
    main()
