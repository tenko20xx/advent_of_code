#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

#include "AoC.h"

class Day11 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
	struct Position {
		int64 x;
		int64 y;
		void operator+=(Position other);
		void operator-=(Position other);
	};
	class Universe {
		public:
		void expand(unsigned int factor = 2);
		void print();
		void add_galaxy(Position p);
		void clear();
		const std::vector<Position> get_galaxies() { return galaxies; }
		private:
		std::vector<Position> galaxies;
		int64 min_x;
		int64 max_x;
		int64 min_y;
		int64 max_y;
	} universe;
	void parse_universe(std::ifstream fp);
	void clear();
};

namespace Day11NS {

};

void Day11::Position::operator+=(Position other) {
	x += other.x;
	y += other.y;
}

void Day11::Position::operator-=(Position other) {
	x -= other.x;
	y -= other.y;
}

void Day11::Universe::add_galaxy(Position p) {
	if(galaxies.empty()) {
		min_x = p.x;
		max_x = p.x;
		min_y = p.y;
		max_y = p.y;
	}
	galaxies.push_back(p);
	if(p.x < min_x) min_x = p.x;
	if(p.x > max_x) max_x = p.x;
	if(p.y < min_y) min_y = p.y;
	if(p.y > max_y) max_y = p.y;
}


void Day11::Universe::print() {
	if(galaxies.empty()) {
		std::cout << "(void)" << std::endl;
		return;
	}
	uint64 range_x = max_x - min_x;
	uint64 range_y = max_y - min_y;
	char out[range_y+1][range_x+1];
	for(uint64 y=0;y<=range_y;y++) {
		for(uint64 x=0;x<=range_x;x++) {
			out[y][x] = '.';
		}
	}
	for(auto g : galaxies) {
		out[g.y - min_y][g.x - min_x] = '#';
	}
	for(uint64 y=0;y<=range_y;y++) {
		for(uint64 x=0;x<=range_x;x++) {
			std::cout << out[y][x];
		}
		std::cout << std::endl;
	}
	std::cout << std::endl;
}

void Day11::Universe::expand(unsigned int factor) {
	std::vector<int64> empty_rows;
	std::vector<int64> empty_cols;
	bool is_empty = true;
	for(int64 r = min_y ; r <= max_y ; r++) {
		is_empty = true;
		for(auto g : galaxies) {
			if(g.y == r) {
				is_empty = false;
				break;
			}
		}
		if(is_empty) {
			empty_rows.push_back(r);
		}
	}
	for(int64 c = min_x ; c <= max_x ; c++) {
		is_empty = true;
		for(auto g : galaxies) {
			if(g.x == c) {
				is_empty = false;
				break;
			}
		}
		if(is_empty) {
			empty_cols.push_back(c);
		}
	}

	int64 add_rows = 0;
	for(auto r : empty_rows) {
		//std::cout << "empty row: " << r << std::endl;
		for(auto &g : galaxies) {
			if(g.y > (r+add_rows)) g.y += factor-1;
		}
		add_rows += factor-1;
	}
	int64 add_cols = 0;
	for(auto c : empty_cols) {
		//std::cout << "empty col: " << c << std::endl;
		for(auto &g : galaxies) {
			if(g.x > (c+add_cols)) g.x += factor-1;
		}
		add_cols += factor-1;
	}
	for(auto g : galaxies) {
		if(g.x > max_x) max_x = g.x;
		if(g.y > max_y) max_y = g.y;
	}
}

void Day11::Universe::clear() {
	galaxies.clear();
	min_x = 0;
	max_x = 0;
	min_y = 0;
	max_y = 0;
}

void Day11::clear() {
	universe.clear();
}

void Day11::parse_universe(std::ifstream fp) {
	clear();
	std::string line;
	int64 x=0;
	int64 y=0;
	while(std::getline(fp,line)) {
		//std::cout << "line: " << line << std::endl;
		x = 0;
		for(char ch : line) {
			if(ch == '#') {
				Position p {x, y};
				//std::cout << "(" << p.x << "," << p.y << ")" << std::endl;
				universe.add_galaxy(p);
			}
			x++;
		}
		y++;
	}
}

bool Day11::part1() {
	try {
		parse_universe(getInputFile());
		if(test_mode)
			universe.print();
		universe.expand();
		if(test_mode)
			universe.print();
		int64 sum = 0;
		auto galaxies = universe.get_galaxies();
		for(int i = 0 ; i < galaxies.size() ; i++) {
			for(int j = i + 1 ; j < galaxies.size() ; j++) {
				auto g1 = galaxies[i];
				auto g2 = galaxies[j];
				int64 dist = std::abs(g1.x-g2.x) + std::abs(g1.y-g2.y);
				if(test_mode) {
					std::cout << "Distance between galaxy " << (i+1) << " and galaxy " << (j+1) << ": " << dist << std::endl;
				}
				sum += dist;
			}
		}
		std::cout << "Total sum of distances: " << sum << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

bool Day11::part2() {
	try {
		std::vector<int> factors;
		if(test_mode) {
			factors.push_back(2);
			factors.push_back(10);
			factors.push_back(100);
			factors.push_back(1000);
			factors.push_back(10000);
			factors.push_back(100000);
		}
		factors.push_back(1000000);
		for(int f : factors) {
			parse_universe(getInputFile());
			if(test_mode)
				universe.print();
			universe.expand(f);
			int64 sum = 0;
			auto galaxies = universe.get_galaxies();
			for(int i = 0 ; i < galaxies.size() ; i++) {
				for(int j = i + 1 ; j < galaxies.size() ; j++) {
					auto g1 = galaxies[i];
					auto g2 = galaxies[j];
					int64 dist = std::abs(g1.x-g2.x) + std::abs(g1.y-g2.y);
					sum += dist;
				}
			}
			std::cout << "Expansion factor: " << f << std::endl;
			std::cout << "Total sum of distances: " << sum << std::endl;
		}
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

Day11 *day11_create(bool test) {
	return new Day11(test);
}
