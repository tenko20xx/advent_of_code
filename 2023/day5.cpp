#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <set>
#include <utility>

#include "AoC.h"

class Day5 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
};

namespace Day5NS {
	bool test_mode = false;

	struct Mapping {
		uint64 src;
		uint64 dst;
		uint64 range;
	};

	class Translation {
		public:
		uint64 get(uint64 src);
		uint64 get_reverse(uint64 dst);
		void add_map(uint64 src, uint64 dst, uint64 range);
		std::vector<uint64> get_srcs();
		private:
		std::vector<Mapping> mappings;
	};

	std::vector<uint64> Translation::get_srcs() {
		std::vector<uint64> srcs;
		for(auto &m : mappings) srcs.push_back(m.src);
		return srcs;
	}

	uint64 Translation::get(uint64 src) {
		for(auto &m : mappings) {
			if (src >= m.src && src < (m.src + m.range)) {
				uint64 offset = (src - m.src);
				//std::cout << src << " is between " << m.src << " and " << (m.src + m.range) << std::endl;
				//std::cout << "base destination for this mapping is " << m.dst << std::endl;
				//std::cout << "offset is " << offset << std::endl;
				return m.dst + offset;
			}
		}
		return src;
	}

	uint64 Translation::get_reverse(uint64 dst) {
		for(auto &m : mappings) {
			if (dst >= m.dst && dst < (m.dst + m.range)) {
				uint64 offset = (dst - m.dst);
				//std::cout << src << " is between " << m.src << " and " << (m.src + m.range) << std::endl;
				//std::cout << "base destination for this mapping is " << m.dst << std::endl;
				//std::cout << "offset is " << offset << std::endl;
				return m.src + offset;
			}
		}
		return dst;
	}

	void Translation::add_map(uint64 dst, uint64 src, uint64 range) {
		mappings.push_back({src,dst,range});
	}

	std::pair<std::vector<uint64>,std::map<std::string,Translation>> parse_translations(std::ifstream fp) {
		std::vector<uint64> seeds;
		std::string line;
		std::getline(fp,line);
		auto sn = string_split(line,":");
		if(sn[0] == "seeds") {
			string_trim(sn[1]);
			auto nums = string_split(sn[1]," ");
			for(auto &s : nums) {
				seeds.push_back(std::stoull(s));
			}
		} else {
			throw ParseException(1,"cannot parse seeds");
		}

		int li = 1;
		std::string this_mapping = "";
		std::map<std::string,Translation> trans;
		while(std::getline(fp,line)) {
			li++;
			string_trim(line);
			if(line == "") {
				this_mapping = "";
				continue;
			}
			if(this_mapping == "") {
				if(line.substr(line.length()-4) == "map:") {
					std::string map_name = string_split(line," ")[0];
					this_mapping = map_name;
					trans.insert({map_name,Translation()});
				} else {
					throw ParseException(li, "expected new mapping label");
				}
			} else {
				auto snums = string_split(line, " ");
				if(snums.size() != 3) {
					throw ParseException(li, "expected 3 numbers");
				}
				std::vector<uint64> nums;
				for(auto &n : snums) {
					nums.push_back(std::stoull(n));
				}
				trans[this_mapping].add_map(nums[0],nums[1],nums[2]);
			}
		}
		return {seeds, trans};
	}

	void resolve_to_location(std::map<std::string,Translation> &translations, const std::string mapping, const uint64 start_val) {
		auto map_def = string_split(mapping,"-to-");
		std::string last_mapping = map_def[0];
		uint64 last_val = start_val;
		std::cout << last_mapping << " " << last_val;
		while(last_mapping != "location") {
			for(auto &[key, trans] : translations) {
				auto map_def2 = string_split(key,"-to-");
				if (map_def2[0] == last_mapping) {
					last_val = trans.get(last_val);
					last_mapping = map_def2[1];
					std::cout << ", " << last_mapping << " " << last_val;
				}
			}
		}
		std::cout << "." << std::endl;
	}

	void resolve_from_location(std::map<std::string,Translation> &translations, const std::string mapping, const uint64 start_val) {
		std::vector<std::pair<std::string,uint64>> chain;
		auto map_def = string_split(mapping,"-to-");
		std::string last_mapping = map_def[1];
		uint64 last_val = start_val;
		chain.push_back({last_mapping, last_val});
		while (last_mapping != "seed") {
			for(auto &[key, trans] : translations) {
				auto map_def2 = string_split(key,"-to-");
				if (map_def2[1] == last_mapping) {
					last_val = trans.get_reverse(last_val);
					last_mapping = map_def2[0];
					chain.push_back({last_mapping, last_val});
				}
			}
		}
		bool first = true;
		for(auto it = chain.rbegin(); it != chain.rend(); it++) {
			if(!first) std::cout << ", ";
			std::cout << it->first << " " << it->second;
			first = false;
		}
		std::cout << "." << std::endl;
	}

