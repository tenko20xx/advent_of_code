// This file is auto-generated by gen_header.py
#ifndef AoC_modules_H
#define AoC_modules_H

#include <string>
#include <map>
#include "AoC.h"

AoC *day1_create(bool test);
AoC *day4_create(bool test);
AoC *day2_create(bool test);
AoC *day3_create(bool test);

using ModuleFuncPtr = AoC* (*)(bool);

namespace AoCModules {
	std::map<std::string,ModuleFuncPtr> modules = {
		{"day1", day1_create},
		{"day4", day4_create},
		{"day2", day2_create},
		{"day3", day3_create}
	};
};

#endif