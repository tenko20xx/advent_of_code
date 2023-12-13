#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <vector>

#include "AoC.h"

class Day13 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
	struct Position {
		int row;
		int col;
	};
	class Pattern {
		public:
		Pattern(const std::vector<std::string>);
		~Pattern();
		std::string get_row(int n);
		std::string get_col(int n);
		int get_width();
		int get_height();
		void smudge(Position);
		void unsmudge();
		private:
		char* data;
		int width;
		int height;
		bool has_smudge;
		Position smudge_pos;
	};
	std::vector<Pattern*> patterns;
	void clear();
	void parse_patterns(std::ifstream fp);
	int find_vertical_reflection(Pattern&);
	int find_horizontal_reflection(Pattern&);
	std::set<int> find_vertical_reflections(Pattern&);
	std::set<int> find_horizontal_reflections(Pattern&);
	std::set<int> find_reflection_lines(std::vector<std::string>);
	std::vector<Position> find_smudges(Pattern&);
};

Day13::Pattern::Pattern(const std::vector<std::string> lines) {
	const int H = lines.size();
	const int W = lines[0].length();
	if(H == 0) std::cerr << "ERROR: 0 height" << std::endl;
	if(W == 0) std::cerr << "ERROR: 0 width" << std::endl;
	data = new char[H*W];
	height = H;
	width = W;
	for(int h = 0; h < height; h++) {
		for(int w = 0; w < width; w++) {
			data[h*width + w] = lines[h][w];
		}
	}
}

Day13::Pattern::~Pattern() {
	delete data;
}

std::string Day13::Pattern::get_row(int n) {
	if(n < 0 || n >= height) return "";
	std::string row = "";
	for(int i=0;i<width;i++) {
		row += data[n*width + i];
	}
	return row;
}

std::string Day13::Pattern::get_col(int n) {
	if(n < 0 || n >= width) return "";
	std::string col = "";
	for(int i=0;i<height;i++) {
		col += data[i*width + n];
	}
	return col;
}

int Day13::Pattern::get_width() {
	return width;
}

int Day13::Pattern::get_height() {
	return height;
}

void Day13::Pattern::smudge(Position p) {
	if(has_smudge) unsmudge();
	if(p.row >= 0 && p.row < height && p.col >= 0 && p.col < width) {
		int idx = p.row * width + p.col;
		char orig = data[idx];
		if(orig == '.') data[idx] = '#';
		else data[idx] = '.';
		has_smudge = true;
		smudge_pos = p;
	}
}

void Day13::Pattern::unsmudge() {
	if(!has_smudge) return;
	int idx = smudge_pos.row * width + smudge_pos.col;
	char orig = data[idx];
	if(orig == '.') data[idx] = '#';
	else data[idx] = '.';
	has_smudge = false;
}

void Day13::clear() {
	for(auto p : patterns) {
		delete p;
	}
	patterns.clear();
}

void Day13::parse_patterns(std::ifstream fp) {
	//std::cout << "parse_patterns" << std::endl;
	clear();
	std::string line;
	std::vector<std::string> lines;
	while(std::getline(fp,line)) {
		string_trim(line);
		if(line == "") {
			if(lines.size() == 0) continue;
			Pattern* p = new Pattern(lines);
			patterns.push_back(p);
			lines.clear();
		} else {
			lines.push_back("" + line);
		}
	}
	if(lines.size() > 0) {
		Pattern* p = new Pattern(lines);
		patterns.push_back(p);
	}
}

int Day13::find_vertical_reflection(Pattern &p) {
	//std::cout << "find_vertical_reflection" << std::endl;
	std::vector<std::string> lines;
	for(int col = 0 ; col < p.get_width() ; col++) {
		std::string img = p.get_col(col);
		lines.push_back(img);
	}
	auto reflection_lines = find_reflection_lines(lines);
	if(reflection_lines.size() == 1) return *(reflection_lines.begin());
	return 0;
}

int Day13::find_horizontal_reflection(Pattern &p) {
	//std::cout << "find_horizontal_reflection" << std::endl;
	std::vector<std::string> lines;
	for(int row = 0 ; row < p.get_height() ; row++) {
		std::string img = p.get_row(row);
		lines.push_back(img);
	}
	auto reflection_lines = find_reflection_lines(lines);
	if(reflection_lines.size() == 1) return *(reflection_lines.begin());
	return 0;
}

std::set<int> Day13::find_vertical_reflections(Pattern &p) {
	//std::cout << "find_vertical_reflection" << std::endl;
	std::vector<std::string> lines;
	for(int col = 0 ; col < p.get_width() ; col++) {
		std::string img = p.get_col(col);
		lines.push_back(img);
	}
	auto reflection_lines = find_reflection_lines(lines);
	return reflection_lines;
}

std::set<int> Day13::find_horizontal_reflections(Pattern &p) {
	//std::cout << "find_horizontal_reflection" << std::endl;
	std::vector<std::string> lines;
	for(int row = 0 ; row < p.get_height() ; row++) {
		std::string img = p.get_row(row);
		lines.push_back(img);
	}
	auto reflection_lines = find_reflection_lines(lines);
	return reflection_lines;
}

