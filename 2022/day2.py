#!/usr/bin/python3

def outcome_score(p1,p2):
    if p1 == p2:
        return 3
    if p1 == "R":
        if p2 == "P":
            return 6
        elif p2 == "S":
            return 0
    elif p1 == "P":
        if p2 == "R":
            return 0
        elif p2 == "S":
            return 6
    elif p1 == "S":
        if p2 == "R":
            return 6
        elif p2 == "P":
            return 0
    raise Exception("Invalid play: {} - {}".format(p1,p2))

def p1_type(p1):
    if p1 == "A":
        return "R"
    elif p1 == "B":
        return "P"
    elif p1 == "C":
        return "S"
    raise Exception("Invalid play: {}".format(p1))

def p2_strat1(p1,p2):
    if p2 == "X":
        return "R"
    elif p2 == "Y":
        return "P"
    elif p2 == "Z":
        return "S"
    raise Exception("Invalid play: {} - {}".format(p1,p2))

def p2_strat2(p1,p2):
    if p2 == "Y":
        return p1
    elif p2 == "X":
        if p1 == "R":
            return "S"
        elif p1 == "P":
            return "R"
        elif p1 == "S":
            return "P"
    elif p2 == "Z":
        if p1 == "R":
            return "P"
        elif p1 == "P":
            return "S"
        elif p1 == "S":
            return "R"
    raise Exception("Invalid play: {} - {}".format(p1,p2))

def main():
    print("--- Part 1 ---")
    score = 0
    with open("inputs/day2.input",'r') as fp:
        for line in fp:
            p1,p2 = line.strip().split()
            p1 = p1_type(p1)
            p2 = p2_strat1(p1,p2)
            if p2 == "R":
                score += 1
            elif p2 == "P":
                score += 2
            elif p2 == "S":
                score += 3
            else:
                raise Exception("Invalid play: {}".format(p2))
            score += outcome_score(p1,p2)
    print("Score: {}".format(score))

    print("--- Part 2 ---")
    score = 0
    with open("inputs/day2.input",'r') as fp:
        for line in fp:
            p1,p2 = line.strip().split()
            p1 = p1_type(p1)
            p2 = p2_strat2(p1,p2)
            if p2 == "R":
                score += 1
            elif p2 == "P":
                score += 2
            elif p2 == "S":
                score += 3
            else:
                raise Exception("Invalid play: {}".format(p2))
            score += outcome_score(p1,p2)
    print("Score: {}".format(score))

if __name__ == "__main__":
    main()
