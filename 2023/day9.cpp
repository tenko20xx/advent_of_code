#include <iostream>
#include <fstream>
#include <string>
#include <deque>
#include <sstream>

#include "AoC.h"

class Day9 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
	~Day9();
	private:
	typedef std::deque<int> History;
	std::deque<History*> histories;
	void parse_histories(std::ifstream& fp);
	int extrapolate(const History& h, bool backwards = false);
	bool all_equal(const History& h);
	History calc_differences(const History& h);
	void clear();
};

namespace Day9NS {

};

Day9::~Day9() {
	clear();
}

void Day9::clear() {
	for(auto &it : histories) delete it;
	histories.clear();
}

void Day9::parse_histories(std::ifstream& fp) {
	clear();
	std::string line;
	while(std::getline(fp,line)) {
		auto iss = std::istringstream(line);
		History *h = new History;
		int n;
		while(iss >> n) {
			h->push_back(n);
		}
		histories.push_back(h);
	}
}

int Day9::extrapolate(const History& h, bool backwards) {
	if(h.size() == 1) return h[0];
	auto diffs = calc_differences(h);
	if(all_equal(diffs)) {
		if(backwards) {
			return h.front() - diffs[0];
		} else {
			return h.back() + diffs[0];
		}
	}
	if(backwards) {
		return h.front() - extrapolate(diffs,backwards);
	}
	return h.back() + extrapolate(diffs);
}

Day9::History Day9::calc_differences(const History& h) {
	History diffs;
	if(h.size() <= 1) return diffs;
	for(auto it = h.begin()+1; it != h.end(); it++) {
		diffs.push_back(*it - *(it-1));
	}
	return diffs;
}

bool Day9::all_equal(const History& h) {
	if(h.size() <= 1) return true;
	int n = h[0];
	for(auto it = h.begin()+1; it != h.end(); it++) {
		if(*it != n) return false;
	}
	return true;
}

bool Day9::part1() {
	try {
		parse_histories(getInputFile());
		int sum = 0;
		for(auto &history : histories) {
			int next = extrapolate(*history);
			if(test_mode) {
				for(int &n : *history) {
					std::cout << n << " ";
				}
				std::cout << next << std::endl;
			}
			sum += next;
		}
		std::cout << "Sum of all extrapolated values: " << sum << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

bool Day9::part2() {
	try {
		parse_histories(getInputFile());
		int sum = 0;
		for(auto &history : histories) {
			int prev = extrapolate(*history,true);
			if(test_mode) {
				std::cout << prev << " ";
				for(int &n : *history) {
					std::cout << n << " ";
				}
				std::cout << std::endl;
			}
			sum += prev;
		}
		std::cout << "Sum of all extrapolated values: " << sum << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

Day9 *day9_create() {
	return new Day9;
}
