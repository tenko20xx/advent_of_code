#include <iostream>
#include <fstream>

#include "AoC.h"

class Day14 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
	struct Position {
		int row;
		int col;
	};
	struct RepeatingSequence {
		std::vector<int> sequence;
		int offset;
	};
	class Platform {
		public:
		Platform();
		~Platform();
		void load(std::vector<std::string>);
		void clear();
		void tilt(char dir = 'N');
		int calc_load();
		std::string get_row(int n);
		void print();
		private:
		char* data;
		bool loaded = false;
		int width;
		int height;
	} platform;
	void parse_platform(std::ifstream& fp);
	void clear();
	RepeatingSequence find_repeating_sequence(std::vector<int>);
};

Day14::Platform::Platform() {
	loaded = false;
}

Day14::Platform::~Platform() {
	clear();
}

void Day14::Platform::clear() {
	if(loaded) {
		delete data;
	}
	width = 0;
	height = 0;
	loaded = false;
}

void Day14::Platform::load(std::vector<std::string> lines) {
	height = lines.size();
	width = lines[0].length();
	data = new char[height*width];
	for(int r=0;r<height;r++) {
		//std::cout << "load line: " << lines[r] << std::endl;
		for(int c=0;c<width;c++) {
			data[r*width + c] = lines[r][c];
		}
	}
	loaded = true;
}

void Day14::Platform::tilt(char dir) {
	Position move { 0, 0 };
	if(dir == 'N') {
		move.row = -1;
	} else if (dir == 'W') {
		move.col = -1;
	} else if (dir == 'S') {
		move.row = 1;
	} else if (dir == 'E') {
		move.col = 1;
	} else {
		std::cerr << "WARNING: Invalid direction to tilt: " << dir << std::endl;
	}

	bool changed = true;
	while(changed) {
		changed = false;
		for(int r=0;r<height;r++) {
			int r_next = r + move.row;
			if(r_next < 0 || r_next >= height) continue;
			for(int c=0;c<width;c++) {
				int c_next = c + move.col;
				if(c_next < 0 || c_next >= width) continue;
				if(data[r*width + c] == 'O' && data[r_next*width + c_next] == '.') {
					data[r*width + c] = '.';
					data[r_next*width + c_next] = 'O';
					changed = true;
				}
			}
		}
	}
}

int Day14::Platform::calc_load() {
	int load = 0;
	for(int r=0;r<height;r++) {
		auto row = get_row(r);
		for(auto c : row) {
			if(c == 'O') load += (height - r);
		}
	}
	return load;
}

std::string Day14::Platform::get_row(int n) {
	std::string ret = "";
	for(int c=0;c<width;c++) {
		ret += data[n*width + c];
	}
	return ret;
}

void Day14::Platform::print() {
	for(int r=0;r<height;r++) {
		for(int c=0;c<width;c++) {
			std::cout << data[r*width + c];
		}
		std::cout << std::endl;
	}
	std::cout << "---" << std::endl;
}

void Day14::clear() {
	platform.clear();
}

void Day14::parse_platform(std::ifstream& fp) {
	clear();
	if(!fp) {
		throw ParseException(0,"Unable to read input file");
	}
	std::vector<std::string> lines;
	std::string line;
	while(std::getline(fp,line)) {
		string_trim(line);
		if (line == "") continue;
		lines.push_back(line);
	}
	platform.load(lines);
}

Day14::RepeatingSequence Day14::find_repeating_sequence(std::vector<int> list) {
	RepeatingSequence rs;
	std::vector<int> seq;
	rs.offset = 0;
	for(int size = 1 ; size < list.size() / 2 ; size++) {
		for(int i = 0 ; i < list.size() - size ; i++) {
			seq.clear();
			for(int j = 0 ; j < size ; j++) {
				seq.push_back(list[i+j]);
			}
			bool repeats = true;
			bool all_found = false;
			int si = 0;
			for(int j = i + size; j < list.size() ; j++) {
				if(list[j] != seq[si++]) { 
					repeats = false;
					break;
				}
				if(si >= size) {
					si = 0;
					all_found = true;
				}
			}
			if(repeats && all_found) {
				rs.sequence = seq;
				rs.offset = i + 1;
				return rs;
			}
		}
	}
	return rs;
}

bool Day14::part1() {
	try {
		parse_platform(getInputFile());
		if(test_mode) platform.print();
		platform.tilt('N');
		if(test_mode) platform.print();
		int load = platform.calc_load();
		std::cout << "Total load on north support beams: " << load << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

bool Day14::part2() {
	try {
		std::vector<char> cycle_pattern = {'N', 'W', 'S', 'E'};
		parse_platform(getInputFile());
		if(test_mode) { 
			platform.print();
			std::vector<std::pair<char,std::string>> try_tilts;
			try_tilts.push_back({'N', "North"});
			try_tilts.push_back({'W', "West"});
			try_tilts.push_back({'S', "South"});
			try_tilts.push_back({'E', "East"});
			for(auto pair : try_tilts) {
				platform.tilt(pair.first);
				std::cout << pair.second << " tilt:" << std::endl;
				platform.print();
			}
			parse_platform(getInputFile());
			for(int i=0;i<3;i++) {
				for(auto c : cycle_pattern) {
					platform.tilt(c);
				}
				std::cout << "After " << (i+1) << " cycle" << (i == 0 ? "" : "s") << ":" << std::endl;
				platform.print();
			}
			parse_platform(getInputFile());
		}
		constexpr int N = 1000000000;
		int count = 0;
		std::vector<int> results;
		RepeatingSequence repeating_seq;
		while(count++ < 100 || repeating_seq.sequence.size() == 0) {
			for(auto c : cycle_pattern) {
				platform.tilt(c);
			}
			//if(test_mode) std::cout << count << ":" << platform.calc_load() << std::endl;
			results.push_back(platform.calc_load());
			repeating_seq = find_repeating_sequence(results);
		}
		if(test_mode) {
			std::cout << "Repeating Sequence: ";
			for(auto n : repeating_seq.sequence) std::cout << n << " ";
			std::cout << std::endl;
			std::cout << "Offset: " << repeating_seq.offset << std::endl;
		}
		int n = (N - repeating_seq.offset) % repeating_seq.sequence.size();
		int load = repeating_seq.sequence[n];
		std::cout << "Total load after " << N << " cycles: " << load << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

Day14 *day14_create() {
	return new Day14;
}
