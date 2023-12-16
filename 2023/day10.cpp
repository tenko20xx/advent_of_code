#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <set>
#include <stack>
#include <queue>

#include "AoC.h"

class Day10 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
	private:
	struct Position {
		int row;
		int col;
		Position move(char dir);
		std::string to_string();
		bool operator==(Position other);
	};
	struct Map {
		const static int MAX_MAP_SIZE = 150 * 2 + 1;
		
		Position start;
		int width;
		int height;
		char data[MAX_MAP_SIZE][MAX_MAP_SIZE];

		void clear();
		void clamp_position(Position& p);
		bool valid_position(Position& p);
		char get_pos(Position& p);
		char get_pos(int, int);
		char advance(Position& p, char prev_dir);
		void print();
		void fill(Position p, char c);
	} map;
	void clear();
	void parse_map(std::ifstream& fp);
};

namespace Day10NS {

};

Day10::Position Day10::Position::move(char dir) {
	Position p;
	p.row = this->row;
	p.col = this->col;
	switch(dir) {
		case 'N':
			p.row -= 1;
			break;
		case 'E':
			p.col += 1;
			break;
		case 'S':
			p.row += 1;
			break;
		case 'W':
			p.col -= 1;
			break;
	}
	return p;
}

std::string Day10::Position::to_string() {
	return "(" + std::to_string(this->row) + "," + std::to_string(this->col) + ")";
}

bool Day10::Position::operator==(Position other) {
	return this->row == other.row && this->col == other.col;
}

void Day10::Map::clear() {
	width = 0;
	height = 0;
}

void Day10::Map::clamp_position(Position& p) {
	if(p.row < 0) p.row = 0;
	if(p.row >= height) p.row = height - 1;
	if(p.col < 0) p.col = 0;
	if(p.col >= width) p.col = width - 1;
}

bool Day10::Map::valid_position(Position& p) {
	if(p.row < 0) return false;
	if(p.row >= height) return false;
	if(p.col < 0) return false;
	if(p.col >= width) return false;
	return true;
}

char Day10::Map::get_pos(Position& p) {
	if(valid_position(p)) {
		return data[p.row][p.col];
	}
	return '?';
}

char Day10::Map::get_pos(int row, int col) {
	Position p {row, col};
	return get_pos(p);
}

char Day10::Map::advance(Position& p, char prev_dir) {
	char x = get_pos(p);
	switch(prev_dir) {
		case 'N':
			switch(x) {
				case '|':
					p.row += 1;
					return 'N';
				case 'J':
					p.col -= 1;
					return 'E';
				case 'L':
					p.col += 1;
					return 'W';
			}
			break;
		case 'E':
			switch(x) {
				case '-':
					p.col -= 1;
					return 'E';
				case 'L':
					p.row -= 1;
					return 'S';
				case 'F':
					p.row += 1;
					return 'N';
			}
			break;
		case 'S':
			switch(x) {
				case '|':
					p.row -= 1;
					return 'S';
				case 'F':
					p.col += 1;
					return 'W';
				case '7':
					p.col -= 1;
					return 'E';
			}
			break;
		case 'W':
			switch(x) {
				case '-':
					p.col += 1;
					return 'W';
				case 'J':
					p.row -= 1;
					return 'S';
				case '7':
					p.row += 1;
					return 'N';
			}
			break;
	}
	return '?';
}

void Day10::Map::fill(Position start_p, char c) {
	std::stack<Position> checkp;
	checkp.push(start_p);
	while(!checkp.empty()) {
		Position p = checkp.top();
		checkp.pop();
		if(!valid_position(p)) continue;
		if(get_pos(p) == '.') {
			data[p.row][p.col] = c;
			checkp.push(p.move('N'));
			checkp.push(p.move('E'));
			checkp.push(p.move('S'));
			checkp.push(p.move('W'));
		}
	}
}

void Day10::Map::print() {
	for(int h=0;h<height;h++) {
		for(int w=0;w<width;w++) {
			std::cout << get_pos(h,w);
		}
		std::cout << std::endl;
	}
	std::cout << std::endl;
}

void Day10::clear() {
	map.clear();
}

void Day10::parse_map(std::ifstream& fp) {
	clear();
	std::string line;
	int h=0;
	while(std::getline(fp,line)) {
		int w = 0;
		for(auto &ch : line) {
			if(ch == 'S') {
				map.start = {h,w};
			}
			map.data[h][w++] = ch;
		}
		if(h == 0) {
			map.width = w;
		}
		h++;
	}
	map.height = h;
}

