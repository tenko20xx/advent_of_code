#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

#include "AoC.h"

class Day18 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
	struct Instruction {
		char dir;
		int depth;
		unsigned int color;
	};
	struct Bounds {
		Position min;
		Position max;
	};
	struct PointI64 {
		int64 x;
		int64 y;
	};
	struct Polygon {
		std::vector<PointI64> vertices;
		int64 area() {
			int64 sum = 0;
			for(auto it = vertices.begin(); it+1 != vertices.end(); it++) {
				PointI64 p = *it;
				PointI64 np = *(it+1);
				int64 s = (p.x * np.y) - (np.x * p.y);
				sum += s;
			}
			return sum/2;
		}
		void clear() {
			vertices.clear();
		}
	};
	class Plan {
		public:
		void clear();
		void init(std::vector<std::string>,bool from_color = false);
		std::vector<Instruction> get_instructions() { return instructions; }
		int get_width() { return bounds.max.col - bounds.min.col; }
		int get_height() { return bounds.max.row - bounds.min.row; }
		Bounds get_bounds() { return bounds; }
		void draw_dig();
		void auto_fill();
		void fill(Position, char);
		int count_fill();
		int64 fill_area() { return poly.area(); }
		void print_poly();
		private:
		Polygon poly;
		Bounds bounds;
		int inst_idx;
		std::vector<Instruction> instructions;
		char* dig_data;
		int pos_idx(Position);
	} plan;
	void parse_plan(std::ifstream&,bool from_color = false);
};

int Day18::Plan::pos_idx(Position p) {
	int r = p.row - bounds.min.row;
	int c = p.col - bounds.min.col;
	return r * get_width() + c;
}

void Day18::Plan::clear() {
	if(get_width() != 0 && get_height() != 0) {
		delete[] dig_data;
	}
	bounds.min.row = 0;
	bounds.min.col = 0;
	bounds.max.row = 0;
	bounds.max.col = 0;
	inst_idx = 0;
	instructions.clear();
	poly.clear();
}

void Day18::Plan::init(std::vector<std::string> lines, bool from_color) {
	clear();
	Position pos = {0, 0};
	poly.vertices.push_back({pos.row,pos.col});
	char prev_d = ' ';
	char prev_turn = ' ';
	for(auto line : lines) {
		char this_turn = ' ';
		auto parts = string_split(line," ");
		Instruction i;
		i.dir = parts[0][0];
		i.depth = std::stoi(parts[1]);
		auto hex = parts[2].substr(2,parts[2].length()-1);
		std::istringstream(hex) >> std::hex >> i.color;
		if(from_color) {
			i.depth = i.color >> 4;
			int diri = i.color & 0xf;
			if(diri == 0) i.dir = 'R';
			if(diri == 1) i.dir = 'D';
			if(diri == 2) i.dir = 'L';
			if(diri == 3) i.dir = 'U';
		}
		instructions.push_back(i);
		if(i.dir == 'U') {
			pos.row -= i.depth;
		}
		if(i.dir == 'R') {
			pos.col += i.depth;
		}
		if(i.dir == 'D') {
			pos.row += i.depth;
		}
		if(i.dir == 'L') {
			pos.col -= i.depth;
		}
		//std::cout << pos.string() << std::endl;
		poly.vertices.push_back({pos.col,pos.row});
		if(pos.row < bounds.min.row) bounds.min.row = pos.row;
		if(pos.row + 1 > bounds.max.row) bounds.max.row = pos.row + 1;
		if(pos.col < bounds.min.col) bounds.min.col = pos.col;
		if(pos.col + 1 > bounds.max.col) bounds.max.col = pos.col + 1;
		prev_d = i.dir;
		prev_turn = this_turn;
	}
	auto prev_p = poly.vertices.begin();
	for(auto p = poly.vertices.begin()+1; p != poly.vertices.end() ; p++) {
		if(p->y > prev_p->y) {
			p->x++;
			prev_p->x++;
		}
		else if(p->x < prev_p->x) {
			p->y++;
			prev_p->y++;
		}
		prev_p = p;
	}
	/*
	dig_data = new char[get_width() * get_height()];
	for(int i = 0 ; i < get_width() * get_height() ; i++) dig_data[i] = ' ';
	pos = {0, 0};
	for(auto instr : instructions) {
		Position next_pos(pos);
		if(instr.dir == 'U') next_pos.row -= instr.depth;
		if(instr.dir == 'R') next_pos.col += instr.depth;
		if(instr.dir == 'D') next_pos.row += instr.depth;
		if(instr.dir == 'L') next_pos.col -= instr.depth;
		while(pos != next_pos) {
			dig_data[pos_idx(pos)] = '#';
			if(next_pos.row < pos.row) pos.row--;
			else if(next_pos.row > pos.row) pos.row++;
			else if(next_pos.col < pos.col) pos.col--;
			else if(next_pos.col > pos.col) pos.col++;
		}
	}
	auto_fill();
	*/
}



