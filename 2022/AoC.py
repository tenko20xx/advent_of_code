import os
import argparse

TEST = False
DAY = None

exec_part1 = True
exec_part2 = True

def tprint(msg):
    if TEST:
        print(msg)

def get_input(day=None):
    if day is None:
        if DAY:
            day = DAY
        else:
            raise Exception("Day has not been set")
    filename = "inputs/day{}{}.input".format(day,".test" if TEST else "")
    if os.path.exists(filename):
        with open(filename,'r') as fp:
            return fp.read()
    raise Exception("Cannot find input file for day {}".format(day))

def set_day(day):
    global DAY
    DAY = day

def get_default_argparse():
    desc = "Advent of Code solutions"
    if DAY:
        desc = desc + " -- Day {}".format(DAY)
    return argparse.ArgumentParser(description=desc)

def parse_args(parser=None):
    global TEST, exec_part1, exec_part2
    if parser is None:
        parser = get_default_argparse()
    parser.add_argument("-t","--test",action="store_true")
    parser.add_argument("--part1",action="store_true")
    parser.add_argument("--part2",action="store_true")
    args = parser.parse_args()

    if args.test:
        TEST = True
    if args.part1 or args.part2:
        exec_part1 = args.part1
        exec_part2 = args.part2
    return args
