#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include "AoC.h"

class Day3 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
};

namespace Day3NS {
	const size_t MAX_DATA_SIZE = 20000;
	class Schematic {
		public:
		const unsigned int get_index(unsigned int row, unsigned int col) { return row*width + col; }
		const char get_char(unsigned int row, unsigned int col) { return data[get_index(row,col)]; }
		const unsigned int get_width() { return width; }
		const unsigned int get_height() { return height; }
		Schematic(std::ifstream fp);
		~Schematic();
		private:
		char* data;
		unsigned int width;
		unsigned int height;
	};
	
	Schematic::Schematic(std::ifstream fp) {
		data = new char[MAX_DATA_SIZE];
		std::string line;
		width = 0;
		height = 0;
		int li = 1;
		int ci = 0;
		while(std::getline(fp,line)) {
			string_trim(line);
			if(line == "") continue;
			if(width == 0) {
				width = line.length();
			}
			if(line.length() != width) {
				throw ParseException(li,"line length is not a consistent width");
			}
			for(auto &c : line) {
				if(c == '\n') {
					std::cout << "line includes new lines" << std::endl;
				}
				data[ci++] = c;
				if(ci >= MAX_DATA_SIZE) {
					throw ParseException(li,"data exceeds max size (" + std::to_string(MAX_DATA_SIZE) + ")");
				}
			}
			height++;
			li++;
		}
	}

	Schematic::~Schematic() {
		delete data;
	}

	bool is_digit(char c) {
		return c >= '0' && c <= '9';
	}
	bool is_symbol(char c) {
		return c != '.' && !is_digit(c);
	}
	bool has_adj_symbols(Schematic &s, int row, int from_col, int to_col) {
		for(int r = row-1; r <= row+1; r++) {
			if(r < 0) continue;
			if(r >= s.get_height()) continue;
			for(int c=from_col-1; c <= to_col+1; c++) {
				if(c < 0) continue;
				if(c >= s.get_width()) continue;
				if(r == row && (c >= from_col && c <= to_col)) continue;
				if(is_symbol(s.get_char(r,c))) {
					//std::cout << "char at (" << r << "," << c << ") is a symbol: " << s.get_char(r,c) << std::endl;
					return true;
				}
			}
		}
		return false;
	}
	
	int parse_num_at(Schematic &s, int row, int col) {
		if(!is_digit(s.get_char(row,col))) return 0;
		std::string n_buf = "";
		while(col-1 >= 0 && is_digit(s.get_char(row,col-1))) col--;
		while(col < s.get_width() && is_digit(s.get_char(row,col))) {
			n_buf.push_back(s.get_char(row,col));
			col++;
		}
		return std::stoi(n_buf);
	}

	std::vector<int> find_adj_numbers(Schematic &s, int row, int col) {
		std::vector<int> nums;
		for(int r=row-1;r<=row+1;r++) {
			if(r < 0) continue;
			if(r >= s.get_height()) continue;
			for(int c=col-1;c<=col+1;c++) {
				if(c < 0) continue;
				if(c >= s.get_width()) continue;
				if(r == row && c == col) continue;
				if(is_digit(s.get_char(r,c))) {
					while(c+1 < s.get_width() && is_digit(s.get_char(r,c+1))) c++;
					nums.push_back(parse_num_at(s,r,c));

				}
			}
		}
		return nums;
	}
};

bool Day3::part1() {
	try {
		Day3NS::Schematic s(getInputFile());
		std::string n_buf;
		int n_col;
		int part_num_sum = 0;
		for(int row=0;row < s.get_height(); row++) {
			n_buf = "";
			for(int col=0; col < s.get_width(); col++) {
				char ch = s.get_char(row,col);
				if(!Day3NS::is_digit(ch)) {
					if(n_buf != "") {
						if(test_mode) {
							std::cout << "Found part #" << n_buf << std::endl;
						}
						if(Day3NS::has_adj_symbols(s,row,n_col,col-1)) {
							part_num_sum += std::stoi(n_buf);
						} else {
							if(test_mode) {
								std::cout << n_buf << " is not adjacent to a symbol" << std::endl;
							}
						}
						n_buf = "";
					}
				} else {
					if(n_buf == "") {
						n_col = col;
					}
					n_buf.push_back(ch);
				}
			}
			if(n_buf != "") {
				if(test_mode) {
					std::cout << "Found part #" << n_buf << std::endl;
				}
				if(Day3NS::has_adj_symbols(s,row,n_col,s.get_width()-1)) {
					part_num_sum += std::stoi(n_buf);
				} else {
					if(test_mode) {
						std::cout << n_buf << " is not adjacent to a symbol" << std::endl;
					}
				}
			}
		}
		std::cout << "The sum of the part numbers is " << part_num_sum << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
		return false;
	}
	return true;
}

bool Day3::part2() {
	try {
		Day3NS::Schematic s(getInputFile());
		std::string n_buf;
		unsigned long long ratio_sum = 0;
		for(int row=0;row < s.get_height(); row++) {
			for(int col=0; col < s.get_width(); col++) {
				if(s.get_char(row,col) == '*') {
					if(test_mode) {
						std::cout << "Found gear at (" << row << "," << col << ")" << std::endl;
					}
					auto nums = find_adj_numbers(s,row,col);
					if(nums.size() == 2) {
						unsigned long long ratio = nums[0] * nums[1];
						if(test_mode) std::cout << "Gear ratio is " << ratio << std::endl;
						ratio_sum += nums[0] * nums[1];
					}
				}
			}
		}
		std::cout << "The sum of the gear ratios is " << ratio_sum << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
		return false;
	}
	return true;
}

Day3 *day3_create(bool test) {
	return new Day3(test);
}
