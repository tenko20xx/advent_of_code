#include <iostream>
#include <fstream>
#include <list>

#include "AoC.h"

class Day15 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
	private:
	struct Lens {
		std::string label;
		unsigned short focal;
	};
	typedef std::list<Lens> Box;
	std::vector<Box> boxes;
	unsigned char HASH(std::string);
};

unsigned char Day15::HASH(std::string s) {
	unsigned short h = 0;
	for(auto c : s) {
		if(c == '\n') continue;
		h += c;
		h *= 17;
		h = h % 256;
	}
	return (unsigned char)h;
}
bool Day15::part1() {
	auto &fp = getInputFile();
	std::string line;
	while(std::getline(fp,line)) {
		unsigned int hash_sum = 0;
		string_trim(line);
		if(line == "") continue;
		auto parts = string_split(line,",");
		for(auto part : parts) {
			unsigned char h = HASH(part);
			if(test_mode) std::cout << part << " -> " << (int)h << std::endl;
			hash_sum += h;
		}
		std::cout << "Sum of all hashes in line: " << hash_sum << std::endl;
	}
	return true;
}

bool Day15::part2() {
	auto &fp = getInputFile();
	std::string line;
	while(std::getline(fp,line)) {
		string_trim(line);
		if(line == "") continue;
		boxes.clear();
		for(int i=0;i<265;i++) boxes.push_back({});
		auto parts = string_split(line,",");
		for(auto part : parts) {
			unsigned short h;
			if(part.back() == '-') {
				std::string label = part.substr(0,part.length()-1);
				h = HASH(label);
				for(auto it = boxes[h].begin() ; it != boxes[h].end() ; it++) {
					if(it->label == label) {
						boxes[h].erase(it);
						break;
					}
				}
			} else {
				auto l_f = string_split(part,"=");
				std::string label = l_f[0];
				unsigned short focal = std::stoi(l_f[1]);
				h = HASH(label);
				bool found = false;
				for(auto it = boxes[h].begin() ; it != boxes[h].end() ; it++) {
					if(it->label == label) {
						it->focal = focal;
						found = true;
						break;
					}
				}
				if(!found) { 
					boxes[h].push_back({label,focal});
				}
			}
			if(test_mode) {
				std::cout << "After \"" << part << "\":" << std::endl;
				int bn = 0;
				for(auto box : boxes) {
					bn++;
					if(box.empty()) continue;
					std::cout << "Box " << bn << ": ";
					for(auto lens : box) {
						std::cout << "[" << lens.label << " " << lens.focal << "] ";
					}
					std::cout << std::endl;
				}
			}
		}
		int focus_power = 0;
		int bn = 0;
		for(auto box : boxes) {
			bn++;
			int slot = 0;
			for(auto lens : box) {
				slot++;
				int power = bn * slot * lens.focal;
				if(test_mode) std::cout << lens.label << ": " << power << std::endl;
				focus_power += power;
			}
		}
		std::cout << "Total focusing power: " << focus_power << std::endl;
	}
	return true;
}

Day15 *day15_create() {
	return new Day15;
}
