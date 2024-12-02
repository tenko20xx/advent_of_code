if AOC ~= nil then
	return AOC
end
AOC = {}
AOC.test_mode = false

local context_registered = false
local this_context = {}

function AOC.tprint(msg)
	if AOC.test_mode then
		print(msg)
	end
end

function AOC.get_input_file_name(custom)
	s = "inputs/" .. this_context.short_name
	if AOC.test_mode then
		s = s .. ".test"
	end
	if custom then
		s = s .. "." .. custom
	end
	s = s .. ".input"
	return s
end

function AOC.get_input_file(custom)
	fname = AOC.get_input_file_name(custom)
	return io.open(fname,'r')
end

function AOC.register(short_name, long_name, part1, part2)
	this_context.short_name = short_name
	this_context.long_name = long_name
	this_context.part1 = part1
	this_context.part2 = part2
	context_registered = true
end

function AOC.start()
	if context_registered == false then
		print("ERROR: No AOC module has been registered yet")
		os.exit(10)
	end

	local argparse = require("argparse")
	local parser = argparse(this_context.short_name,"Advent of Code -- " .. this_context.long_name)
	parser:flag("-1 --part1","Execute Part 1")
	parser:flag("-2 --part2","Execute Part 2")
	parser:flag("--test", "Enable test mode")

	local args = parser:parse()
	if args.test then
		AOC.test_mode = true
		print("** TESTING **")
	end

	exec_p1 = args.part1 and true or false
	exec_p2 = args.part2 and true or false
	if exec_p1 == false and exec_p2 == false then
		exec_p1 = true
		exec_p2 = true
	end

	print("== " .. this_context.long_name .. " ==")
	if exec_p1 then
		print("-- Part 1 --")
		this_context.part1()
	end

	if exec_p2 then
		print("-- Part 2 --")
		this_context.part2()
	end
end

return AOC
