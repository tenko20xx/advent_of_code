import os
import argparse

TEST = False
DAY = None

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
    global TEST
    if parser is None:
        parser = get_default_argparse()
    parser.add_argument("-t","--test",action="store_true")
    args = parser.parse_args()

    if args.test:
        TEST = True
    return args