void Day18::Plan::draw_dig() {
	for(int r = 0 ; r < get_height() ; r++) {
		for(int c = 0 ; c < get_width() ; c++) {
			std::cout << dig_data[r*get_width() + c];
		}
		std::cout << std::endl;
	}
}

void Day18::Plan::auto_fill() {
	Position pos(bounds.min);
	while(pos.col < bounds.max.col) {
		fill(pos,'.');
		pos.col++;
	}
	pos.col--;
	while(pos.row < bounds.max.row) {
		fill(pos,'.');
		pos.row++;
	}
	pos.row--;
	while(pos.col >= bounds.min.col) {
		fill(pos,'.');
		pos.col--;
	}
	pos.col++;
	while(pos.row >= bounds.min.row) {
		fill(pos,'.');
		pos.row--;
	}
	bool filled = false;
	for(int r = bounds.min.row ; r < bounds.max.row ; r++) {
		for(int c = bounds.min.col ; c < bounds.max.col ; c++) {
			if(dig_data[pos_idx(Position{r,c})] == ' ') {
				fill(Position{r,c},'#');
				filled = true;
				break;
			}

		}
		if(filled) break;
	}
}

void Day18::Plan::fill(Position pos, char c) {
	if(pos.row < bounds.min.row || pos.col < bounds.min.col ||
			pos.row >= bounds.max.row || pos.col >= bounds.max.col)
		return;
	if (dig_data[pos_idx(pos)] != ' ') return;
	dig_data[pos_idx(pos)] = c;
	fill(pos + Position {-1, 0},c);
	fill(pos + Position { 0, 1},c);
	fill(pos + Position { 1, 0},c);
	fill(pos + Position { 0,-1},c);
}

int Day18::Plan::count_fill() {
	int cnt = 0;
	for(int i=0; i<get_width()*get_height(); i++) {
		cnt += (dig_data[i] == '#' ? 1 : 0);
	}
	return cnt;
}

void Day18::Plan::print_poly() {
	for(auto p : poly.vertices) {
		std::cout << "(" << p.x << "," << p.y << ")" << std::endl;
	}
}

void Day18::parse_plan(std::ifstream& fp,bool from_color) {
	std::vector<std::string> lines;
	std::string line;
	while(std::getline(fp,line)) {
		string_trim(line);
		if(line == "") continue;
		lines.push_back(line);
	}
	plan.init(lines,from_color);
}

bool Day18::part1() {
	try {
		parse_plan(getInputFile());
		if(isVerbose()) {
			plan.print_poly();
			auto b = plan.get_bounds();
			std::cout << "bounds: " << b.min.string() << "->" << b.max.string() << std::endl;
		}
		//if(isVerbose()) plan.draw_dig();
		std::cout << "Dig site filled with " << plan.fill_area() << " cubic meters of lava." << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

bool Day18::part2() {
	try {
		parse_plan(getInputFile(),true);
		if(isVerbose()) {
			for(auto instr : plan.get_instructions()) {
				std::cout << instr.dir << " " << instr.depth << std::endl;
			}
			plan.print_poly();
			auto b = plan.get_bounds();
			std::cout << "bounds: " << b.min.string() << "->" << b.max.string() << std::endl;
		}
		std::cout << "Dig site filled with " << plan.fill_area() << " cubic meters of lava." << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

Day18 *day18_create() {
	return new Day18();
}