std::set<int> Day13::find_reflection_lines(std::vector<std::string> lines) {
	std::set<int> reflection_lines;
	for(int i=1;i<lines.size();i++) {
		//std::cout << "Check line " << line << ":" << img << std::endl;
		//std::set<int> this_reflections;
		int h = i-1;
		int j = i;
		bool reflects = true;
		while(h >= 0 && j < lines.size()) {
			if(lines[h] != lines[j]) {
				reflects = false;
				break;
			}
			h--;
			j++;
		}
		if(reflects) {
			//std::cout << "reflects at line " << i << std::endl;
			reflection_lines.insert(i);
		}
	}
	return reflection_lines;
}

std::vector<Day13::Position> Day13::find_smudges(Pattern &p) {
	std::vector<Position> smudges;
	for(int r=0;r<p.get_height()-1;r++) {
		for(int r2=r+1;r2<p.get_height();r2++) {
			std::string line1 = p.get_row(r);
			std::string line2 = p.get_row(r2);
			int diffs = 0;
			int diff_i = -1;
			for(int i=0;i<line1.length();i++) {
				if(line1[i] != line2[i]) {
					diffs++;
					diff_i = i;
				}
			}
			if(diffs == 1) {
				//std::cout << "RDiff at rows (" << r << "," << (r2) << ") position " << diff_i << std::endl;
				//std::cout << line1 << std::endl;
				//std::cout << line2 << std::endl;
				smudges.push_back({r,diff_i});
				smudges.push_back({r2,diff_i});
			}
		}
	}
	for(int c=0;c<p.get_width()-1;c++) {
		for(int c2 = c+1; c2 < p.get_width(); c2++) {
			std::string line1 = p.get_col(c);
			std::string line2 = p.get_col(c2);
			int diffs = 0;
			int diff_i = -1;
			for(int i=0;i<line1.length();i++) {
				if(line1[i] != line2[i]) {
					diffs++;
					diff_i = i;
				}
			}
			if(diffs == 1) {
				//std::cout << "CDiff at columns (" << c << "," << c2 << ") position " << diff_i << std::endl;
				//std::cout << line1 << std::endl;
				//std::cout << line2 << std::endl;
				smudges.push_back({diff_i,c});
				smudges.push_back({diff_i,c2});
			}
		}
	}
	return smudges;
}

bool Day13::part1() {
	try {
		parse_patterns(getInputFile());
		int summary = 0;
		int done = 0;
		for(auto p : patterns) {
			if(test_mode) {
				std::cout << "Pattern " << (done + 1) << "/" << patterns.size() << std::endl;
			}
			int v_refl = find_vertical_reflection(*p);
			int h_refl = find_horizontal_reflection(*p);
			summary += v_refl + 100 * h_refl;
			if(test_mode) {
				std::cout << "Vertical reflection line: " << v_refl << std::endl;
				std::cout << "Horizontal reflection line: " << h_refl << std::endl;
			}
			done++;
		}
		std::cout << "Summary: " << summary << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

bool Day13::part2() {
	try {
		parse_patterns(getInputFile());
		int summary = 0;
		int done = 0;
		for(auto p : patterns) {
			if(test_mode) {
				std::cout << "Pattern " << (done + 1) << "/" << patterns.size() << std::endl;
			}
			int og_v_refl = find_vertical_reflection(*p);
			int og_h_refl = find_horizontal_reflection(*p);
			auto smudges = find_smudges(*p);
			for(auto s : smudges) {
				if(test_mode) std::cout << "Smudge: (" << s.row << "," << s.col << ")" << std::endl;
				p->smudge(s);
				auto s_v_refl = find_vertical_reflections(*p);
				auto s_h_refl = find_horizontal_reflections(*p);
				for(auto it = s_v_refl.begin() ; it != s_v_refl.end() ; ) {
					if(*it == og_v_refl) 
						it = s_v_refl.erase(it);
					else
						it++;
				}
				for(auto it = s_h_refl.begin() ; it != s_h_refl.end() ; ) {
					if(*it == og_h_refl)
						it = s_h_refl.erase(it);
					else
						it++;
				}
				int v_refl = 0;
				int h_refl = 0;
				if(s_v_refl.size() == 1) v_refl = *(s_v_refl.begin());
				if(s_h_refl.size() == 1) h_refl = *(s_h_refl.begin());
				if(v_refl > 0 || h_refl > 0) {
					summary += v_refl + 100 * h_refl;
					if(test_mode) {
						std::cout << "Vertical reflection line: " << v_refl << std::endl;
						std::cout << "Horizontal reflection line: " << h_refl << std::endl;
					}
					break;
				}
			}
			done++;
		}
		std::cout << "Summary: " << summary << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

Day13 *day13_create(bool test) {
	return new Day13(test);
}
