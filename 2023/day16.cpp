#include <iostream>
#include <fstream>
#include <vector>
#include <list>
#include <queue>

#include "AoC.h"

class Day16 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
	struct Position {
		int row;
		int col;
		bool operator==(Position other) {
			return other.row == row && other.col == col;
		}
		Position operator+(Position other) {
			return {row + other.row, col + other.col};
		}	
		Position operator-(Position other) {
			return {row - other.row, col - other.col};
		}
		void operator+=(Position other) {
			row += other.row;
			col += other.col;
		}	
		void operator-=(Position other) {
			row -= other.row;
		       	col -= other.col;
		}
	};
	enum Direction : short {
		none   = 0,
		up     = 1,
		right  = 2,
		down   = 4,
		left   = 8
	};
	struct Beam {
		Position pos;
		Direction direction;
	};
	class Contraption {
		public:
		void init(std::vector<std::string>& lines);
		void reset_beams();
		void clear();
		char get_tile(int row, int col);
		char get_tile(Position p);
		int get_width();
		int get_height();
		void light(Beam);
		void print_tiles();
		void print_energized();
		void print_beams();
		int count_energized();
		Contraption() : width(0), height(0) { };
		private:
		char* tiles;
		short* beams;
		int width;
		int height;
		inline int get_idx(int row, int col) { return row * width + col; }
		inline int get_idx(Position p) { return p.row * width + p.col; }
	} contraption;
	void parse_contraption(std::ifstream&);
};

void Day16::Contraption::clear() {
	if(width != 0 && height != 0) {
		delete[] tiles;
		delete[] beams;
	}
	width = 0;
	height = 0;
}

void Day16::Contraption::init(std::vector<std::string>& lines) {
	clear();
	width = lines[0].length();
	height = lines.size();
	tiles = new char[width * height];
	beams = new short[width * height];
	for(int r = 0; r < height ; r++) {
		for(int c = 0 ; c < width ; c++) {
			tiles[get_idx(r,c)] = lines[r][c];
		}
	}
}

void Day16::Contraption::reset_beams() {
	for(int r = 0; r < height ; r++) {
		for(int c = 0 ; c < width ; c++) {
			beams[get_idx(r,c)] = 0;
		}
	}
}

char Day16::Contraption::get_tile(int row, int col) {
	return tiles[get_idx(row,col)];
}

char Day16::Contraption::get_tile(Position p) {
	return tiles[get_idx(p)];
}

int Day16::Contraption::get_width() {
	return width;
}

int Day16::Contraption::get_height() {
	return height;
}

void Day16::Contraption::light(Beam beam) {
	std::list<Beam> move_beams = {beam};
	std::list<Beam> add_beams;
	while(!move_beams.empty()) {
		add_beams.clear();
		for(auto it = move_beams.begin(); it != move_beams.end() ; ) {
			auto idx = get_idx(it->pos);
			if(it->pos.row < 0 || it->pos.col < 0 || it->pos.row >= height || it->pos.col >= width) {
				it = move_beams.erase(it);
				continue;
			}
			if((beams[idx] & it->direction) != 0) {
				it = move_beams.erase(it);
				continue;
			}
			beams[idx] = (beams[idx] | it->direction);
			if((it->direction == up || it->direction == down) && tiles[idx] == '-') {
				it->direction = left;
				add_beams.push_back({it->pos, right});
			}
			if ((it->direction == left || it->direction == right) && tiles[idx] == '|') {
				it->direction = up;
				add_beams.push_back({it->pos, down});
			}
			if (tiles[idx] == '\\') {
				if(it->direction == up) {
					it->direction = left;
				} else if (it->direction == left) {
					it->direction = up;
				} else if (it->direction == down) {
					it->direction = right;
				} else if (it->direction == right) {
					it->direction = down;
				}
			}
			if (tiles[idx] == '/') {
				if(it->direction == up) {
					it->direction = right;
				} else if (it->direction == left) {
					it->direction = down;
				} else if (it->direction == down) {
					it->direction = left;
				} else if (it->direction == right) {
					it->direction = up;
				}
			}
			it++;
		}
		move_beams.insert(move_beams.end(), add_beams.begin(), add_beams.end());
		for(auto it = move_beams.begin(); it != move_beams.end() ; it++) {
			if(it->direction == up) {
				it->pos.row -= 1;
			} else if (it->direction == left) {
				it->pos.col -= 1;
			} else if (it->direction == down) {
				it->pos.row += 1;
			} else if (it->direction == right) {
				it->pos.col += 1;
			}
		}
	}
}

