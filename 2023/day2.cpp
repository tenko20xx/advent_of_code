#include <iostream>
#include <fstream>
#include <map>
#include <string>
#include <vector>
#include <exception>

#include "AoC.h"

class Day2 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
};

namespace Day2NS {
	typedef std::map<std::string,int> Handful;
	typedef std::vector<Handful> Game;

	std::map<int,Game> read_games(std::ifstream& fp) {
		std::map<int,Game> games;
		std::string line;
		int li = 1;
		while(std::getline(fp,line)) {
			auto g = string_split(line,":");
			if(g.size() != 2) {
				throw ParseException(li,"too many \":\"s");
			}
			if(g[0].substr(0,5) != "Game ") {
				throw ParseException(li,"expected line to start with \"Game \"");
			}
			int gid = std::stoi(g[0].substr(5));
			//std::cout << "Game ID: " << gid << std::endl;
			auto handfuls = string_split(g[1],";");
			Game game;
			for(auto &handful : handfuls) {
				Handful h;
				string_trim(handful);
				auto cubes = string_split(handful,",");
				for(auto &cube : cubes) {
					string_trim(cube);
					//std::cout << cube << std::endl;
					auto parts = string_split(cube," ");
					h[parts[1]] = std::stoi(parts[0]);
				}
				game.push_back(h);
			}
			games[gid] = game;
		}
		return games;
	}
};

bool Day2::part1() {
	try {
		std::map<std::string,int> max_cubes = {
			{"red", 12},
			{"green", 13},
			{"blue", 14}
		};
    		auto games = Day2NS::read_games(getInputFile());
		int id_sum = 0;
		for(auto &id_game : games) {
			int gid = id_game.first;
			Day2NS::Game game = id_game.second;
			bool possible_game = true;
			for(auto &handful : game) {
				for(auto &pair : max_cubes) {
					std::string color = pair.first;
					int count = pair.second;
					if(handful.find(color) != handful.end()) {
						if(handful[color] > count) {
							possible_game = false;
							break;
						}
					}
				}
				if(!possible_game) break;
			}
			if(possible_game) {
				if(verbosity >= 1) {
					std::cout << "Game " << gid << " is possible" << std::endl;
				}
				id_sum += gid;
			} else {
				if(verbosity >= 1) {
					std::cout << "Game " << gid << " is impossible" << std::endl;
				}
			}
		}
		std::cout << "Sum of the IDs of possible games: " << id_sum << std::endl;
	} catch(ParseException exc) {
		std::cerr << exc.what() << ": " << exc.getMessage() << std::endl;
		return false;
	}
	return true;
}

bool Day2::part2() {
	try {
    		auto games = Day2NS::read_games(getInputFile());
		int power_sum = 0;
		for(auto &id_game : games) {
			Day2NS::Handful minset = {
				{"red", 0},
				{"green", 0},
				{"blue", 0}
			};
			int gid = id_game.first;
			Day2NS::Game game = id_game.second;
			bool possible_game = true;
			for(auto &handful : game) {
				for(auto &pair : handful) {
					std::string color = pair.first;
					int count = pair.second;
					if(minset[color] < count) minset[color] = count;
				}
			}
			int power = minset["red"] * minset["green"] * minset["blue"];
			if(verbosity >= 1) {
				std::cout << "Game " << gid << " power: " << power << std::endl;
			}
			power_sum += power;
		}
		std::cout << "Sum of the power of each game set: " << power_sum << std::endl;
	} catch(ParseException exc) {
		std::cerr << exc.what() << ": " << exc.getMessage() << std::endl;
		return false;
	}
	return true;
}

Day2 *day2_create() {
    return new Day2;
}
