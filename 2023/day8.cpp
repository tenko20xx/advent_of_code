#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <utility>
#include <numeric>

#include "AoC.h"

class Day8 : public AoC {
	public:
	using AoC::AoC;
	bool part1() override;
	bool part2() override;
	private:
	std::string::iterator instr_it;
	std::string instructions;

	struct Node {
		std::string name;
		Node *left;
		Node *right;
	};
	
	std::map<std::string,Node*> nodes;

	void parse_document(std::ifstream& fp);
	char get_next_instruction();
	void reset_instruction();
	void clear();
	bool all_nodes_end_in_z(std::vector<Node*>);
};

namespace Day8NS {

};

void Day8::clear() {
	for(auto &[key, val] : nodes) {
		delete val;
	}
	nodes.clear();
	instructions = "";
}

void Day8::reset_instruction() {
	instr_it = instructions.begin();
}

void Day8::parse_document(std::ifstream& fp) {
	clear();
	std::string line;
	std::getline(fp,line);
	instructions = line;
	std::getline(fp,line);

	// connections placeholder
	std::vector<std::pair<Node*,std::pair<std::string,std::string>>> conn_ph;
	while(std::getline(fp,line)) {
		auto parts = string_split(line," = ");
		auto node_name = parts[0];
		auto connections = parts[1].substr(1,parts[1].find(")")-1);
		auto conn_node_names = string_split(connections,", ");
		Node *node = new Node;
		node->name = node_name;
		//std::cout << "insert into nodes " << node->name << std::endl;
		nodes.insert({node->name,node});
		conn_ph.push_back({node,{conn_node_names[0],conn_node_names[1]}});
	}
	for(auto &it : conn_ph) {
		auto node = it.first;
		auto conns = it.second;
		//std::cout << "connect " << node->name << " to (" << conns.first << "," << conns.second << ")" << std::endl;
		node->left = nodes.at(conns.first);
		node->right = nodes.at(conns.second);
	}
	instr_it = instructions.begin();
}

char Day8::get_next_instruction() {
	if(instr_it == instructions.end()) instr_it = instructions.begin();
	return *(instr_it++);
}

bool Day8::all_nodes_end_in_z(std::vector<Node*> v) {
	for(auto &it : v) {
		if(it->name[2] != 'Z') return false;
	}
	return true;
}

bool Day8::part1() {
	try {
		parse_document(getInputFile());
		int steps = 0;
		char instr;
		Node *current = nodes.at("AAA");
		while(current->name != "ZZZ") {
			if(isVerbose())
				std::cout << (steps+1) << ":" << current->name << " -> ";
			instr = get_next_instruction();
			if(instr == 'L') current = current->left;
			if(instr == 'R') current = current->right;
			if(isVerbose())
				std::cout << current->name << std::endl;
			steps++;
		}
		std::cout << "Total steps taken to reach ZZZ: " << steps << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

bool Day8::part2() {
	try {
		parse_document(test_mode ? getInputFile("test2") : getInputFile());
		int steps = 0;
		char instr;
		std::vector<Node*> current_nodes;
		for(auto &[key, val] : nodes) {
			if(key[2] == 'A') current_nodes.push_back(val);
		}
		/** I don't think the naive way will finish in a reasonable time
		while(!all_nodes_end_in_z(current_nodes)) {
			instr = get_next_instruction();
			for(auto &n : current_nodes) {
				if(test_mode || true)
					std::cout << (steps+1) << ":" << n->name << " -> ";
				if(instr == 'L') n = n->left;
				if(instr == 'R') n = n->right;
				if(test_mode || true)
					std::cout << n->name << std::endl;
			}
			steps++;
		}
		**/
		std::vector<std::pair<Node*,int>> node_steps;
		for(auto &n : current_nodes) {
			Node* start_node = n;
			reset_instruction();
			steps = 0;
			while(n->name[2] != 'Z') {
				instr = get_next_instruction();
				if(isVerbose())
					std::cout << (steps+1) << ":" << n->name << " -> ";
				if(instr == 'L') n = n->left;
				if(instr == 'R') n = n->right;
				if(isVerbose())
					std::cout << n->name << std::endl;
				steps++;
			}
			node_steps.push_back({start_node,steps});
		}
		uint64 total_steps = 1;
		for(auto &it : node_steps) {
			int steps = it.second;
			if(isVerbose()) std::cout << (it.first)->name << " -- " << steps << std::endl;
			total_steps = (total_steps * steps) / std::gcd(total_steps,steps);
		}
		std::cout << "Total steps taken to reach all nodes ending in Z: " << total_steps << std::endl;
	} catch (ParseException exc) {
		std::cerr << exc.getMessage() << std::endl;
	}
	return true;
}

Day8 *day8_create() {
	return new Day8;
}
