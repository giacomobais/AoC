import numpy as np

def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        lines = [line.strip('\n') for line in lines]
    return lines[0]

def get_file_blocks(disk_map):
    file_blocks = []
    file_id = 0
    free_space = False
    for char in disk_map:
        number = int(char)
        for _ in range(number):
            if free_space:
                file_blocks.append('.')
            else:
                file_blocks.append(str(file_id))
        free_space = not free_space
        if free_space:
            file_id += 1
    return file_blocks

def arrange_space(file_blocks):
    new_file_blocks = []
    i = 0
    j = len(file_blocks) - 1
    while i < j:
        
        if file_blocks[i] != '.':
            new_file_blocks.append(file_blocks[i])
        else:
            while file_blocks[j] == '.':
                j -= 1
            if i < j:
                new_file_blocks.append(file_blocks[j])
                # print(f"Added {file_blocks[j]} in position {i}")
            j -= 1
        # print(f"i: {i}, j: {j}, new_file_blocks: {new_file_blocks}")
        i += 1
    if i == j:
        new_file_blocks.append(file_blocks[i])
    for i in range(len(file_blocks) - len(new_file_blocks)):
        new_file_blocks.append('.')
    return new_file_blocks

def checksum(arranged_file_blocks):
    """Do the checksum with Long"""
    check_sum = 0
    for i, block in enumerate(arranged_file_blocks):
        if block == '.':
            continue
        check_sum += int(block) * i
    return check_sum

if __name__ == '__main__':
    disk_map = read_file('example.txt')
    file_blocks  = get_file_blocks(disk_map)

    ## Part 1   
    arranged_file_blocks = arrange_space(file_blocks)  
    check_sum = checksum(arranged_file_blocks)
    print(f"Part 1: {check_sum}")

    ## Part 2