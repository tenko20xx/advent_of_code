#!/usr/bin/python3

import os
import sys
from gen_header import gen_header

DAY_TEMPLATE="""#include <iostream>
#include <fstream>

#include "AoC.h"

class Day{{N}} : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
};

bool Day{{N}}::part1() {
    std::cout << "-- Part 1 --" << std::endl;
    return false;
}

bool Day{{N}}::part2() {
    std::cout << "-- Part 2 --" << std::endl;
    return false;
}

Day{{N}} *day{{N}}_create(bool test) {
    return new Day{{N}}(test);
}
"""

def usage(f=sys.stdout):
    print("""usage mk_day.py N
N: Creates day N where N is an int between 1 and 25
""",file=f)

def make_day(n):
    fname = f"day{n}.cpp"
    if os.path.exists(fname):
        print(f"ERROR: File with name {fname} already exists!")
        sys.exit(13)
    print(f"making {fname}...")
    with open(fname,'w') as fp:
        output = DAY_TEMPLATE
        output = output.replace("{{N}}",str(n))
        fp.write(output)
    print("updating AoC_modules.h...")
    gen_header(True)
    print("done.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(10)
    try:
        N = int(sys.argv[1])
        if N < 1 or N > 25:
            print("ERROR: N should be between 1 and 25",file=sys.stderr)
            usage(sys.stderr)
            sys.exit(11)
        make_day(N)
    except ValueError:
        print(f"ERROR: {N} is not a valid integer",file=sys.stderr)
        usage(sys.stderr)
        sys.exit(12)
