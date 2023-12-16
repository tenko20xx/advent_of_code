#include <iostream>
#include <fstream>
#include <vector>
#include <utility>
#include <map>

#include "AoC.h"

class Day12 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
	const bool DEBUGMSGS = false;
	typedef std::pair<std::string,std::vector<int>> Record;
	std::vector<Record> records;
	std::map<Record,int64> memo;
	void clear();
	void parse_records(std::ifstream& fp);
	void print_record(const Record&);
	int64 count_arrangements(const Record&);
	bool valid_record(const Record&);
	int find_spring(const std::string &str, int len, int start = 0);
	Record unfold(Record, int);
};

namespace Day12NS {

};

void Day12::clear() {
	records.clear();
}

void Day12::parse_records(std::ifstream& fp) {
	clear();
	std::string line;
	while(std::getline(fp,line)) {
		Record r;
		auto parts = string_split(line, " ");
		r.first = parts[0];
		auto nums = string_split(parts[1],",");
		for(auto sn : nums) {
			r.second.push_back(std::stoi(sn));
		}
		records.push_back(r);
	}
}

void Day12::print_record(const Record &r) {
	std::cout << r.first << " ";
	bool first = true;
	for(auto n : r.second) {
		if(!first) std::cout << ",";
		std::cout << n;
		first = false;
	}
	std::cout << std::endl;
}

int64 Day12::count_arrangements(const Record &r) {
	//std::cout << "count_arrangements ";
	//print_record(r);
	if(memo.find(r) != memo.end()) return memo.at(r);
	int64 count = 0;

	if(r.second.empty()) {
		for(auto ch : r.first) {
			if(ch == '#') {
				//std::cout << "X -> ";
				//print_record(r);
				memo[r] = 0;
				return 0;
			}
		}
		//std::cout << "1 -> ";
		//print_record(r);
		memo[r] = 1;
		return 1;
	}

	int sum = r.second.size()-1;
	for(auto n : r.second) sum += n;
	if(sum > r.first.length()) {
		//std::cout << "X -> ";
		//print_record(r);
		memo[r] = 0;
		return 0;
	}

	if(r.second[0] == 0) {
		if(r.first.length() == 0 && r.second.size() == 1) {
			//std::cout << "1 -> ";
			//print_record(r);
			memo[r] = 1;
			return 1;
		}
		if(r.first[0] == '#') {
			//std::cout << "X -> ";
			//print_record(r);
			memo[r] = 0;
			return 0;
		}
		Record r_next;
		r_next.first = r.first;
		r_next.first = '.' + r_next.first.substr(1);
		for(auto it = r.second.begin()+1; it != r.second.end(); it++)  r_next.second.push_back(*it);
		count = count_arrangements(r_next);
		//std::cout << count << " -> ";
		//print_record(r);
		memo[r] = count;
		return count;
	}

	int si = 0;
	while(si < r.first.length() && r.first[si] == '.') si++;
	if(si == r.first.length()) {
		//std::cout << "X -> ";
		//print_record(r);
		memo[r] = 0;
		return 0;
	}

	std::string ss = r.first.substr(si);
	if(ss.front() == '#') {
		Record r_next;
		r_next.first = ss.substr(1);
		r_next.second.push_back(r.second[0]-1);
		for(auto it = r.second.begin()+1; it != r.second.end(); it++)  r_next.second.push_back(*it);
		if(r_next.second[0] == 0) {
			count = count_arrangements(r_next);
			//std::cout << count << " -> ";
			//print_record(r);
			memo[r] = count;
			return count;
		}
		if(r_next.first.length() == 0 || r_next.first[0] == '.') {
			//std::cout << "X -> ";
			//print_record(r);
			memo[r] = 0;
			return 0;
		}
		r_next.first = '#' + r_next.first.substr(1);
		count = count_arrangements(r_next);
		//std::cout << count << " -> ";
		//print_record(r);
		memo[r] = count;
		return count;
	}
	Record r1;
	Record r2;
	for(auto n : r.second) {
		r1.second.push_back(n);
		r2.second.push_back(n);
	}
	r1.first = '.' + ss.substr(1);
	r2.first = '#' + ss.substr(1);
	count += count_arrangements(r1);
	count += count_arrangements(r2);
	//std::cout << count << " -> ";
	//print_record(r);
	memo[r] = count;
	return count;
}

