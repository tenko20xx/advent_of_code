#ifndef AoC_H
#define AoC_H

#include <string>
#include <iostream>
#include <fstream>
#include <exception>
#include <vector>

typedef unsigned int uint;
typedef unsigned long long uint64;
typedef long long int64;

class AoC {
	public:
		void tprint(std::string msg) { if(test_mode) std::cout << msg << std::endl; };
		void setName(std::string name) { this->name = name; };
		std::string getInputFileName();
		std::string getInputFileName(std::string subpart);
		std::ifstream getInputFile();
	       	std::ifstream getInputFile(std::string subpart);
		virtual bool part1() = 0;
		virtual bool part2() = 0;
		AoC(bool test_mode = false);
	protected:
		bool test_mode;
		std::string name;
};


class ParseException : public std::exception {
	public:
	const char* what();
	const std::string getMessage();
	ParseException(int l, std::string emsg);
	private:
	int line;
	std::string message = "";
};

std::vector<std::string> string_split(std::string s, std::string delim);

inline void string_trim(std::string& str) {
	str.erase(str.find_last_not_of(" ")+1);
	str.erase(0, str.find_first_not_of(" "));
}

#endif
