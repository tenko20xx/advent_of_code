#include <iostream>
#include <fstream>
#include <map>
#include <utility>
#include "AoC.h"

class Day1 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
};

bool Day1::part1() {
	std::cout << "-- Part 1 --" << std::endl;
	//std::cout << this->getInputFileName() << std::endl;
	std::ifstream file = this->getInputFile();
	std::string line;
	int n1,n2,total;
	total = 0;
	while(std::getline(file,line)) {
		for(auto it = line.cbegin(); it != line.cend(); it++) {
			//std::cout << *it << "(" << (int)(*it) << ")" << std::endl;
			if((int)(*it) >= '0' && (int)(*it) <= '9') {
				n1 = (int)(*it) - '0';
				break;
			}
		}
		for(auto it = line.crbegin(); it != line.crend(); it++) {
			//std::cout << (*it) << std::endl;
			if((int)(*it) >= '0' && (int)(*it) <= '9') {
				n2 = (int)(*it) - '0';
				break;
			}
		}
		int this_sum = n1*10 + n2;
		if(this->test_mode) 
			std::cout << line << " -> " << this_sum << std::endl;
		total += this_sum;
	}
	std::cout << "The sum of all of the calibration values is " << total << std::endl;
	return true;
}

bool Day1::part2() {
	std::cout << "-- Part 2 --" << std::endl;
	std::map<std::string,int> searches = {
		{"0", 0},
		{"1", 1},
		{"2", 2},
		{"3", 3},
		{"4", 4},
		{"5", 5},
		{"6", 6},
		{"7", 7},
		{"8", 8},
		{"9", 9},
		{"zero",	0},
		{"one",		1},
		{"two",		2},
		{"three",	3},
		{"four",	4},
		{"five",	5},
		{"six",		6},
		{"seven",	7},
		{"eight",	8},
		{"nine",	9}
	};
	std::ifstream file = test_mode ? this->getInputFile("test2") : this->getInputFile();
	std::string line;
	int n1,n2,total;
	total = 0;
	auto print_pair = [](std::pair<int,std::string> p){ std::cout << p.first << ":" << p.second << std::endl; };
	while(std::getline(file,line)) {
		tprint(line);
		std::pair<int,std::string> firstFound = {-1,""};
		std::pair<int,std::string> lastFound = {-1,""};
		for( const auto &kv : searches ) {
			std::string key = kv.first;
			int found = line.find(key);
		       	if (found != std::string::npos && 
					(firstFound.first == -1 || found < firstFound.first)) {
				firstFound.first = found;
				firstFound.second = key;
			}
			found = line.rfind(key);
			if (found != std::string::npos && 
					(lastFound.first == -1 || found > lastFound.first)) {
				lastFound.first = found;
				lastFound.second = key;
			}
		}
		if(this->test_mode) {
			print_pair(firstFound);
			print_pair(lastFound);
		}
		n1 = searches[firstFound.second];
		n2 = searches[lastFound.second];
		int this_sum = n1*10 + n2;
		tprint(std::to_string(this_sum));
		total += this_sum;
	}
	std::cout << "The sum of all of the calibration values is " << total << std::endl;
	return true;
}

Day1 *day1_create(bool test) { 
	return new Day1(test);
}
