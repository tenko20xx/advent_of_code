#include <iostream>
#include <fstream>
#include <map>
#include <set>
#include <string>
#include <iterator>
#include <algorithm>

#include "AoC.h"

class Day4 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
};

namespace Day4NS {
	class Card {
		public:
		std::set<int> get_your_winning_numbers();
		Card(std::set<int>, std::set<int>);
		private:
		int id;
		std::set<int> winning_numbers;
		std::set<int> your_numbers;
	};
	std::set<int> Card::get_your_winning_numbers() {
		std::set<int> intersection;
		std::set_intersection(winning_numbers.begin(), winning_numbers.end(),
				your_numbers.begin(), your_numbers.end(),
				std::inserter(intersection, intersection.end()));
		
		
		/*
		for(auto it1 = winning_numbers.begin(); it1 != winning_numbers.end(); it1++) {
			std::cout << "wn: " << *it1 << std::endl << "yn: ";
			for(auto it2 = your_numbers.begin(); it2 != your_numbers.end(); it2++) {
				std::cout << *it2 << " ";
				if(*it1 == *it2) {
					std::cout << "!";
					intersection.insert(*it2);
					break;
				}
			}
			std::cout << std::endl;
		}
		*/
		return intersection;
	}
	Card::Card(std::set<int> w, std::set<int> y) : winning_numbers(w), your_numbers(y) {
	}

	inline const bool is_digit(char ch) {
		return ch >= '0' && ch <= '9';
	}

	std::map<int,Card> parse_cards(std::ifstream fp) {
		std::string line;
		int li = 1;
		std::map<int,Card> cards;
		while(std::getline(fp,line)) {
			int card_id;
			auto spl1 = string_split(line,":");
			if(spl1.size() != 2) {
				throw ParseException(li,"expected 1 ':' in line");
			}
			if (spl1[0].substr(0,4) != "Card") {
				throw ParseException(li,"invalid card id section: " + spl1[0]);
			}
			std::string s_card_id = spl1[0].substr(4);
			string_trim(s_card_id);
			card_id = std::stoi(s_card_id);

			auto nums = string_split(spl1[1]," | ");
			if(nums.size() != 2) {
				throw ParseException(li,"expected 2 sets of numbers");
			}
			std::set<int> wn;
			std::set<int> yn;
			std::string buf;
			for(int i = 1; i <= nums[0].length(); i += 3) {
				buf = nums[0].substr(i,2);
				string_trim(buf);
				//std::cout << "wn: " << buf << std::endl;
				wn.insert(std::stoi(buf));
			}
			//std::cout << nums[1] << std::endl;
			for(int i = 0; i <= nums[1].length(); i += 3) {
				buf = nums[1].substr(i,2);
				string_trim(buf);
				//std::cout << "yn: " << buf << std::endl;
				yn.insert(std::stoi(buf));
			}

			cards.insert({card_id, Card(wn,yn)});
			li++;
		}
		return cards;
	}
};

bool Day4::part1() {
	try {
		auto cards = Day4NS::parse_cards(getInputFile());
		int total_pts = 0;
		for(auto &[card_id, card] : cards) {
			auto ywn = card.get_your_winning_numbers();
			int pts = 0; 
			if(ywn.size() > 0) {
				pts = 1 << (ywn.size()-1);
			}
			if(test_mode) {
				std::cout << "Card " << card_id << " winning numbers: ";
				if(ywn.size() == 0) {
					std::cout << "(none)";
				} else {
					for(auto n : ywn) {
						std::cout << n << " ";
					}
				}
				std::cout << " (" << pts << " pts)" << std::endl;
			}
			total_pts += pts;
		}
		std::cout << "The Elf's pile of scratchcards is worth " << total_pts << " points." << std::endl;
	} catch(ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
		return false;
	}
	return true;
}

bool Day4::part2() {
	try {
		auto cards = Day4NS::parse_cards(getInputFile());
		std::map<int,int> copies;
		int total_cards = 0;
		for(auto &[card_id, card]: cards) {
			copies.insert({card_id,1});
		}
		for(auto &[card_id, card] : cards) {
			auto ywn = card.get_your_winning_numbers();
			for(int i = 0; i < ywn.size(); i++) {
				copies[card_id + i + 1] += copies[card_id];
			}
			if(test_mode) {
				std::cout << copies[card_id] << " instance" << (copies[card_id] == 1 ? "" : "s") << " of card " << card_id << std::endl;
			}
			total_cards += copies[card_id];
		}
		std::cout << "Total scratchcards: " << total_cards << std::endl;
	} catch(ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
		return false;
	}
	return true;
}

Day4 *day4_create(bool test) {
	return new Day4(test);
}
