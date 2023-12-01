#ifndef AoC_H
#define AoC_H

#include <string>
#include <iostream>
#include <fstream>

class AoC {
	public:
		void tprint(std::string msg) { if(test_mode) std::cout << msg << std::endl; };
		void setName(std::string name) { this->name = name; };
		std::string getInputFileName();
		std::string getInputFileName(std::string subpart);
		std::ifstream getInputFile();
	       	std::ifstream getInputFile(std::string subpart);
		virtual bool part1() { std::cout << "-- Part 1 --" << std::endl; return false; };
		virtual bool part2() { std::cout << "-- Part 2 --" << std::endl; return false; };
		AoC(bool test_mode = false);
	protected:
		bool test_mode;
		std::string name;
};

#endif
