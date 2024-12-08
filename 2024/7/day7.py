import numpy as np
from itertools import product

def read_file(file_path):
    results = []
    all_operators = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            result, operators = line.split(':')[0].strip(), line.split(':')[1].strip()
            results.append(int(result))
            temp = []
            for operator in operators.split(' '):
                temp.append(int(operator))
            all_operators.append(temp)
    return results, all_operators

def check_result(results, operators, part2 = False):
    good_results = []
    for result, operator in zip(results, operators):

        operations = ['+', '*']
        if part2:
            operations.append('||')
        # generate all possible combinations of operators assuming they can be either + or *
        # it is a list of tuples
        combinations = list(product(operations, repeat = len(operator)-1))
        for combination in combinations:
            tmp_result = operator[0]
            for i, op in enumerate(combination):
                if op == '+':
                    tmp_result += operator[i+1]
                elif op == '*':
                    tmp_result *= operator[i+1]
                elif op == '||':
                    tmp_result = int(str(tmp_result) + str(operator[i+1]))
            if tmp_result == result:
                good_results.append(result)
                break
    return np.sum(good_results)

if __name__ == '__main__':
    results, operators = read_file('input.txt')
    
    #  Part 1
    sum_of_results = check_result(results, operators)
    print(f"Part 1: {sum_of_results}")

    #  Part 2
    sum_of_results = check_result(results, operators, part2 = True)
    print(f"Part 2: {sum_of_results}")