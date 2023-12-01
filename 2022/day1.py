#!/usr/bin/python3

import AoC

def main():
    inp = AoC.get_input("1")
    elvs_cals = []
    elf = 1
    this_cals = 0
    for line in inp.splitlines():
        line = line.strip()
        if line == "":
            elvs_cals.append((elf,this_cals))
            this_cals = 0
            elf += 1
            continue
        this_cals += int(line)
    i = 1
    subtotal = 0
    for elf,cals in sorted(elvs_cals,key=lambda x: x[1],reverse=True)[:3]:
        print("{}: Elf {} is carrying {} calories".format(i,elf,cals))
        subtotal += cals
        i += 1
    print("Their total caloies is {}".format(subtotal))

if __name__ == "__main__":
    main()
