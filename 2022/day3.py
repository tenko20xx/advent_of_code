#!/usr/bin/python3

def getValue(l):
    v = ord(l)
    if v >= ord('a'):
        return (v - ord('a')) + 1
    return (v - ord('A')) + 27

def main():
    print("== Part 1 ==")
    total = 0
    with open("inputs/day3.input",'r') as fp:
        for pack in fp:
            pack = pack.strip()
            c1 = pack[:len(pack)//2]
            c2 = pack[len(pack)//2:]
            #print("{}|{}".format(c1,c2))
            for i in c1:
                if i in c2:
                    #print("{}:{}".format(i,getValue(i)))
                    total += getValue(i)
                    break
    print("Total: {}".format(total))

    print("== Part 2 ==")
    total = 0
    group = []
    with open("inputs/day3.input",'r') as fp:
        for pack in fp:
            group.append(pack)
            if len(group) < 3:
                continue
            for c in group[0]:
                if c in group[1] and c in group[2]:
                    #print("{}:{}".format(c,getValue(c)))
                    total += getValue(c)
                    break
            group = []
    print("Total: {}".format(total))

if __name__ == "__main__":
    main()
