import time

def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        lines = [line.strip('\n') for line in lines]
    return lines[0]

def get_file_blocks(disk_map):
    """Builds a list of blocks from the disk map like specified in the problem"""
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
    # if i and j have crossed, we can't rearrange blocks anymore
    while i < j:
        # l2r: if the block is not a dot, we keep it
        if file_blocks[i] != '.':
            new_file_blocks.append(file_blocks[i])
        # if it is a dot, we can look from r2l to find a non-dot block
        else:
            while file_blocks[j] == '.':
                j -= 1
            # only move if i and j still haven't crossed
            if i < j:
                new_file_blocks.append(file_blocks[j])
            j -= 1
        # next block l2r
        i += 1
    # corner case, if i == j we need to add the last block
    if i == j:
        new_file_blocks.append(file_blocks[i])
    # fill the rest with dots, optional
    for i in range(len(file_blocks) - len(new_file_blocks)):
        new_file_blocks.append('.')
    return new_file_blocks

def checksum(arranged_file_blocks):
    """Do the checksum as specified in the problem"""
    check_sum = 0
    for i, block in enumerate(arranged_file_blocks):
        if block == '.':
            continue
        check_sum += int(block) * i
    return check_sum

def get_good_position(file_blocks, memory_needed, j):
    """Calculates the index that corresponds to the first availaspace of memory_needed, looking from l2r"""
    space = 0
    good_i = -1
    for i, block in enumerate(file_blocks):
        # limit for the search is the position of the block we are trying to move
        if i >= j:
            break
        # found candidate position
        if block == '.' and space == 0:
            good_i = i
        # count dots == space
        if block == '.':
            space += 1
        # if we find a non-dot block, we check if we have enough space
        if block != '.' and space > 0:
            if space >= memory_needed:
                # found a match!
                return good_i
            # if the space was too small, we reset the counter for space
            space = 0
    # corner case, if the last block is a dot we still check, should not be necessary because of the i>=j condition
    if space >= memory_needed:
        return good_i
    # we return -1 if there is no good position
    else:
        return -1

def get_memory_of_file(j, file_blocks):
    """Simple function to calculate the space occupied by a file in position j"""
    memory_of_file = 1
    while j > 0 and file_blocks[j-1] == file_blocks[j]:
        memory_of_file += 1
        j -= 1
    return memory_of_file

def arrange_space2(file_blocks):
    """Rearrange the blocks in a more efficient way, like explained in the problem"""
    j = len(file_blocks) - 1
    tried_to_move = set()
    # We start from the end of the list
    while j >= 0:
        # if it is a file and we haven't tried to move it yet
        if file_blocks[j] != '.' and file_blocks[j] not in tried_to_move:
            tried_to_move.add(file_blocks[j])
            # get the space occupied by the file
            memory_of_file = get_memory_of_file(j, file_blocks)
            # get a good position to insert the file
            i_to_insert = get_good_position(file_blocks, memory_of_file, j)
            # if we found a good position, we move the file
            if i_to_insert >= 0:
                # copy paste the file to the new position
                for i in range(i_to_insert, memory_of_file+i_to_insert):
                    file_blocks[i] = file_blocks[j]
                # replace the old file with dots
                file_blocks[j-memory_of_file+1:j+1] = ['.']*(memory_of_file)
                
            # back-off the index so that the whole file space is not checked again
            j -= memory_of_file
        # if it was a dot, go to the next block
        else:
            j -= 1
    return file_blocks 

if __name__ == '__main__':
    disk_map = read_file('example.txt')
    file_blocks  = get_file_blocks(disk_map)

    ## Part 1   
    arranged_file_blocks = arrange_space(file_blocks)  
    check_sum = checksum(arranged_file_blocks)
    print(f"Part 1: {check_sum}")

    ## Part 2
    arranged_file_blocks2 = arrange_space2(file_blocks)
    check_sum2 = checksum(arranged_file_blocks2)
    print(f"Part 2: {check_sum2}")

    