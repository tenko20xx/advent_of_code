#!/bin/sh

usage() {
	echo "usage: $0 options | day_number"
	echo "options:"
	echo "    -h|--help		show this message"
}

day=""

while [ "$1" ]; do
	case $1 in
		-h|--help) usage; exit 0
			;;
		-*) echo "ERROR: Invalid option: $1" >&2; usage; exit 14
			;;
		*)
			if [ -z "$day" ]; then
				day=$1
			else
				echo "ERROR: Too many arguments: $@" >&2; usage; exit 15
			fi
			;;
	esac
	shift
done

if [ -z "$day" ]; then
	usage
	exit 13
fi

echo $day | egrep -q '^[0-9]{1,2}$' || {
	echo "ERROR: Day must be a 2 digit number" >&2
	exit 10
}
if [ "$day" -lt 1 -o "$day" -gt 25 ]; then
	echo "ERROR: Day must be between 1 and 25" >&2
	exit 11
fi

if [ -e "day${day}.py" ]; then
	echo "ERROR: File 'day${day}.py' already exists" >&2
	exit 12
fi

cp -v AoC_template.py day${day}.py
touch inputs/day${day}.test.input
touch inputs/day${day}.input

sed -i "s/AoC\.set_day(\".*\")/AoC\.set_day(\"${day}\")/" day${day}.py
