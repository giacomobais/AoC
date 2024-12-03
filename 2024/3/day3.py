import numpy as np
import re

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def calc_multiplications(lines):
    mult_results = []
    # re that matches mul(1-3 digits, 1-3 digits)
    pattern = r'mul\(\d{1,3},\d{1,3}\)'
    for line in lines:
        mults = re.findall(pattern, line)
        for mult in mults:
            # extract numbers to multiply
            nums = re.findall(r'\d{1,3}', mult)
            mult_results.append(int(nums[0]) * int(nums[1]))
    
    return np.sum(mult_results)

def calc_multiplications_dos(lines):
    mult_results = []
    pattern = r'mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)'
    do = True
    for i, line in enumerate(lines):
        mults = re.findall(pattern, line)
        for mult in mults:
            if mult.startswith('d'):
                do = True if mult == 'do()' else False
            else:
                if do:
                    # extract numbers to multiply
                    nums = re.findall(r'\d{1,3}', mult)
                    mult_results.append(int(nums[0]) * int(nums[1]))
    return np.sum(mult_results)

if __name__ == '__main__':
    file_path = 'input.txt'
    lines = read_file(file_path)

    ## PART 1
    mult_result = calc_multiplications(lines)
    print(f"Part 1: {mult_result}")

    ## PART 2
    mult_do_result = calc_multiplications_dos(lines)
    print(f"Part 2: {mult_do_result}")