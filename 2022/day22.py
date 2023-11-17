#!/usr/bin/python3

import AoC

class Map:
    def __init__(self):
        self.map_data = []
        self.col_start = []
        self.col_end = []
        self.row_start = []
        self.row_end = []
        self.max_col = 0
        self.is_cube = False
        self.faces = None
        self.face_length = None
        self.face_links = None
    def add_row(self,row):
        rownum = len(self.map_data)
        self.map_data.append(row)
        rs = 0
        while row[rs] == " " and rs < len(row)-1:
            rs += 1
        re = len(row)-1
        while row[re] == " " and re >= 1:
            re -= 1
        self.row_start.append(rs)
        self.row_end.append(re)
        for ci in range(len(row)):
            if row[ci] == " ":
                continue
            while ci >= len(self.col_start):
                self.col_start.append(None)
            while ci >= len(self.col_end):
                self.col_end.append(None)
            if self.col_start[ci] is None or rownum < self.col_start[ci]:
                self.col_start[ci] = rownum
            if self.col_end[ci] is None or rownum > self.col_end[ci]:
                self.col_end[ci] = rownum
        if len(row)-1 > self.max_col:
            self.max_col = len(row)-1
        for r in self.map_data:
            if len(r) < self.max_col:
                r = r.extend([' ']*((self.max_col+1) - len(r)))
    def cubify(self):
        l, w = len(self.map_data), len(self.map_data[0])
        if l > w:
            l, w = w, l
        if l % 3 != 0:
            print(f"ERROR: Dimensions of map are not a valid cube: {l}x{w}. {l} must be divisible by 3.")
            return False
        if w % 4 != 0:
            print(f"ERROR: Dimensions of map are not a valid cube: {l}x{w}. {w} must be divisible by 4.")
            return False
        l_fl = l // 3
        w_fl = w // 4
        if l_fl != w_fl:
            print(f"ERROR: Dimensions of map are not a valid cube: {l}x{w}. Ratio of {l}:{w} must be 3:4.")
            return False
        face_length = l_fl
        regions = []
        current_face = "A"
        for row in range(len(self.map_data)//face_length):
            regions.append([])
            for col in range(len(self.map_data[0])//face_length):
                if self.map_data[row*face_length][col*face_length] != ' ':
                    regions[row].append(current_face)
                    current_face = chr(ord(current_face)+1)
                else:
                    regions[row].append(" ")
        #print_map(regions)
        if current_face != "G":
            print(f"ERROR: Too many faces in map to be a cube.")
            print_map(regions)
            return False
        faces = [[" " for _ in range(len(regions[0]))] for _ in range(len(regions))]
        for c in range(len(regions[0])):
            if regions[0][c] == " ":
                continue
            if faces[0][c] != " ":
                continue
            faces[0][c] = "U"
            if c < len(regions[0])-1 and regions[0][c+1] != " ":
                faces[0][c+1] = "R"
            if regions[1][c] != " ":
                faces[1][c] = "F"
        faces_needed = set(["R","F","D","L","B"])
        face_links = {
            "U": ["B","R","F","L"],
            "R": ["U","B","D","F"],
            "F": ["U","R","D","L"],
            "L": ["U","F","D","B"],
            "B": ["U","L","D","R"],
            "D": ["F","R","B","L"]
        }
        while faces_needed:
            rem = []
            for fn in faces_needed:
                p = find_map_value(faces,fn)
                if p is None:
                    continue
                rem.append(fn)
                #print_map(faces)
                #print(fn)
                r,c = p
                checks = [(-1,0),(0,1),(1,0),(0,-1)]
                found = None
                for i,chk in enumerate(checks):
                    if r + chk[0] < 0 or r + chk[0] >= len(faces):
                        continue
                    if c + chk[1] < 0 or c + chk[1] >= len(faces[0]):
                        continue
                    r2, c2 = map_translate(faces,(r,c),chk)
                    if faces[r2][c2] != " ":
                        found = (faces[r2][c2],i)
                        break
                #print(found)
                #print(f"{fn}: {face_links[fn]}")
                while face_links[fn][found[1]] != found[0]:
                    face_links[fn].append(face_links[fn].pop(0))
                #print(f"{fn}: {face_links[fn]}")
                for i in range(4):
                    tr = checks[i]
                    if r + tr[0] < 0 or r + tr[0] >= len(faces):
                        continue
                    if c + tr[1] < 0 or c + tr[1] >= len(faces[0]):
                        continue
                    lnk = face_links[fn][i]
                    r2, c2 = map_translate(faces,(r,c),tr)
                    if regions[r2][c2] == " ":
                        continue
                    if faces[r2][c2] == " ":
                        faces[r2][c2] = lnk
                    else:
                        if faces[r2][c2] != lnk:
                            print("ERROR: Invalid cube shape based on face orientation")
                            print_map(faces)
                            print(f"{tr} from {fn} should be {lnk}")
                            return False
            for r in rem:
                faces_needed.remove(r)
        self.faces = faces
        self.face_length = face_length
        self.face_links = face_links

        #print(self.face_links)
        #print_map(faces)
        self.is_cube = True

    def get(self,row,col):
        if row < 0 or row >= len(self.map_data) or col < 0 or col >= len(self.map_data[row]):
            return ' '
        return self.map_data[row][col]

    def get_region(self,row,col):
        if not self.is_cube:
            return (None, None)
        rr = row // self.face_length
        rc = col // self.face_length
        return (rr,rc)
    
    def advance(self,r,c,d):
        rot = 0
        if d == '>':
            n = (r,c+1)
            u = self.get(*n)
            if u == ' ':
                if self.is_cube:
                    n, u, rot = self.cube_advance((r,c),1)
                else:
                    n = (r,self.row_start[r])
                    u = self.get(*n)
                    if u == ' ':
                        raise Exception(f"Row {r} should not start with a blank")
        elif d == 'v':
            n = (r+1,c)
            u = self.get(*n)
            if u == ' ':
                if self.is_cube:
                    n, u, rot = self.cube_advance((r,c),2)
                else:
                    n = (self.col_start[c],c)
                    u = self.get(*n)
                    if u == ' ':
                        raise Exception(f"Column {c} should not start with a blank")
        elif d == '<':
            n = (r,c-1)
            u = self.get(*n)
            if u == ' ':
                if self.is_cube:
                    n, u, rot = self.cube_advance((r,c),3)
                else:
                    n = (r,self.row_end[r])
                    u = self.get(*n)
                    if u == ' ':
                        raise Exception(f"Row {r} should not end with a blank")
        elif d == '^':
            n = (r-1,c)
            u = self.get(*n)
            if u == ' ':
                if self.is_cube:
                    n, u, rot = self.cube_advance((r,c),0)
                else:
                    n = (self.col_end[c],c)
                    u = self.get(*n)
                    if u == ' ':
                        raise Exception(f"Column {c} should not end with a blank")
        else:
            raise ValueError(f"Invalid direction: {d}")
        if u == '.':
            return n, rot
        return (r,c), 0

    def cube_advance(self,p,d):
        r,c = p
        reg = self.get_region(r,c)
        face = self.faces[reg[0]][reg[1]]
        to_face = self.face_links[face][d]
        to_face_d = self.face_links[to_face].index(face)
        rotations = to_face_d - (d+2 % 4)
        while rotations < 0:
            rotations += 4
        nf_r = find_map_value(self.faces,to_face) # new face region
        n = (nf_r[0] * self.face_length, nf_r[1] * self.face_length) # new position
        if d == 0:
            offset = c % self.face_length
        elif d == 1:
            offset = r % self.face_length
        elif d == 2:
            offset = (self.face_length - 1) - (c % self.face_length)
        elif d == 3:
            offset = (self.face_length - 1) - (r % self.face_length)

        if to_face_d == 0:
            n = (n[0],(n[1] + self.face_length - 1) - offset)
        elif to_face_d == 1:
            n = ((n[0] + self.face_length - 1) - offset,n[1] + self.face_length - 1)
        elif to_face_d == 2:
            n = (n[0] + self.face_length - 1, n[1] + offset)
        elif to_face_d == 3:
            n = (n[0] + offset,n[1])
        else:
            raise Exception(f"Invalid to_face direction: {to_face_d}")
        u = self.get(*n)
        return n,u,rotations

    def find_start(self):
        r = 0
        c = self.row_start[0]
        while self.get(r,c) != ".":
            c += 1
        return (r,c)

    def draw(self):
        s = ""
        for r in range(len(self.map_data)):
            for c in range(self.max_col+1):
                s += self.get(r,c)
            s += "\n"
        return s

    def draw_path(self,path):
        draw = self.draw()
        str_data = [list(line) for line in draw.splitlines()]
        for fp, tp, d in path:
            r,c = fp
            str_data[r][c] = d
            while (r,c) != tp:
                (r,c),rot = self.advance(r,c,d)
                d = rotate_dir(d,rot)
                str_data[r][c] = d
        return "\n".join("".join(line) for line in str_data)

def rotate_dir(d,rot):
    if rot == 0:
        return d
    dirs = ["^",">","v","<"]
    di = dirs.index(d)
    #print(f"{d}r{rot} -> {dirs[(di+rot)%4]}")
    return dirs[(di + rot) % 4]

def rotate_list(l,n):
    for i in range(n):
        x = l.pop(0)
        l.append(x)
    return l

def print_map(m):
    s = ""
    for r in range(len(m)):
        for c in range(len(m[r])):
            s += m[r][c]
        s += "\n"
    print(s)

def find_map_value(m,v):
    for r in range(len(m)):
        for c in range(len(m[r])):
            if m[r][c] == v:
                return (r,c)
    return None

def map_translate(m,p1,p2):
    return ((p1[0] + p2[0]) % len(m), (p1[1] + p2[1]) % len(m[0]))

def read_map_and_instructions(txt):
    themap = Map()
    instructions = []
    state = 0
    for line in txt.splitlines():
        if line.strip() == "":
            if state == 0:
                state = 1
            continue
        if state == 0:
            row = []
            for c in line:
                if c == '\n':
                    break
                row.append(c)
            themap.add_row(row)
        elif state == 1:
            line = line.strip()
            n_buf = ''
            ci = 0
            while ci < len(line):
                if line[ci].isnumeric():
                    n_buf = n_buf + line[ci]
                else:
                    if n_buf != '':
                        instructions.append(int(n_buf))
                        n_buf = ''
                    instructions.append(line[ci])
                ci += 1
            if n_buf != '':
                instructions.append(int(n_buf))
    return themap, instructions

def exec_instructions(themap,ins,start=None):
    turn_left = {
            '>': '^',
            'v': '>',
            '<': 'v',
            '^': '<'
    }
    turn_right = {
            '>': 'v',
            'v': '<',
            '<': '^',
            '^': '>'
    }
    turn = {
            'L': lambda d: turn_left[d],
            'R': lambda d: turn_right[d]
    }
    if start is None:
        start = themap.find_start()
    r,c = start
    pr, pc = r, c
    d = '>'
    path = []
    for i in ins:
        if type(i) is int:
            t = i
            init_d = d
            while t > 0:
                (nr,nc),rot = themap.advance(r,c,d)
                if r == nr and c == nc:
                    break
                r, c = nr, nc
                d = rotate_dir(d,rot)
                t -= 1
            path.append(((pr,pc),(r,c),init_d))
            pr, pc = r, c
        else:
            if i in turn:
                d = turn[i](d)
            else:
                raise Exception(f"Unknown instruction: {i}")
    return path, ((r,c),d)

def part1(inp):
    themap, instr = read_map_and_instructions(inp)
    path,final = exec_instructions(themap, instr)
    print(path)
    draw = themap.draw_path(path)
    print(draw)
    d_vals = {'>': 0, 'v': 1, '<': 2, '^': 3}
    fp = final[0]
    d = final[1]
    pw = (fp[0]+1) * 1000 + (fp[1]+1) * 4 + d_vals[d]
    print(f"Final password is 1000 * {fp[0]+1} + 4 * {fp[1]+1} + {d_vals[d]}: {pw}")

def part2(inp):
    themap, instr = read_map_and_instructions(inp)
    themap.cubify()
    path,final = exec_instructions(themap, instr)
    #print(path)
    #for i in range(len(path)):
    #    draw = themap.draw_path(path[:i+1])
    #    print(draw)
    #    print("---")
    draw = themap.draw_path(path)
    print(draw)
    d_vals = {'>': 0, 'v': 1, '<': 2, '^': 3}
    fp = final[0]
    d = final[1]
    pw = (fp[0]+1) * 1000 + (fp[1]+1) * 4 + d_vals[d]
    print(f"Final password is 1000 * {fp[0]+1} + 4 * {fp[1]+1} + {d_vals[d]}: {pw}")

def main():
    AoC.set_day("22")
    args = AoC.parse_args()

    inp = AoC.get_input()
    print("--- Part 1 ---")
    part1(inp)
    print("--- Part 2 ---")
    part2(inp)

if __name__ == "__main__":
    main()
