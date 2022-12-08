#!/usr/bin/python3

import AoC

class FSNode:
    def __init__(self,name,parent):
        self.name = name
        self.parent = parent
        self.size = 0
    def __str__(self):
        if self.parent is None:
            return "/"
        path = [self]
        n = self
        while n.parent is not None:
            path = [n.parent] + path
            n = n.parent
        return "/".join([p.name for p in path])
    def get_size(self):
        return self.size

class Directory(FSNode):
    def __init__(self,name,parent):
        self.name = name
        self.parent = parent
        self.contents = {}
        self.size = 0
    def add_content(self,content):
        if content.name not in self.contents:
            self.contents[content.name] = content
        else:
            raise Exception("ERROR: File with name {} already in directory {}".format(content.name,self))
    def get_size(self):
        size = self.size
        for c in self.contents.values():
            size += c.get_size()
        return size
    def find_all_subdirs(self):
        subdirs = [self]
        for c in self.contents.values():
            if type(c) is Directory:
                subdirs.extend(c.find_all_subdirs())
        return subdirs

class File(FSNode):
    def __init__(self,name,parent,size):
        self.name = name
        self.parent = parent
        self.size = size

def tree(node,space=0):
    print(" "*space + ("{: <"+str(30-space)+"}{}").format(node.name + ("/" if type(node) is Directory else ""),node.get_size()))
    if type(node) is Directory:
        for name in node.contents:
            tree(node.contents[name],space+2)

def build_fs(cmds):
    root = Directory("",None)
    pwd = root
    cmd_state = ""
    for line in cmds.splitlines():
        #print(pwd)
        #print(line)
        line = line.strip()
        parts = line.split()
        if parts[0] == "$":
            cmd_state = None
            cmd = parts[1]
            if cmd == "cd":
                d = parts[2]
                if d == "/":
                    pwd = root
                elif d == "..":
                    pwd = pwd.parent
                    continue
                else:
                    cd = pwd.contents.get(d)
                    if type(cd) is Directory:
                        pwd = cd
                    else:
                        raise Exception("Cannot cd to non-directory: {}".format(cd))
            elif cmd == "ls":
                cmd_state = "ls"
        else:
            if cmd_state is None:
                raise Exception("Output present while not in a command state")
            if cmd_state == "ls":
                name = parts[1]
                if parts[0] == "dir":
                    d = Directory(name,pwd)
                    pwd.add_content(d)
                else:
                    pwd.add_content(File(name,pwd,int(parts[0])))
    return root

def part1(inp):
    root = build_fs(inp)
    all_dirs = root.find_all_subdirs()
    if AoC.TEST:
        tree(root)
    limit = 100000
    total = 0
    for d in all_dirs:
        if d.get_size() <= limit:
            total += d.get_size()
    print("Total of all directories with size at most {}: {}".format(limit,total))

def part2(inp):
    root = build_fs(inp)
    all_dirs = root.find_all_subdirs()
    if AoC.TEST:
        tree(root)
    disk_size    = 70000000
    space_needed = 30000000
    unused_space = disk_size - root.get_size()
    free_space_req = space_needed - unused_space
    AoC.tprint("fs size is {}".format(root.get_size()))
    AoC.tprint("unused space is {}".format(unused_space))
    AoC.tprint("free space needed is {}".format(free_space_req))
    min_delete = None
    for d in all_dirs:
        ds = d.get_size()
        if ds >= free_space_req:
            if min_delete is None or ds < min_delete[0]:
                min_delete = (ds,d.name)
    print("Minimum directory to delete is {} (size: {})".format(min_delete[1],min_delete[0]))

def main():
    AoC.parse_args()
    inp = AoC.get_input("7")
    print("== Part 1 ==")
    part1(inp)
    print("== Part 2 ==")
    part2(inp)

if __name__ == "__main__":
    main()
