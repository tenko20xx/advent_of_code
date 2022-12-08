import os
import argparse

TEST = False

def tprint(msg):
    if TEST:
        print(msg)

def get_input(day):
    filename = "inputs/day{}{}.input".format(day,".test" if TEST else "")
    if os.path.exists(filename):
        with open(filename,'r') as fp:
            return fp.read()
    raise Exception("Cannot find input file for day {}".format(day))

def parse_args():
    global TEST
    parser = argparse.ArgumentParser("Advent of Code solutions")
    parser.add_argument("-t","--test",action="store_true")
    args = parser.parse_args()

    if args.test:
        TEST = True

