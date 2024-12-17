#!/usr/bin/env lua
-- day5.lua

require("aoc")
local day5 = {}

function day5.repr_update(update)
	s = ""
	for _,p in ipairs(update) do
		if s ~= "" then s = s .. " -> " end
		s = s .. p
	end
	return s
end

function day5.parse_orderings_updates(f)
	local orderings = {}
	for line in f:lines() do
		if line:gsub("^%s*$","") == "" then
			break
		end
		local p1,p2 = line:match("(%d+)|(%d+)")
		p1 = tonumber(p1)
		p2 = tonumber(p2)
		if orderings[p1] == nil then
			orderings[p1] = {}
		end
		table.insert(orderings[p1],p2)
	end

	local updates = {}
	for line in f:lines() do
		local this_update = {}
		for p in line:gmatch("%d+") do
			table.insert(this_update,tonumber(p))
		end
		table.insert(updates,this_update)
	end

	if AOC.debug then
		for k,v in pairs(orderings) do
			print("page " .. k .. " appears before:")
			for _,p in ipairs(v) do
				print("  " .. p)
			end
		end

		print("updates:")
		for _,upd in ipairs(updates) do
			print(day5.repr_update(upd))
		end
	end
	return orderings, updates
end

function day5.get_first_update_correction(ord,upd)
	for i = 2, #upd do
		local this_page = upd[i]
		if ord[this_page] ~= nil then
			for j = 1, i do
				local check_page = upd[j]
				if AOC.list_contains(ord[this_page],check_page) then
					return {j,i}
				end
			end
		end
	end
	return nil
end

function day5.is_update_valid(ord,upd)
	return day5.get_first_update_correction(ord,upd) == nil
end

function day5.part1(f)
	local orderings,updates = day5.parse_orderings_updates(f)
	local middle_page_sum = 0
	for _,upd in ipairs(updates) do
		local valid_update = day5.is_update_valid(orderings,upd)
		if valid_update then
			AOC.tprint(day5.repr_update(upd) .. " is valid")
			local middle = upd[(#upd+1)//2]
			AOC.tprint("Middle value: " .. middle)
			middle_page_sum = middle_page_sum + middle
		else
			AOC.tprint(day5.repr_update(upd) .. " is invalid")
		end
	end
	print("The middle page sum is: " .. middle_page_sum)
end

function day5.part2(f)
	local orderings,updates = day5.parse_orderings_updates(f)
	local middle_page_sum = 0
	for _,upd in ipairs(updates) do
		local has_corrections = false
		local correction = day5.get_first_update_correction(orderings,upd)
		while correction ~= nil do
			has_corrections = true
			AOC.tprint(day5.repr_update(upd))
			AOC.tprint(upd[correction[1]] .. " should be after " .. upd[correction[2]])
			for i = correction[2], correction[1]+1,-1 do
				upd[i], upd[i-1] = upd[i-1], upd[i]
				AOC.dprint(day5.repr_update(upd))
			end
			correction = day5.get_first_update_correction(orderings,upd)
		end
		if has_corrections then
			local middle = upd[(#upd+1)//2]
			AOC.tprint(day5.repr_update(upd))
			AOC.tprint("Middle value: " .. middle)
			middle_page_sum = middle_page_sum + middle
		end
	end
	print("The middle page sum is: " .. middle_page_sum)
end

AOC.register("day5","Day 5",day5.part1,day5.part2)
AOC.start()

