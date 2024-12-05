#!/usr/bin/env lua
-- day4.lua

require("aoc")
local day4 = {}

function day4.parse_grid(f)
	local grid = {}
	for line in f:lines() do
		local row = {}
		for c in line:gmatch(".") do
			table.insert(row,c)
		end
		table.insert(grid,row)
	end
	return grid
end

function day4.xmas_subgrids()
	local grids = {}
	local grid = {
		{'M','.','S'},
		{'.','A','.'},
		{'M','.','S'}
	}
	table.insert(grids,grid)
	for i = 1, 3 do
		grid = day4.grid_rot90(grid)
		table.insert(grids,grid)
	end
	return grids
end

function day4.grid_rot90(g)
	local new_grid = {}
	for r = 1, #g do
		local row = {}
		for c = 1, #g[r] do
			local rp = c
			local cp = (#g - r) + 1
			table.insert(row,g[rp][cp])
		end
		table.insert(new_grid,row)
	end
	return new_grid
end

function day4.str_to_subgrids(str)
	local subgrids = {}
	local dirs = {
		{ 0,  1},	-- horizontal forward
		{ 0, -1},	-- horizontal backwards
		{ 1,  0}, 	-- vertical forward
		{-1,  0}, 	-- vertical backwards
		{ 1,  1},	-- diagonals
		{-1, -1},
		{ 1, -1},
		{-1,  1}
	}
	for _,d in ipairs(dirs) do
		local sg = {}
		--print("dir",d[1],d[2])
		for r = 1, #str do
			--print("r",r)
			local row = {}
			for c = 1, #str do
				--print("c",c)
				local ch = '.'
				local rp = d[1] < 0 and ((#str + 1) - r) or r
				local cp = d[2] < 0 and ((#str + 1) - c) or c
				--print(rp,cp)
				if d[1] == 0 then
					ch = str:sub(cp,cp)
				elseif d[2] == 0 then
					ch = str:sub(rp, rp)
				elseif rp == cp then
					ch = str:sub(cp, cp)
				end
				table.insert(row,ch)
				if d[2] == 0 then
					break
				end
			end
			table.insert(sg, row)
			if d[1] == 0 then
				break
			end
		end
		table.insert(subgrids,sg)
	end
	return subgrids
end

function day4.grid_match_subgrid(grid, subgrid, row, col)
	for r = 1, #subgrid do
		for c = 1, #subgrid[r] do
			if subgrid[r][c] ~= '.' then
				local gr, gc = row + (r-1), col + (c-1)
				if gr > #grid or gc > #grid[gr] then
					return false
				end
				--print("subgrid["..r.."]["..c.."]="..(subgrid[r][c] or "nil").."|grid["..gr.."]["..gc.."]="..(grid[gr][gc] or "nil"))
				if subgrid[r][c] ~= grid[gr][gc] then
					return false
				end
			end
		end
	end
	return true
end

function day4.subgrid_search(grid, subgrid)
	local matches = {}
	for row = 1, #grid do
		for col = 1, #grid[row] do
			local match = day4.grid_match_subgrid(grid, subgrid, row, col)
			if match then
				table.insert(matches,{row,col})
			end
		end
	end
	return matches
end

function day4.print_grid(g)
	for r = 1, #g do
		local line = ""
		for c = 1, #g[r] do
			line = line .. g[r][c]
		end
		print(line)
	end
end

function day4.print_masked_grid(g, m)
	local mask = {}
	for r = 1, #g do
		local row = {}
		for c = 1, #g[r] do
			table.insert(row,'.')
		end
		table.insert(mask,row)
	end

	for _,match in ipairs(m) do
		local p = match[1]
		local sg = match[2]
		for r = 1, #sg do
			for c = 1, #sg[r] do
				local pr,pc = p[1] + (r-1), p[2] + (c-1)
				if sg[r][c] ~= '.' then
					mask[pr][pc] = g[pr][pc]
				end
			end
		end
	end
	day4.print_grid(mask)
end

function day4.solve(grid,subgrids)
	local matches = {}
	--day4.print_grid(grid)
	if AOC.debug then
		for i, sg in ipairs(subgrids) do
			print("** " .. i .. " **")
			day4.print_grid(sg)
		end
	end

	local x = 0
	for i, sg in ipairs(subgrids) do
		local this_matches = {}
		this_matches = day4.subgrid_search(grid,sg)
		x = x + #this_matches
		print(x)
		AOC.dprint("** SUBGRID-" .. i .. " **")
		AOC.dprint(#this_matches .. " matches")
		for _,m in ipairs(this_matches) do
			if AOC.debug then 
				print("match",m[1],m[2]) 
			end
			table.insert(matches,{m,sg})
		end
	end

	if AOC.test_mode or AOC.debug then
		day4.print_masked_grid(grid,matches)
	end
	return matches
end

function day4.part1(f)
	local grid = day4.parse_grid(f)
	local find = "XMAS"
	local subgrids = day4.str_to_subgrids(find)
	local matches = day4.solve(grid,subgrids)
	print(find .. " occurs a total of " .. #matches .. " times")
end

function day4.part2(f)
	local grid = day4.parse_grid(f)
	local subgrids = day4.xmas_subgrids(find)
	local matches = day4.solve(grid,subgrids)
	print("X-MAS occurs a total of " .. #matches .. " times")
end

AOC.register("day4","Day 4",day4.part1,day4.part2)
AOC.start()

