#!/usr/bin/env lua
-- day2.lua

require("aoc")
local day2 = {}

function day2.get_diffs(list)
	local diffs = {}
	for i = 2, #list do
		table.insert(diffs,list[i] - list[i-1])
	end

	if AOC.debug then
		s = ""
		for _,v in ipairs(diffs) do s = s .. " " .. v end
		print("diffs: " .. s)
	end
	
	return diffs
end

function day2.all_same_sign(list)
	local sign = nil
	for _,v in ipairs(list) do
		if sign == nil then
			if v ~= 0 then 
				sign = v < 0 and -1 or 1
			end
		else
			vsign = v < 0 and -1 or 1
			if sign ~= vsign then
				return false
			end
		end
	end
	return true
end

function day2.all_within_mag(list,min,max)
	for _,v in ipairs(list) do
		m = math.abs(v)
		if m < min or m > max then
			return false
		end
	end
	return true
end

function day2.skip_levels(list)
	local new_list = {}
	for i = 1, #list do
		sublist = {}
		for j = 1, #list do
			if i ~= j then
				table.insert(sublist,list[j])
			end
		end
		table.insert(new_list,sublist)
	end
	if AOC.debug then
		print("Sublists:")
		for _,sl in ipairs(new_list) do
			s = ""
			for _,v in ipairs(sl) do
				s = s .. v .. " "
			end
			print(s)
		end
	end
	return new_list
end

function day2.solve(dampen)
	local f = AOC.get_input_file()
	local num_safe = 0
	for line in f:lines() do
		nums = {}
		for n in line:gmatch("%d+") do
			table.insert(nums,tonumber(n))
		end
		if dampen then
			AOC.dprint("dampening...")
			check = day2.skip_levels(nums)
		else
			check = {nums}
		end
		local safe = false
		for _,nums in ipairs(check) do
			local diffs = day2.get_diffs(nums)
			if day2.all_same_sign(diffs) and day2.all_within_mag(diffs,1,3) then
				safe = true
				break
			end
		end
		AOC.tprint((safe and "safe  " or "unsafe") .. "   " .. line)
		num_safe = num_safe + (safe and 1 or 0)
	end
	print(num_safe .. " reports are safe")
end

function day2.part1()
	day2.solve()
end

function day2.part2()
	day2.solve(true)
end

AOC.register("day2","Day 2",day2.part1,day2.part2)
AOC.start()
