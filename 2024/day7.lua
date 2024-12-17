#!/usr/bin/env lua
-- day7.lua

require("aoc")
local day7 = {}

function day7.print_lol(lol) -- print a list of lists (lol)
	for i,l in ipairs(lol) do
		local s = nil
		for _,v in ipairs(l) do
			if s == nil then
				s = "{"
			else
				s = s .. ","
			end
			s = s .. v
		end
		s = s .. "}"
		print(i..":"..s)
	end
end

function day7.get_perm(opts,n)
	if n <= 0 then
		return {}
	end
	
	if n == 1 then
		local ret = {}
		for _,o in ipairs(opts) do table.insert(ret,{o}) end
		return ret
	end

	local perms = {}
	local subperms = day7.get_perm(opts,n-1)
	for _,sp in ipairs(subperms) do
		for _,o in ipairs(opts) do
			local this_sp = {o}
			for _,v in ipairs(sp) do
				table.insert(this_sp,v)
			end
			table.insert(perms,this_sp)
		end
	end
	return perms
end

function day7.process_input(f)
	local records = {}
	for l in f:lines() do
		local result, soperands = string.match(l,"^(.*): (.*)$")
		result = tonumber(result)
		local operands = {}
		for op in soperands:gmatch("%d+") do
			table.insert(operands,tonumber(op))
		end
		table.insert(records,{result=result,operands=operands})
	end
	return records
end

function day7.do_calculation(operands, operators)
	if #operands ~= (#operators + 1) then
		print("ERROR: Mismatch operators and operands ("..#operators..","..#operands..")")
		return 0
	end

	local res = operands[1]
	for i,op in ipairs(operators) do
		local n = operands[i+1]
		if op == "+" then
			res = res + n
		elseif op == "*" then
			res = res * n
		elseif op == "||" then
			res = tonumber(res .. n)
		else
			print("ERROR: Unknown operator: " .. op)
			return 0
		end
	end
	return res
end

function day7.part1(f)
	local records = day7.process_input(f)
	local operators = {"+","*"}
	local sum = 0
	for _,r in ipairs(records) do
		local op_perms = day7.get_perm(operators,#r.operands - 1)
		for _,ops in ipairs(op_perms) do
			local calc = day7.do_calculation(r.operands,ops)
			if calc == r.result then
				sum = sum + calc
				break
			end
		end
	end
	print("The sum of all correct operator sets is: " .. sum)
end

function day7.part2(f)
	local records = day7.process_input(f)
	local operators = {"+","*","||"}
	local sum = 0
	for _,r in ipairs(records) do
		local op_perms = day7.get_perm(operators,#r.operands - 1)
		for _,ops in ipairs(op_perms) do
			local calc = day7.do_calculation(r.operands,ops)
			if calc == r.result then
				sum = sum + calc
				break
			end
		end
	end
	print("The sum of all correct operator sets is: " .. sum)
end

AOC.register("day7","Day 7",day7.part1,day7.part2)
AOC.start()
