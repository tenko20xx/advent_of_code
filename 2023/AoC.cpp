#include <string>
#include <vector>
#include <iostream>

#include "AoC.h"
#include "AoC_modules.h"

std::string prog_name;

AoC::AoC(bool test_mode) : test_mode(test_mode) {
};

std::string AoC::getInputFileName() {
	if(test_mode)
		return getInputFileName("test");
	return getInputFileName("");
}

std::string AoC::getInputFileName(std::string subpart) {
	return "inputs/" + this->name + (subpart == "" ? "" : "." + subpart) + ".input";
}

std::ifstream AoC::getInputFile() {
	std::ifstream fp;
	fp.open(this->getInputFileName());
	return fp;
}

std::ifstream AoC::getInputFile(std::string subpart) {
	std::ifstream fp;
	fp.open(this->getInputFileName(subpart));
	return fp;
}

struct Options {
	std::string exec_day = "";
	bool test_mode = false;
	bool list_days = false;
	bool show_help = false;	
	bool has_errors = false;
	bool exec_part1 = false;
	bool exec_part2 = false;
	std::vector<std::string> error_messages;
};

void show_help() {
	std::cout << "usage: " << prog_name << " -h | -l | [options] day##" << std::endl;
	std::cout << "options: " << std::endl;
	std::cout << "  -h,--help          Show this message and exit" << std::endl;
	std::cout << "  -t,--test          Execute in test mode" << std::endl;
	std::cout << "  -l,--list          List available days" << std::endl;
	std::cout << "  --part1,--part2    Execute part1 or part2 (leave absent to exec both)" << std::endl;
}

Options parse_args(int argc, char** argv) {
	Options ret;
	for(int i=1;i<argc;i++) {
		std::string arg = argv[i];
		if(arg == "-h" || arg == "--help") {
			ret.show_help = true;
			break;
		} else if (arg == "-t" || arg == "--test") {
			ret.test_mode = true;
		} else if (arg == "-l" || arg == "--list") {
			ret.list_days = true;
		} else if (arg == "--part1") {
			ret.exec_part1 = true;
		} else if (arg == "--part2") {
			ret.exec_part2 = true;
		} else if (arg[0] != '-') {
			if(ret.exec_day == "") {
				ret.exec_day = arg;
			} else {
				ret.has_errors = true;
				ret.error_messages.push_back("Cannot pass more than one day");
			}
		} else {
			ret.has_errors = true;
			ret.error_messages.push_back("Unknown argument: " + arg);
			break;
		}
	}
	if (!ret.exec_part1 && !ret.exec_part2) {
		ret.exec_part1 = true;
		ret.exec_part2 = true;
	}
	return ret;
}

int main(int argc, char** argv) {
	prog_name = argv[0];
	if (argc == 1) {
		show_help();
		return 0;
	}
	Options opts = parse_args(argc, argv);
	if(opts.has_errors) {
		for(auto &m : opts.error_messages) {
			std::cerr << "Error: " << m << std::endl;
		}
		show_help();
		return 10;
	}
	if (opts.show_help) {
		show_help();
		return 0;
	}
	if (opts.list_days) {
		std::cout << "Available days to execute:" << std::endl;
		for(auto &kv : AoCModules::modules) {
			std::cout << "  " << kv.first << std::endl;
		}
		return 0;
	}
	if(AoCModules::modules[opts.exec_day]) {
		AoC *puzzle = AoCModules::modules[opts.exec_day](opts.test_mode);
		puzzle->setName(opts.exec_day);
		std::cout << "** " << opts.exec_day << " **" << std::endl << std::endl;
		bool okay;
		if (opts.exec_part1) {
			okay = puzzle->part1();
			if(!okay) {
				std::cerr << "ERROR: part1 failed" << std::endl;
				return 12;
			}
		}
		if (opts.exec_part2) {
			okay = puzzle->part2();
			if(!okay) {
				std::cerr << "ERROR: part2 failed" << std::endl;
				return 13;
			}
		}
	} else {
		std::cerr << "ERROR: There is no " << opts.exec_day << std::endl;
		return 11;
	}
	return 0;
}