	uint64 find_lowest_location(std::map<std::string,Translation> &trans, const std::string mapping, const uint64 start_val, const uint64 range) {
		if(test_mode) {
			std::cout << "Searching for lowest " << mapping << ": " << start_val << "->" << (start_val+range) << std::endl;
		}
		std::set<std::pair<uint64,uint64>> next_search;
		//if(test_mode) std::cout << "next search -> " << start_val << ":(" << trans[mapping].get(start_val) << "," << range << ")" << std::endl;
		next_search.insert({trans[mapping].get(start_val),range});
		for(auto src : trans[mapping].get_srcs()) {
			if(src >= start_val && src < (start_val + range)) {
				uint64 next_start_val = trans[mapping].get(src);
				uint64 next_range = range - (src - start_val);
				//if(test_mode) std::cout << "next search -> " << src << ":(" << next_start_val << "," << next_range << ")" << std::endl;
				next_search.insert({next_start_val,next_range});
			}
		}
		auto map_def = string_split(mapping,"-to-");
		if(map_def[1] == "location") {
			uint64 lowest = (*(next_search.begin())).first;
			for(auto &pair : next_search) {
				if(test_mode) {
					std::cout << "found " << mapping << ": " << pair.first << std::endl;
					resolve_from_location(trans, mapping, pair.first);
				}
				if(pair.first < lowest) lowest = pair.first;
			}
			return lowest;
		}
		std::string next_mapping;
		for(auto &[key, t] : trans) {
			auto map_def2 = string_split(key,"-to-");
			if (map_def[1] == map_def2[0]) {
				next_mapping = key;
				break;
			}
		}
		uint64 lowest;
		bool first = true;
		for(auto &[sv, r] : next_search) {
			uint64 nr = r;
			for(auto src : trans[mapping].get_srcs()) {
				if(src > sv) {
					uint64 tr = src - start_val;
					if(tr < nr) {
						nr = tr;
					}
				}
			}
			uint64 loc = find_lowest_location(trans, next_mapping, sv, nr);
			if (first || loc < lowest) {
				lowest = loc;
				first = false;
			}
		}
		return lowest;
	}
};

bool Day5::part1() {
	try {
		auto [seeds, translations] = Day5NS::parse_translations(getInputFile());
		if(test_mode) {
			//std::cout << "seed  soil" << std::endl;
			//for(uint64 i=0; i < 100; i++) { 
			//	std::cout << i << "    " << (i > 9 ? "" : " ") << translations["seed-to-soil"].get(i) << std::endl;
			//}
		}
		uint64 lowest_location;
		bool first = true;
		for(auto &seed : seeds) {
			//std::cout << "Seed number " << seed << " corresponds to soil number " << translations["seed-to-soil"].get(seed) << std::endl;
			std::string last_mapping = "seed";
			uint64 last_val = seed;
			if(test_mode) std::cout << "seed " << last_val;
			while(last_mapping != "location") {
				for(auto &[key, trans] : translations) {
					auto map_def = string_split(key,"-to-");
					if (map_def[0] == last_mapping) {
						last_val = trans.get(last_val);
						last_mapping = map_def[1];
						if(test_mode) std::cout << ", " << last_mapping << " " << last_val;
					}
				}
			}
			if(first) {
				lowest_location = last_val;
				first = false;
			} else {
				if(last_val < lowest_location) lowest_location = last_val;
			}
			if(test_mode) std::cout << "." << std::endl;
		}
		std::cout << "The lowest location number that corresponds to any of the initial seed numbers is " << lowest_location << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
		return false;
	}
	return true;
}

bool Day5::part2() {
	Day5NS::test_mode = test_mode;
	try {
		auto [seeds, translations] = Day5NS::parse_translations(getInputFile());
		if(test_mode) {
			//std::cout << "seed  soil" << std::endl;
			//for(uint64 i=0; i < 100; i++) { 
			//	std::cout << i << "    " << (i > 9 ? "" : " ") << translations["seed-to-soil"].get(i) << std::endl;
			//}
		}
		uint64 lowest_location;
		bool first = true;
		bool range = false;
		uint64 start_seed;
		for(auto &seed : seeds) {
			//std::cout << "Seed number " << seed << " corresponds to soil number " << translations["seed-to-soil"].get(seed) << std::endl;
			if(!range) {
				start_seed = seed;
				range = true;
			} else {
				std::vector<uint64> check_seeds = {start_seed};
				uint64 location = Day5NS::find_lowest_location(translations,"seed-to-soil",start_seed,seed);
				if(test_mode) {
					std::cout << "Starting from seed " << start_seed << " with range " << seed << std::endl;
					Day5NS::resolve_from_location(translations, "humidity-to-location", location);
				}
				if(location < lowest_location) {
					lowest_location = location;
				}
				range = false;
			}
		}
		std::cout << "The lowest location number that corresponds to any of the initial seed numbers is " << lowest_location << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
		return false;
	}
	return true;
}

Day5 *day5_create(bool test) {
	return new Day5(test);
}
