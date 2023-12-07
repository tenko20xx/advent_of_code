#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <map>

#include "AoC.h"

class Day7 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
};

namespace Day7NS {
	struct Hand {
		std::string cards;
		int bid;
	};

	bool use_jokers = false;

	std::map<char,int> RANKS = {
		{'2', 2},
		{'3', 3},
		{'4', 4},
		{'5', 5},
		{'6', 6},
		{'7', 7},
		{'8', 8},
		{'9', 9},
		{'T', 10},
		{'J', 11},
		{'Q', 12},
		{'K', 13},
		{'A', 14}
	};

	const std::map<std::string,int> HANDRANKS = {
		{"HighCard", 1},
		{"OnePair", 2},
		{"TwoPair", 3},
		{"ThreeOfAKind", 4},
		{"FullHouse", 5},
		{"FourOfAKind", 6},
		{"FiveOfAKind", 7}
	};

	std::map<char,int> rank_counts(std::string hand) {
		std::map<char,int> cnt;
		for(auto &c : hand) {
			cnt[c] = 0;
		}
		for(auto &c : hand) {
			cnt[c]++;
		}
		return cnt;
	}

	void enable_jokers() {
		use_jokers = true;
		RANKS['J'] = 1;
	}

	int get_hand_rank(std::string hand) {
		auto counts = rank_counts(hand);
		int max_cnt = 0;
		int pairs = 0;
		int jokers = 0;
		for(auto &pair : counts) {
			if(use_jokers && pair.first == 'J') {
				jokers = pair.second;
			} else {
				if(pair.second > max_cnt) max_cnt = pair.second;
				if(pair.second == 2) pairs++;
			}
		}
		if(max_cnt == 2 && jokers > 0) pairs--;
		max_cnt += jokers;
		if(max_cnt == 5) return HANDRANKS.at("FiveOfAKind");
		if(max_cnt == 4) return HANDRANKS.at("FourOfAKind");
		if(max_cnt == 3) {
			if(pairs >= 1) return HANDRANKS.at("FullHouse");
			return HANDRANKS.at("ThreeOfAKind");
		}
		if(max_cnt == 2) {
			if(pairs == 2) return HANDRANKS.at("TwoPair");
			return HANDRANKS.at("OnePair");
		}
		return HANDRANKS.at("HighCard");
	}
	
	struct HandCompare {
		bool operator()(Hand a, Hand b) {
			int hr_a = get_hand_rank(a.cards);
			int hr_b = get_hand_rank(b.cards);
			if(hr_a < hr_b) return true;
			if(hr_a == hr_b) {
				int i = 0;
				while(RANKS.at(a.cards[i]) == RANKS.at(b.cards[i]) && i < 5) i++;
				return RANKS.at(a.cards[i]) < RANKS.at(b.cards[i]);
			}
			return false;
		};
	} handCmp;

	std::vector<Hand> parse_hands(std::ifstream fp) {
		std::vector<Hand> hands;
		std::string line;
		while(std::getline(fp,line)) {
			auto spl = string_split(line," ");
			hands.push_back({spl[0], std::stoi(spl[1])});
		}
		return hands;
	}
};

bool Day7::part1() {
	try {
		auto hands = Day7NS::parse_hands(getInputFile());
		std::sort(hands.begin(), hands.end(), Day7NS::handCmp);
		int rank = 1;
		int total_winnings = 0;
		for(auto &h : hands) {
			int winnings = rank * h.bid;
			if(test_mode)
				std::cout << h.cards << "(" << Day7NS::get_hand_rank(h.cards) << ") - Rank " << rank << " | " << winnings << std::endl;
			total_winnings += winnings;
			rank++;
		}
		std::cout << "Total Winnings: " << total_winnings << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

bool Day7::part2() {
	try {
		Day7NS::enable_jokers();
		auto hands = Day7NS::parse_hands(getInputFile());
		std::sort(hands.begin(), hands.end(), Day7NS::handCmp);
		int rank = 1;
		int total_winnings = 0;
		for(auto &h : hands) {
			int winnings = rank * h.bid;
			if(test_mode || true)
				std::cout << h.cards << "(" << Day7NS::get_hand_rank(h.cards) << ") - Rank " << rank << " | " << winnings << std::endl;
			total_winnings += winnings;
			rank++;
		}
		std::cout << "Total Winnings: " << total_winnings << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

Day7 *day7_create(bool test) {
	return new Day7(test);
}
