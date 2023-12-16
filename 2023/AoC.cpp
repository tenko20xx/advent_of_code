#include <string>
#include <vector>
#include <iostream>

#include "AoC.h"
#include "AoC_modules.h"

std::string prog_name;

AoC::AoC() : test_mode(false), verbosity(0), name("base") {
	inputFileOpened = false;
}

AoC::~AoC() {
	closeInputFile();
}

void AoC::closeInputFile() {
	if(inputFileOpened) {
		inputFile_fp.close();
		inputFile_fp.clear();
	}
	inputFileOpened = false;
}

std::string AoC::getInputFileName() {
	if(test_mode)
		return getInputFileName("test");
	return getInputFileName("");
}

std::string AoC::getInputFileName(std::string subpart) {
	return "inputs/" + this->name + (subpart == "" ? "" : "." + subpart) + ".input";
}

std::ifstream& AoC::getInputFile() {
	openInputFile();
	return inputFile_fp;
}

std::ifstream& AoC::getInputFile(std::string subpart) {
	openInputFile(subpart);
	return inputFile_fp;
}


void AoC::openInputFile() {
	closeInputFile();
	auto fname = getInputFileName();
	if(isVerbose(3)) 
		std::cout << "Opening input file \"" << fname << "\"" << std::endl;
	inputFile_fp.open(fname);
	if(!inputFile_fp) {
		std::cerr << "ERROR: Unable to open file '" << fname << "'" << std::endl;
	}
	inputFileOpened = true;
}

void AoC::openInputFile(std::string subpart) {
	closeInputFile();
	auto fname = getInputFileName(subpart);
	if(isVerbose(3)) 
		std::cout << "Opening input file \"" << fname << "\"" << std::endl;
	inputFile_fp.open(fname);
	if(!inputFile_fp) {
		std::cerr << "ERROR: Unable to open file '" << fname << "'" << std::endl;
	}
	inputFileOpened = true;
}

const char* ParseException::what() {
	return "Parsing Exception";
}

const std::string ParseException::getMessage() {
	return "Error parsing input file on line " + std::to_string(line) + ": " + message;
}

ParseException::ParseException(int l, std::string emsg) : line(l), message(emsg) { }

////////////////////////////////
// Stand-alone utilities
//////////////////////////////
std::vector<std::string> string_split(std::string s, std::string delim) {
	std::vector<std::string> parts;
	std::size_t i = 0;
	std::size_t pos;
	while(true) {
		pos = s.find(delim,i);
		if(pos == s.npos) {
			parts.push_back(s.substr(i));
			break;
		}
		parts.push_back(s.substr(i,pos-i));
		i = pos + delim.length();
	}
	return parts;
}
//////////////////////////////
// Stand-alone utilities
////////////////////////////////

struct Options {
	std::string exec_day = "";
	bool test_mode = false;
	bool list_days = false;
	bool show_help = false;	
	bool has_errors = false;
	bool exec_part1 = false;
	bool exec_part2 = false;
	int verbosity = 0;
	std::vector<std::string> error_messages;
};

void show_help() {
	std::cout << "usage: " << prog_name << " -h | -l | [options] day## | all" << std::endl;
	std::cout << "options: " << std::endl;
	std::cout << "  -h,--help          Show this message and exit" << std::endl;
	std::cout << "  -t,--test          Execute in test mode" << std::endl;
	std::cout << "  -l,--list          List available days" << std::endl;
	std::cout << "  -v,--verbose       Be verbose (pass multiple times for more verbosity [max:3])" << std::endl;
	std::cout << "  --part1,--part2    Execute part1 or part2 (leave absent to exec both)" << std::endl;
}

Options parse_args(int argc, char** argv) {
	Options ret;
	for(int i=1;i<argc;i++) {
		std::string arg = argv[i];
		if(arg.length() >= 2 && arg.substr(0,2) == "--") {
			auto opt = arg.substr(2);
			if(opt == "help") {
				ret.show_help = true;
				break;
			} else if (opt == "test") {
				ret.test_mode = true;
			} else if (opt == "list") {
				ret.list_days = true;
			} else if (opt == "part1") {
				ret.exec_part1 = true;
			} else if (opt == "part2") {
				ret.exec_part2 = true;
			} else if (opt == "verbose") {
				ret.verbosity++;
			} else {
				ret.has_errors = true;
				ret.error_messages.push_back("Unknown argument: " + arg);
				break;
			}
		} else if (arg.length() >= 1 && arg[0] == '-') {
			for(auto c : arg.substr(1)) {
				if(c == 'h') {
					ret.show_help = true;
					break;
				} else if(c == 't') {
					ret.test_mode = true;
				} else if (c == 'l') {
					ret.list_days = true;
				} else if (c == 'v') {
					ret.verbosity++;
				} else {
					ret.has_errors = true;
					ret.error_messages.push_back("Unknown option: " + c);
					break;
				}
			}
			if(ret.has_errors || ret.show_help) break;
		} else {
			if(ret.exec_day == "") {
				ret.exec_day = arg;
			} else {
				ret.has_errors = true;
				ret.error_messages.push_back("Cannot pass more than one day");
				break;
			}
		}
	}
	if (!ret.exec_part1 && !ret.exec_part2) {
		ret.exec_part1 = true;
		ret.exec_part2 = true;
	}
	if(ret.verbosity > 3) ret.verbosity = 3;
	if(ret.test_mode && ret.verbosity == 0) ret.verbosity = 1;
	return ret;
}

int execute_module(std::string module_name, bool test_mode, bool xpart1, bool xpart2, int verbosity = 0) {
	auto factory = *(AoCModules::modules.at(module_name));
	AoC *puzzle = factory();
	puzzle->setName(module_name);
	puzzle->setTestMode(test_mode);
	puzzle->setVerbosity(verbosity);
	std::cout << "** " << module_name << " **" << std::endl << std::endl;
	bool okay;
	if (xpart1) {
		std::cout << "-- Part 1 --" << std::endl;
		okay = puzzle->part1();
		if(!okay) {
			std::cerr << "ERROR: part1 failed" << std::endl;
			return 12;
		}
	}
	if (xpart2) {
		std::cout << "-- Part 2 --" << std::endl;
		okay = puzzle->part2();
		if(!okay) {
			std::cerr << "ERROR: part2 failed" << std::endl;
			return 13;
		}
	}
	delete puzzle;
	return 0;
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
		for(auto &day : AoCModules::modules_order) {
			std::cout << "  " << day << std::endl;
		}
		return 0;
	}
	if(opts.exec_day == "all") {
		for(auto &day : AoCModules::modules_order) {
			execute_module(day,opts.test_mode,opts.exec_part1,opts.exec_part2,opts.verbosity);
			std::cout << std::endl << std::endl;
		}
		return 0;
	}
	else if(AoCModules::modules.find(opts.exec_day) != AoCModules::modules.end()) {
		int rc = execute_module(opts.exec_day,opts.test_mode,opts.exec_part1,opts.exec_part2,opts.verbosity);
		return rc;
	} else {
		std::cerr << "ERROR: There is no " << opts.exec_day << std::endl;
		return 11;
	}
	return 0;
}
