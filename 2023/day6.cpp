#include <iostream>
#include <fstream>
#include <vector>
#include <math.h>

#include "AoC.h"

class Day6 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
};

namespace Day6NS {
	class Race {
		public:
		double getBestButtonPressTime();
		double getButtonPressTime(double d);
		const double getTime() { return time; }
		const double getDistance() { return dist; }
		Race(double time, double dist);
		private:
		double time;
		double dist;
	};

	Race::Race(double time, double dist) : time(time), dist(dist) { }
	
	double Race::getButtonPressTime(double d) {
		double radicand  = (double)(time * time - 4 * d);
		double x1 = (-1*time + sqrt(radicand)) / -2;
		double x2 = (-1*time - sqrt(radicand)) / -2;
		if(x1 < x2) return x1;
		return x2;
	}

	double Race::getBestButtonPressTime() {
		return (double)time / 2;
	}

	std::vector<Race> parse_races(std::ifstream& fp) {
		std::vector<double> times;
		std::vector<double> distances;
		std::string line;
		while(std::getline(fp,line)) {
			if (line.substr(0,5) == "Time:") {
				auto spl = string_split(line,":");
				string_trim(spl[1]);
				for(auto &t : string_split(spl[1]," ")) {
					if(t == "") continue;
					auto tmp = t;
					string_trim(tmp);
					times.push_back(std::stod(tmp));
				}
			} else if (line.substr(0,9) == "Distance:") {
				auto spl = string_split(line,":");
				string_trim(spl[1]);
				for(auto &t : string_split(spl[1]," ")) {
					if(t == "") continue;
					auto tmp = t;
					string_trim(tmp);
					distances.push_back(std::stod(tmp));
				}
			}
		}
		std::vector<Race> races;
		for(int i=0;i<times.size();i++) {
			races.push_back(Race(times[i],distances[i]));
		}
		return races;
	}
};

bool Day6::part1() {
	try {
		auto races = Day6NS::parse_races(getInputFile());
		int64 product = 1;
		for(auto &r : races) {
			double bbpt = r.getBestButtonPressTime();
			double bpt = r.getButtonPressTime(r.getDistance());
			int64 this_ways = (floor(bbpt) - floor(bpt))*2;
			if(((int64)r.getTime() & 1) == 0) this_ways--;
			product *= this_ways;
			if(test_mode) {
				std::cout << "best button press time: " << bbpt << std::endl;
				std::cout << "button press time for distance " << r.getDistance() << ": " << bpt << std::endl;
				std::cout << "Race (" << r.getTime() << "," << r.getDistance() << "): " << this_ways << " ways to win." << std::endl;
			}
		}
		std::cout << product << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
		return false;
	}
	return true;
}

bool Day6::part2() {
	try {
		auto races = Day6NS::parse_races(getInputFile());
		int64 product = 1;
		std::string s_big_race_time = "";
		std::string s_big_race_dist = "";
		for(auto &r : races) {
			s_big_race_time += std::to_string((int)r.getTime());
			s_big_race_dist += std::to_string((int)r.getDistance());
		}
		auto r = Day6NS::Race(std::stod(s_big_race_time), std::stod(s_big_race_dist));

		double bbpt = r.getBestButtonPressTime();
		double bpt = r.getButtonPressTime(r.getDistance());
		int64 this_ways = (floor(bbpt) - floor(bpt))*2;
		if(((int64)r.getTime() & 1) == 0) this_ways--;
		product *= this_ways;
		if(test_mode) {
			std::cout << "best button press time: " << bbpt << std::endl;
			std::cout << "button press time for distance " << r.getDistance() << ": " << bpt << std::endl;
			std::cout << "Race (" << r.getTime() << "," << r.getDistance() << "): " << this_ways << " ways to win." << std::endl;
		}
		std::cout << product << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
		return false;
	}
	return true;
}

Day6 *day6_create() {
	return new Day6;
}
