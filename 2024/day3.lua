#!/usr/bin/env lua
-- day3.lua

require("aoc")
local day3 = {}

function day3.part1(f)
	local contents = f:read("*all")
	local s = "("
	local sum = 0
	for m in contents:gmatch("mul%(%d%d?%d?,%d%d?%d?%)") do
		local n1, n2 = m:match("(%d+),(%d+)")
		if s ~= "(" then
			s = s .. " + "
		end
		s = s .. n1 .. "*" .. n2
		n1 = tonumber(n1)
		n2 = tonumber(n2)
		sum = sum + (n1 * n2)
	end
	s = s .. ")"
	AOC.tprint(s)
	print("sum: " .. sum)
end

function day3.part2(f)
	local contents = f:read("*all")
	if AOC.test_mode then
		contents = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
	end
	contents = contents:gsub("don't%(%).-do%(%)",""):gsub("don't%(%).-$","")
	AOC.dprint(contents)
	local s = "("
	local sum = 0
	for m in contents:gmatch("mul%(%d%d?%d?,%d%d?%d?%)") do
		local n1, n2 = m:match("(%d+),(%d+)")
		if s ~= "(" then
			s = s .. " + "
		end
		s = s .. n1 .. "*" .. n2
		n1 = tonumber(n1)
		n2 = tonumber(n2)
		sum = sum + (n1 * n2)
	end
	s = s .. ")"
	AOC.tprint(s)
	print("sum: " .. sum)
end

AOC.register("day3","Day 3",day3.part1,day3.part2)
AOC.start()