/* slow and obsolete
int64 count_arrangements(const Record &r) {
	//std::cout << "count_arrangements ";
	//print_record(r);
	int count = 0;
	bool broken = false;
	for(int i=0;i<r.first.length();i++) {
		if(r.first[i] != '?') continue;
		broken = true;
		Record test;
		test.first = r.first;
		test.second = r.second;
		test.first[i] = '.';
		if(valid_record(test))
			count += count_arrangements(test);
		test.first[i] = '#';
		if(valid_record(test))
			count += count_arrangements(test);
		break;
	}
	if(!broken) {
		if(valid_record(r)) {
			if(DEBUGMSGS) {
				std::cout << "valid record: ";
				print_record(r);
			}
			return 1;
		}
	}
	return count;
}
*/
int Day12::find_spring(const std::string &str, int len, int start) {
	//std::cout << "find_spring(" << len << "," << start << ")" << std::endl;
	for(int i = start; i < str.length(); i++) {
		if(str[i] == '.') continue;
		int start_pos = i;
		bool all_q = true;
		while(i < str.length() && (str[i] == '#' || str[i] == '?')) {
			all_q = all_q && (str[i] == '?');
			if((i+1) - start_pos == len) {
				if((i+1) == str.length()) return start_pos;
				if(str[(i+1)] == '#') break;
				return start_pos;
			}
			i++;
		}
		if(!all_q) return -1;
	}
	return -1;
}

bool Day12::valid_record(const Record &r) {
	if(DEBUGMSGS) {
		std::cout << "check_validity ";
		print_record(r);
	}
	/*
	int check = 0;
	int start = 0;
	for(int i=start;i<r.first.length();i++) {
		if(r.first[i] == '.') continue;
		int expect = r.second[check];
		int observed = 0;
		bool all_q = true;
		while(i < r.first.length() && (r.first[i] == '#' || r.first[i] == '?')) {
			observed++;
			i++;
			if(observed == expect) break;
			all_q = (r.first[i] == '?');
		}
		if(i < r.first.length()) {
			if(r.first[i] == '#') observed++;
		}
		if(observed != expect && all_q) continue;
		if(DEBUGMSGS) std::cout << "expect: " << expect << ", observed: " << observed << std::endl;
		if(observed != expect) return false;
		check++;
	}
	if(DEBUGMSGS) std::cout << check << " out of " << r.second.size() << " checks passed" << std::endl;
	return check == r.second.size();
	*/
	if(r.first.find('?') != r.first.npos) return true;
	int pos = 0;
	int checks_passed = 0;
	for(auto n : r.second) {
		int next_pos = find_spring(r.first,n,pos);
		if(next_pos == -1) {
			if(DEBUGMSGS) std::cout << n << "-spring not found after " << pos << std::endl;
			break;
		} else {
			if(DEBUGMSGS) std::cout << n << "-spring found at " << next_pos << std::endl;
		}
		checks_passed++;
		pos = next_pos + n + 1;
	}
	if(DEBUGMSGS) std::cout << checks_passed << " out of " << r.second.size() << " checks passed" << std::endl;
	if(checks_passed != r.second.size()) return false;
	for(int i=pos; i<r.first.length(); i++) {
		if(r.first[i] == '#') {
			if(DEBUGMSGS) std::cout << "extra springs found" << std::endl;
			return false;
		}
	}
	return true;
}

Day12::Record Day12::unfold(Record r, int times) {
	Record unfolded;
	unfolded.first = r.first;
	unfolded.second.insert(unfolded.second.begin(),r.second.begin(),r.second.end());
	for(int i=0;i<times-1;i++) {
		unfolded.first += "?" + r.first;
		unfolded.second.insert(unfolded.second.end(),r.second.begin(),r.second.end());
	}
	return unfolded;
}

bool Day12::part1() {
	try {
		parse_records(getInputFile());
		int sum = 0;
		for(auto r : records) {
			int c = count_arrangements(r);
			if(test_mode) {
				print_record(r);
				std::cout << "# of arrangements: " << c << std::endl;
			}
			sum += c;
		}
		std::cout << "Total number of arrangements: " << sum << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

bool Day12::part2() {
	try {
		const int NUM_UNFOLDS=5;
		parse_records(getInputFile());
		int64 sum = 0;
		int num_counted = 0;
		for(auto r : records) {
			Record unfolded = unfold(r,NUM_UNFOLDS);
			int64 c = count_arrangements(unfolded);
			
			if(test_mode) {
				std::cout << c << " -> ";
				print_record(r);
				std::cout << "Record " << ++num_counted << " out of " << records.size() << " counted" << std::endl;
			}
			sum += c;
		}
		std::cout << "Total number of arrangements: " << sum << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

Day12 *day12_create() {
	return new Day12;
}
