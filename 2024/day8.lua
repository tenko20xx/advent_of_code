#!/usr/bin/env lua
-- day8.lua

require("aoc")
local day8 = {}

function day8.mk_map(f)
	local map = {ants={},width=0,height=0}
	local r, c = 0, 0
	for line in f:lines() do
		local row = {}
		r = r + 1
		c = 0
		for l in line:gmatch(".") do
			c = c + 1
			if l ~= "." then
				map.ants[day8.str_pos({r,c})] = l
			end
		end
		if map.width == 0 then
			map.width = c
		end
		map.height = map.height + 1
	end
	return map
end

function day8.repr_map(map,antinodes)
	s = ""
	local ant_dict = {}
	for r = 1, map.height do
		line = ""
		for c = 1, map.width do
			local spos = day8.str_pos({r,c})
			if map.ants[spos] then
				line = line .. map.ants[spos]
			elseif antinodes ~= nil and antinodes[spos] then
				line = line .. "#"
			else
				line = line .. "."
			end
		end
		s = s .. line .. "\n"
	end
	return s
end

function day8.hash_pos(map,pos)
	return map.width * (pos[1]-1) + (pos[2]-1)
end

function day8.unhash_pos(map,hash)
	return {(hash // map.width) + 1, (hash % map.width) + 1}
end

function day8.str_pos(pos)
	return pos[1] .. "," .. pos[2]
end

function day8.calc_antinodes(spos1,spos2)
	local p1, p2 = day8.pos_str(spos1), day8.pos_str(spos2)
	local dr = p2[1] - p1[1]
	local dc = p2[2] - p1[2]
	return {p1[1] - dr, p1[2] - dc}, {p2[1] + dr, p2[2] + dc}
end

function day8.is_in_bounds(map,pos)
	return pos[1] >= 1 and pos[1] <= map.height and pos[2] >= 1 and pos[2] <= map.width
end

function day8.calc_antinodes2(map,spos1,spos2)
	local p1, p2 = day8.pos_str(spos1), day8.pos_str(spos2)
	local dr = p2[1] - p1[1]
	local dc = p2[2] - p1[2]
	local antinodes = {}
	local pn = {p1[1], p1[2]}
	while day8.is_in_bounds(map,pn) do
		table.insert(antinodes,{pn[1],pn[2]})
		pn = {pn[1] - dr, pn[2] - dc}
	end
	pn = {p2[1], p2[2]}
	while day8.is_in_bounds(map,pn) do
		table.insert(antinodes,{pn[1],pn[2]})
		pn = {pn[1] + dr, pn[2] + dc}
	end
	return antinodes
end

function day8.add_antinode(tab,pos,freq)
	local spos = day8.str_pos(pos)
	if tab[spos] == nil then
		tab[spos] = {}
	end
	table.insert(tab[spos],freq)
end

function day8.pos_str(str)
	local n1, n2 = str:match("(-?%d+),(-?%d+)")
	return {tonumber(n1), tonumber(n2)}
end

function day8.part1(f)
	local map = day8.mk_map(f)
	if AOC.debug then
		print(day8.repr_map(map))
	end

	local antinodes = {}
	for apos,afreq in pairs(map.ants) do
		for bpos,bfreq in pairs(map.ants) do
			if apos ~= bpos and afreq == bfreq then
				an1, an2 = day8.calc_antinodes(apos,bpos)
				day8.add_antinode(antinodes,an1,afreq)
				day8.add_antinode(antinodes,an2,afreq)
			end
		end
	end
	if AOC.test_mode then
		print(day8.repr_map(map,antinodes))
	end
	local count = 0
	AOC.dprint("Antinodes:")
	for spos,freqs in pairs(antinodes) do
		local strout = "(" .. spos .. ")"
		local pos = day8.pos_str(spos)
		local oob = false
		if pos[1] < 1 or pos[2] < 1 or pos[1] > map.height or pos[2] > map.width then
			oob = true
			strout = strout .. "OUT"
		else
			count = count + 1
		end
		AOC.dprint("  " .. strout)
	end
	print("There are " .. count .. " uniquely positioned antinodes in-bounds")
end

function day8.part2(f)
	local map = day8.mk_map(f)
	if AOC.debug then
		print(day8.repr_map(map))
	end

	local antinodes = {}
	for apos,afreq in pairs(map.ants) do
		for bpos,bfreq in pairs(map.ants) do
			if apos ~= bpos and afreq == bfreq then
				local ans = day8.calc_antinodes2(map,apos,bpos)
				for _,an in ipairs(ans) do
					day8.add_antinode(antinodes,an,afreq)
				end
			end
		end
	end
	if AOC.test_mode then
		print(day8.repr_map(map,antinodes))
	end
	local count = 0
	AOC.dprint("Antinodes:")
	for spos,freqs in pairs(antinodes) do
		local strout = "(" .. spos .. ")"
		local pos = day8.pos_str(spos)
		local oob = false
		if pos[1] < 1 or pos[2] < 1 or pos[1] > map.height or pos[2] > map.width then
			oob = true
			strout = strout .. "OUT"
		else
			count = count + 1
		end
		AOC.dprint("  " .. strout)
	end
	print("There are " .. count .. " uniquely positioned antinodes in-bounds")
end

AOC.register("day8","Day 8",day8.part1,day8.part2)
AOC.start()