bool Day10::part1() {
	try {
		openInputFile();
		parse_map(inputFile_fp);
		if(test_mode) map.print();
		//std::cout << "Start: " << map.start.to_string() << std::endl;
		Position p1 = map.start;
		Position p2 = map.start;
		char p1_prev;
		char p2_prev;
		std::map<char,std::string> check_exits = {
			{'N', "|7F"},
			{'E', "-J7"},
			{'S', "|JL"},
			{'W', "-FL"}
		};
		Position* this_p = &p1;
		char* this_p_prev = &p1_prev;
		for(auto &[d, pipes] : check_exits) {
			Position checkp = this_p->move(d);
			if(!map.valid_position(checkp)) continue;
			char x = map.get_pos(checkp);
			//std::cout << "Check " << d << ": " << checkp.to_string() << "->" << x << std::endl;
			for(int i=0;i<3;i++) {
				if(x == pipes[i]) {
					this_p->row = checkp.row;
					this_p->col = checkp.col;
					if(d == 'N') *this_p_prev = 'S';
					if(d == 'E') *this_p_prev = 'W';
					if(d == 'S') *this_p_prev = 'N';
					if(d == 'W') *this_p_prev = 'E';
					if(this_p == &p1) {
						this_p = &p2;
						this_p_prev = &p2_prev;
					}
					else this_p = nullptr;
					break;
				}
			}
			if(this_p == nullptr) break;
		}

		int steps = 0;
		int visited[map.height][map.width];
		for(int h=0;h<map.height;h++) {
			for(int w=0;w<map.width;w++) {
				visited[h][w] = 0;
			}
		}
		visited[map.start.row][map.start.col] = 1;
		while(visited[p1.row][p1.col] == 0 || visited[p2.row][p2.col] == 0) {
			//std::cout << "p1:" << p1.to_string() << ", p2:" << p2.to_string() << std::endl;
			visited[p1.row][p1.col] = 1;
			visited[p2.row][p2.col] = 1;
			p1_prev = map.advance(p1,p1_prev);
			p2_prev = map.advance(p2,p2_prev);
			steps++;
		}
		std::cout << "Furthest steps in loop from start: " << steps << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

bool Day10::part2() {
	try {
		std::queue<std::string> file_q;
		if(test_mode) {
			file_q.push("test");
			file_q.push("test2");
			file_q.push("test3");
			file_q.push("test4");
		} else {
			file_q.push("");
		}
		while(!file_q.empty()) {
			auto file_name = file_q.front();
			file_q.pop();
			if(isVerbose()) std::cout << "File: " << file_name << std::endl;
			openInputFile(file_name);
			parse_map(inputFile_fp);
			if(isVerbose()) map.print();
			//std::cout << "Start: " << map.start.to_string() << std::endl;
			Position p1 = map.start;
			char p1_prev = '?';
			std::map<char,std::string> check_exits = {
				{'N', "|7F"},
				{'E', "-J7"},
				{'S', "|JL"},
				{'W', "-FL"}
			};
			Map expanded;
			expanded.height = map.height * 2 + 1;
			expanded.width = map.width * 2 + 1;
			for(int h=0;h<expanded.height;h++) {
				for(int w=0;w<expanded.width;w++) {
					expanded.data[h][w] = '.';
				}
			}
			expanded.data[map.start.row*2+1][map.start.col*2+1] = 'S';
			for(auto &[d, pipes] : check_exits) {
				Position checkp = p1.move(d);
				if(!map.valid_position(checkp)) continue;
				char x = map.get_pos(checkp);
				//std::cout << "Check " << d << ": " << checkp.to_string() << "->" << x << std::endl;
				for(int i=0;i<3;i++) {
					if(x == pipes[i]) {
						p1.row = checkp.row;
						p1.col = checkp.col;
						int exp_r = p1.row*2+1;
						int exp_c = p1.col*2+1;
						expanded.data[exp_r][exp_c] = map.get_pos(p1);
						switch(d) {
							case 'N':
								p1_prev = 'S';
								expanded.data[exp_r+1][exp_c] = '|';
								break;
							case 'E':
								p1_prev = 'W';
								expanded.data[exp_r][exp_c-1] = '-';
								break;
							case 'S':
								p1_prev = 'N';
								expanded.data[exp_r-1][exp_c] = '|';
								break;
							case 'W':
								p1_prev = 'E';
								expanded.data[exp_r][exp_c+1] = '-';
								break;
						}
						break;
					}
				}
				if(p1_prev != '?') break;
			}

			int visited[map.height][map.width];
			for(int h=0;h<map.height;h++) {
				for(int w=0;w<map.width;w++) {
					visited[h][w] = 0;
				}
			}
			visited[map.start.row][map.start.col] = 1;
			while(visited[p1.row][p1.col] == 0) {
				//std::cout << "p1:" << p1.to_string() << ", p2:" << p2.to_string() << std::endl;
				visited[p1.row][p1.col] = 1;
				p1_prev = map.advance(p1,p1_prev);
				int exp_r = p1.row*2+1;
				int exp_c = p1.col*2+1;
				expanded.data[exp_r][exp_c] = map.get_pos(p1);
				switch(p1_prev) {
					case 'N':
						expanded.data[exp_r-1][exp_c] = '|';
						break;
					case 'E':
						expanded.data[exp_r][exp_c+1] = '-';
						break;
					case 'S':
						expanded.data[exp_r+1][exp_c] = '|';
						break;
					case 'W':
						expanded.data[exp_r][exp_c-1] = '-';
						break;
				}
			}
			if(test_mode) expanded.print();
			expanded.fill(Position {0,0}, 'O');
			if(test_mode) expanded.print();
			Position empty_p;
			bool found = false;
			for(int h=0;h<expanded.height;h++) {
				for(int w=0;w<expanded.width;w++) {
					empty_p.row = h;
					empty_p.col = w;
					if(expanded.get_pos(empty_p) == '.') {
						found = true;
						break;
					}
				}
				if(found) break;
			}
			expanded.fill(empty_p,'I');
			if(test_mode) expanded.print();
			int count_inside = 0;
			for(int h=0;h<map.height;h++) {
				for(int w=0;w<map.width;w++) {
					map.data[h][w] = expanded.data[h*2+1][w*2+1];
					if(map.data[h][w] == 'I') count_inside++;
				}
			}
			if(test_mode) map.print();
			std::cout << "Number of inside spaces: " << count_inside << std::endl;
			if(test_mode) {
				std::cout << std::endl;
				std::cout << "********************************************************" << std::endl;
				std::cout << "********************************************************" << std::endl;
				std::cout << std::endl;
			}
		}
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

Day10 *day10_create() {
	return new Day10;
}
