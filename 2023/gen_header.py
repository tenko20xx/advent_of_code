#!/usr/bin/env python3

import os

HEADER_TEMPLATE = """#ifndef AoC_modules_H
#define AoC_modules_H

#include <string>
#include <map>
#include "AoC.h"

{{functions}}

using ModuleFuncPtr = AoC* (*)(bool);

namespace AoCModules {
	std::map<std::string,ModuleFuncPtr> modules = {
		{{modules}}
	};
};

#endif
"""

def gen_header(silent=False):
    days = []
    for f in os.listdir():
        if f.startswith("day") and f.endswith(".cpp"):
            days.append(f[3:f.find(".")])

    functions = "\n".join(f"AoC *day{n}_create(bool test);" for n in days)
    modules = ",\n\t\t".join(f'{{"day{n}", day{n}_create}}' for n in days)
    output = HEADER_TEMPLATE
    output = output.replace("{{functions}}",functions)
    output = output.replace("{{modules}}",modules)
    if not silent:
        print(output)
    with open("AoC_modules.h",'w') as fp:
        fp.write(output)

def _main():
    gen_header()

if __name__ == "__main__":
    _main()
