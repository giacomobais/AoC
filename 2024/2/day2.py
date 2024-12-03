import numpy as np

def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        reports = []
        for line in lines:
            levels = list(map(int, line.split()))
            reports.append(levels)
    return reports

def check_monotony(levels):
    flag = levels[1] - levels[0]
    if flag == 0:
        return False
    incr, decr = flag > 0, flag < 0
    
    for i, lvl in enumerate(levels[2:]):
        if incr and lvl - levels[i+1] <= 0:
            return False
        if decr and lvl - levels[i+1] >= 0:
            return False
    return True

def check_distance(levels):
    for i, lvl in enumerate(levels):
        if i == 0:
            continue
        if abs(lvl - levels[i-1]) < 1 or abs(lvl - levels[i-1]) > 3:
            return False
    return True

def calc_valid_reports(reports):
    tot = 0
    for levels in reports:
        if check_monotony(levels) and check_distance(levels):
            tot+=1
    return tot

def calc_valid_reports_tolerant(reports):
    tot = 0
    for levels in reports:
        levels_combinations = [levels]
        for i in range(len(levels)):
            levels_combinations.append(levels[:i] + levels[i+1:])
        for comb in levels_combinations:
            if check_monotony(comb) and check_distance(comb):
                tot+=1
                break
    return tot

if __name__ == '__main__':
    file_path = 'input.txt'
    reports = read_file(file_path)

    ## PART 1
    n_valid = calc_valid_reports(reports)
    print(n_valid)

    ## PART 2
    n_valid = calc_valid_reports_tolerant(reports)
    print(n_valid)
    