void Day16::Contraption::print_tiles() {
	std::cout << "Tiles (" << get_height() << "x" << get_width() << "):" << std::endl;
	for(int r = 0 ; r < height ; r++) {
		for(int c = 0 ; c < width ; c++) {
			std::cout << get_tile(r,c);
		}
		std::cout << std::endl;
	}
	std::cout << "---" << std::endl;
}
void Day16::Contraption::print_energized() {
	std::cout << "Energized:" << std::endl;
	for(int r = 0 ; r < height ; r++) {
		for(int c = 0 ; c < width ; c++) {
			std::cout << (beams[get_idx(r,c)] == 0 ? "." : "#");
		}
		std::cout << std::endl;
	}
	std::cout << "---" << std::endl;
}
void Day16::Contraption::print_beams() {
	std::cout << "Beams:" << std::endl;
	for(int r = 0 ; r < height ; r++) {
		for(int c = 0 ; c < width ; c++) {
			char tile = get_tile(r,c);
			if(tile != '.') {
				std::cout << tile;
				continue;
			}
			int count = 0;
			short d = 1;
			short b = beams[get_idx(r,c)];
			while(d <= 8) {
				if((b & d) > 0) count++;
				d = d << 1;
			}
			if(count == 0) {
				std::cout << ".";
			} else if (count > 1) {
				std::cout << count;
			} else {
				if((b & 1) > 0) std::cout << "^";
				if((b & 2) > 0) std::cout << ">";
				if((b & 4) > 0) std::cout << "v";
				if((b & 8) > 0) std::cout << "<";
			}
		}
		std::cout << std::endl;
	}
	std::cout << "---" << std::endl;
}

int Day16::Contraption::count_energized() {
	int count = 0;
	for(int i = 0; i < width * height; i++) count += (beams[i] == 0 ? 0 : 1);
	return count;
}

void Day16::parse_contraption(std::ifstream& fp) {
	std::vector<std::string> lines;
	std::string line;
	while(std::getline(fp,line)) {
		string_trim(line);
		if(line == "") continue;
		lines.push_back(line);
	}
	contraption.init(lines);
}

bool Day16::part1() {
	try {
		parse_contraption(getInputFile());
		Beam start = {{0, 0}, right};
		contraption.light(start);
		if(verbosity >= 1) {
			contraption.print_tiles();
			contraption.print_beams();
			contraption.print_energized();
		}
		std::cout << "Total energized tiles: " << contraption.count_energized() << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

bool Day16::part2() {
	try {
		parse_contraption(getInputFile());
		std::queue<Beam> starting_beams;
		int last_row = contraption.get_height() -1;
		int last_col = contraption.get_width() -1;
		for(int r = 0 ; r < contraption.get_height() ; r++) {
			if(r == 0) {
				starting_beams.push({{r, 0}, down});
				starting_beams.push({{r, last_col}, down});
			}
			if(r == last_row) {
				starting_beams.push({{r, 0}, up});
				starting_beams.push({{r, last_col}, up});
			}
			starting_beams.push({{r, 0}, right});
			starting_beams.push({{r, last_col}, left});
		}
		for(int c = 0 ; c < contraption.get_width() ; c++) {
			starting_beams.push({{0, c}, down});
			starting_beams.push({{last_row, up}, left});
		}
		int max_energy = -1;
		Beam best_beam;
		while(!starting_beams.empty()) {
			Beam start = starting_beams.front();
			starting_beams.pop();
			contraption.reset_beams();
			contraption.light(start);
			int energy = contraption.count_energized();
			if(energy > max_energy) {
				max_energy = energy;
				best_beam = start;
			}
		}
		contraption.reset_beams();
		contraption.light(best_beam);
		if(verbosity >= 1) {
			std::cout << "Best beam: <(" << best_beam.pos.row << "," << best_beam.pos.col << ") ";
		       	switch(best_beam.direction) {
			 	case 0:
				       std::cout << "none";
				       break;
				case 1:
				       std::cout << "up";
				       break;
				case 2:
				       std::cout << "right";
				       break;
				case 4:
				       std::cout << "down";
				       break;
				case 8:
				       std::cout << "left";
				       break;
				default:
				       std::cout << "???";
				       break;
			}
			std::cout << ">" << std::endl;
			contraption.print_tiles();
			contraption.print_beams();
			contraption.print_energized();
		}
		std::cout << "Total energized tiles: " << contraption.count_energized() << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

Day16 *day16_create() {
	return new Day16;
}
