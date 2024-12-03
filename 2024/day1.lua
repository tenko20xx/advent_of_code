#!/usr/bin/env lua

require "aoc"
local day1 = {}

function day1.count_each(list)
	vals = {}
	table.sort(list)
	i = 1
	while i <= #list do
		this_val = list[i]
		count = 1
		while list[i+1] == this_val do 
			count = count + 1
			i = i + 1
		end
		vals[this_val] = count
		i = i + 1
	end
	return vals
end

function day1.part1(f)
	list1 = {}
	list2 = {}
	for line in f:lines() do
		local n1, n2 = line:match("(%d+)%s+(%d+)")
		if n1 and n2 then 
			table.insert(list1,tonumber(n1)) 
			table.insert(list2,tonumber(n2)) 
		end
	end

	table.sort(list1)
	table.sort(list2)
	sum = 0
	for i,n1 in ipairs(list1) do
		n2 = list2[i]
		d = math.abs(n1 - n2)
		AOC.tprint(i .. " -> " .. n1 .. ":" .. n2 .. ":" .. d)
		sum = sum + d
	end
	print("sum: " .. sum)
end

function day1.part2(f)
	list1 = {}
	list2 = {}
	for line in f:lines() do
		local n1, n2 = line:match("(%d+)%s+(%d+)")
		if n1 and n2 then 
			table.insert(list1,tonumber(n1)) 
			table.insert(list2,tonumber(n2)) 
		end
	end

	uniq1 = day1.count_each(list1)
	uniq2 = day1.count_each(list2)
	score = 0
	for k,v in pairs(uniq1) do
		if uniq2[k] == nil then uniq2[k] = 0 end
		p = k * v * uniq2[k]
		AOC.tprint(k .. ":" .. v .. ":" .. uniq2[k] .. ":" .. p)
		score = score + p
	end
	print("similarity score: " .. score)
end

AOC.register("day1","Day 1",day1.part1,day1.part2)
AOC.start()
