#!/usr/bin/env lua
-- day6.lua

require("aoc")
local day6 = {}

function day6.mk_map(f)
	local map = {layout={},width=0,height=0,pos=nil,visited={}}
	local start_pos = nil
	local r, c = 0, 0
	for line in f:lines() do
		local row = {}
		r = r + 1
		c = 0
		for l in line:gmatch(".") do
			c = c + 1
			if l == "^" then
				l = '.'
				start_pos = {r,c,'^'}
			end
			table.insert(row,l)
		end
		if map.width == 0 then
			map.width = c
		end
		map.height = map.height + 1
		table.insert(map.layout,row)
	end
	map.pos = start_pos
	return map
end

function day6.repr_map(map)
	s = ""
	for r = 1, #map.layout do
		line = ""
		for c = 1, #map.layout[r] do
			if map.pos[1] == r and map.pos[2] == c then
				line = line .. map.pos[3]
			elseif day6.has_visited(map,{r,c}) then
				line = line .. day6.repr_visit(map, {r,c})
			else
				line = line .. map.layout[r][c]
			end
		end
		s = s .. line .. "\n"
	end
	return s
end

function day6.hash_pos(map,pos)
	return map.width * (pos[1]-1) + (pos[2]-1)
end

function day6.unhash_pos(map,hash)
	return {(hash // map.width) + 1, (hash % map.width) + 1}
end

function day6.visit(map,pos,dir)
	local updated = false
	local h = day6.hash_pos(map,pos)
	if map.visited[h] == nil then
		map.visited[h] = {}
	end
	if map.visited[h][dir] == nil then
		updated = true
		map.visited[h][dir] = true
	end
	return updated
end

function day6.has_visited(map,pos,dir)
	local h = day6.hash_pos(map,pos)
	if dir ~= nil then
		for _,d in ipairs(map.visited[h]) do
			if dir == d then
				return true
			end
		end
		return false
	end
	return map.visited[h] ~= nil
end

function day6.repr_visit(map,pos)
	local h = day6.hash_pos(map,pos)
	local v = map.visited[h]
	if v == nil then
		return '.'
	else
		if day6.count_keys(v) == 1 then
			for k,v in pairs(v) do return k end
		else
			return "X"
		end
	end
end

function day6.str_pos(pos)
	return pos[1] .. "," .. pos[2]
end

function day6.is_obstructed(map,pos)
	local obs = {"#","O"}
	-- print("is_obstructed(map,{"..day6.str_pos(pos).."})")
	for _,o in ipairs(obs) do
		if map.layout[pos[1]][pos[2]] == o then return true end
	end
	return false
end

function day6.travel(map)
	local dir = {0,0}
	local status = ""
	if map.pos[3] == '^' then
		dir[1] = -1
	elseif map.pos[3] == '>' then
		dir[2] = 1
	elseif map.pos[3] == 'v' then
		dir[1] = 1
	elseif map.pos[3] == '<' then
		dir[2] = -1
	else
		print("ERROR: Invalid position direction: " .. map.pos[3])
		os.exit(8)
	end
	
	if day6.is_obstructed(map,map.pos) then
		return "obstructed"
	end

	local new_pos = {map.pos[1],map.pos[2]}
	while not day6.is_obstructed(map,new_pos) do
		local updated = day6.visit(map,new_pos,map.pos[3])
		if not updated then
			status = "loop"
			break
		end
		map.pos[1] = new_pos[1]
		map.pos[2] = new_pos[2]
		new_pos[1] = new_pos[1] + dir[1]
		new_pos[2] = new_pos[2] + dir[2]
		if new_pos[1] < 1 or new_pos[1] > #map.layout or new_pos[2] < 1 or new_pos[2] > #map.layout[1] then
			--map.visited[day6.str_pos(new_pos)] = true
			--map.pos[1] = new_pos[1]
			--map.pos[2] = new_pos[2]
			status = "exit"
			break
		end
	end
	return status
end

function day6.count_keys(t)
	local count = 0
	for k,_ in pairs(t) do
		count = count + 1
	end
	return count
end

function day6.rot_pos(pos)
	if pos[3] == '^' then
		pos[3] = '>'
	elseif pos[3] == '>' then
		pos[3] = 'v'
	elseif pos[3] == 'v' then
		pos[3] = '<'
	elseif pos[3] == '<' then
		pos[3] = '^'
	else
		print("ERROR: Invalid position direction: " .. pos[3])
		os.exit(8)
	end
end

function day6.solve(map)
	while true do
		if AOC.test_mode then
			print(day6.repr_map(map))
			--print("Visited " .. day6.count_keys(map.visited) .. " distinct positions")
		end
		local status = day6.travel(map)
		AOC.dprint(status)
		if status == "exit" then
			break
		end
		day6.rot_pos(map.pos)
	end
	if AOC.test_mode then
		print(day6.repr_map(map))
	end
end

function day6.copy_map(m)
	local map = {layout={},width=m.width,height=m.height,pos={m.pos[1],m.pos[2],m.pos[3]},visited={}}
	for r = 1, m.height do
		map.layout[r] = {}
		for c = 1, m.width do
			map.layout[r][c] = m.layout[r][c]
		end
	end
	for k,v in pairs(m.visited) do
		map[k] = v
	end
	return map
end

function day6.try_obstruction(map,pos)
	AOC.dprint("try obstruction: " .. day6.str_pos(pos))
	local new_map = day6.copy_map(map)
	new_map.layout[pos[1]][pos[2]] = "O"
	while true do
		AOC.dprint(day6.str_pos(new_map.pos))
		local status = day6.travel(new_map)
		AOC.dprint("travel","->",status)
		if status == "exit" then
			AOC.dprint("exited")
			return 0
		elseif status == "loop" then
			if AOC.test_mode then
				print(day6.repr_map(new_map))
			end
			return 1
		elseif status == "obstructed" then
			AOC.dprint("skip")
			return 0
		end
		day6.rot_pos(new_map.pos)
	end
end

function day6.part1(f)
	local map = day6.mk_map(f)
	day6.solve(map)
	print("Visited " .. day6.count_keys(map.visited) .. " distinct positions")
end

function day6.part2(f)
	local map = day6.mk_map(f)
	local orig_map = day6.copy_map(map)
	day6.solve(map)
	local total_obs = 0
	for k,v in pairs(map.visited) do
		local pos = day6.unhash_pos(orig_map,k)
		AOC.dprint(k .. "  ->  " .. day6.str_pos(pos))
		local obs = day6.try_obstruction(orig_map,pos)
		total_obs = total_obs + obs
	end
	print("Total obstructions that cause a loop: " .. total_obs)
end

AOC.register("day6","Day 6",day6.part1,day6.part2)
AOC.start()

