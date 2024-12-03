import numpy as np
from collections import Counter

def read_file(file_path):

    with open(file_path, 'r') as f:
        lines = f.readlines()
        left_list, right_list = [], []
        for line in lines:
            n1, n2 = line.split()
            n1, n2 = int(n1), int(n2)
            left_list.append(n1)
            right_list.append(n2)
    
    return left_list, right_list

def calc_distance(left_list_sorted, right_list_sorted):
    distances = []
    for n1, n2 in zip(left_list_sorted, right_list_sorted):
        distance = np.abs(n1 - n2)
        distances.append(distance)
    
    return np.sum(distances)

def calc_similarity(left_list, right_list_counter):
    similarities = []
    for n in left_list:
        if n in right_list_counter:
            factor = right_list_counter[n]
        else:
            factor = 0
        similarities.append(n*factor)
    return np.sum(similarities)

if __name__ == '__main__':

    file_path = 'input.txt'
    left_list, right_list = read_file(file_path)

    ## PART 1
    left_list_sorted = sorted(left_list)
    right_list_sorted = sorted(right_list)
    
    total_distance = calc_distance(left_list_sorted, right_list_sorted)
    print(total_distance)

    ## PART 2
    right_list_counter = Counter(right_list)
    
    similarity = calc_similarity(left_list, right_list_counter)
    print(similarity)




            