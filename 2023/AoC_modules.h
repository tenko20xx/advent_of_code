#ifndef AoC_modules_H
#define AoC_modules_H

#include <string>
#include <map>
#include "AoC.h"

AoC *day1_create(bool test);

using ModuleFuncPtr = AoC* (*)(bool);

namespace AoCModules {
	std::map<std::string,ModuleFuncPtr> modules = {
		{"day1", day1_create}
	};
};

#endif
