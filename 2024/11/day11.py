import time
import functools

def read_file(file_path):
    with open(file_path, 'r') as f:
        stones = f.readlines()[0].split()
    return stones

def blink(stones, n):
    """Function for part 1, iteratively calculate the new stones"""
    new_stones = []
    # for each blink
    for _ in range(n):
        # for each stone to transform
        for stone in stones:
            # transform the stone according to the rules
            if stone == '0':
                new_stones.append('1')
                continue
            if len(stone) % 2 == 0:
                mid_point = len(stone) // 2
                first_half = str(int(stone[:mid_point]))
                new_stones.append(first_half)
                second_half = str(int(stone[mid_point:]))
                new_stones.append(second_half)
                continue
            new_stones.append(str(int(stone) * 2024))
        stones = new_stones.copy()
        new_stones = []
    return stones

@functools.lru_cache(maxsize=None)
def get_new_stone(stone):
    """Function for part 2 that blinks, i.e. calculates the new stone. We cache the results so that we do not repeat calculations for stones we have already seen"""
    if stone == '0':
        return '1'
    if len(stone) % 2 == 0:
        mid_point = len(stone) // 2
        first_half = str(int(stone[:mid_point]))
        second_half = str(int(stone[mid_point:]))
        return first_half, second_half
    return str(int(stone) * 2024)

@functools.lru_cache(maxsize=None)
def rec_blink(stone, n):
    """Recursive function for part 2. We moved to recursion so that we can cache the results of the new stones we have already seen
       So the function calculates the length of a single stone after n blinks"""
    # base case, if we are at the last blink
    if n == 1:
        # blink it
        new_stone = get_new_stone(stone)
        # if the stone splits into two, return 2
        if isinstance(new_stone, tuple):
            return 2
        # if the stone does not split, return 1
        return 1
    # recursive case, where we need to blink the stone n times
    # blink once
    new_stone = get_new_stone(stone)
    # if the stone did not split
    if isinstance(new_stone, str):
        # blink n-1 times with the new stone and return the length
        return rec_blink(new_stone, n - 1)
    # if the stone split into two
    else:
        # blink n-1 times with each of the new stones and return the sum of the lengths
        return rec_blink(new_stone[0], n - 1) + rec_blink(new_stone[1], n - 1)
    
def blink_optimized(stones, n):
    length = 0
    # for each stone, calculate the length after n blinks
    for stone in stones:
        # add up the lengths of all the stones after n blinks
        length += rec_blink(stone, n)
    return length


if __name__ == '__main__':
    stones = read_file('input.txt')
    
    ## Part 1
    start = time.time()
    new_stones = blink(stones, 25)
    print(f"Time: {time.time() - start}")
    print(f"Part 1: {len(new_stones)}")

    ## Part 2
    start = time.time()
    length_stones = blink_optimized(stones, 75)
    print(f"Time: {time.time() - start}")
    print(f"Part 2: {length_stones}")