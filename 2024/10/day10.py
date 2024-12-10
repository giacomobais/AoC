import numpy as np
import time

def read_file(file_path):
    board = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # string to list of char
            line = list(line.strip())
            line = list(map(int, line))
            board.append(line)
    return np.array(board)

def check_boundaries(i, j, board_shape):
    lim_x, lim_y = board_shape
    if 0 <= i < lim_x and 0 <= j < lim_y:
        return True
    return False

def rec_trail_score(board, i, j, current_height, positions):
    """Recursive function for part 1 that returns all positions of 9 (no duplicates) in a valid path starting from i, j"""
    # base case for the sake of the problem, when we reached 9 it is a valid position
    if current_height == 9:
        positions.add((i, j))
        return positions
    # if we are not at the end of the path, we need to check the next step
    else:
        plausible_paths = []
        up = (i - 1, j)
        down = (i + 1, j)
        left = (i, j - 1)
        right = (i, j + 1)
        # check all forking paths
        if check_boundaries(*up, board.shape) and board[up] == current_height + 1:
            plausible_paths.append(up)
        if check_boundaries(*down, board.shape) and board[down] == current_height + 1:
            plausible_paths.append(down)
        if check_boundaries(*left, board.shape) and board[left] == current_height + 1:
            plausible_paths.append(left)
        if check_boundaries(*right, board.shape) and board[right] == current_height + 1:
            plausible_paths.append(right)

        # for each forking path, we check the next step
        for p in plausible_paths:
            i, j = p
            # this will return all the positions that end in a 9
            path_positions = rec_trail_score(board, i, j, current_height + 1, positions)
            # merge the new positions with the previous ones from the forking paths
            positions = positions.union(path_positions)
        return positions

def rec_trail_rating(board, i, j, current_height, positions):
    """Recursive function for part 2 that returns all positions of 9 (including duplicates) in a valid path starting from i, j"""
    # base case for the sake of the problem, when we reached 9 it is a valid position
    if current_height == 9:
        positions.append((i, j))
        return positions
    # if we are not at the end of the path, we need to check the next step
    else:
        plausible_paths = []
        up = (i - 1, j)
        down = (i + 1, j)
        left = (i, j - 1)
        right = (i, j + 1)
        # check all forking paths
        if check_boundaries(*up, board.shape) and board[up] == current_height + 1:
            plausible_paths.append(up)
        if check_boundaries(*down, board.shape) and board[down] == current_height + 1:
            plausible_paths.append(down)
        if check_boundaries(*left, board.shape) and board[left] == current_height + 1:
            plausible_paths.append(left)
        if check_boundaries(*right, board.shape) and board[right] == current_height + 1:
            plausible_paths.append(right)

        # for each forking path, we check the next step
        for p in plausible_paths:
            i, j = p
            # this will append to positions all the positions that end in a 9
            _ = rec_trail_rating(board, i, j, current_height + 1, positions)
        return positions
    
def get_trails_score(board, part2 = False):
    trails_score = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                if not part2:
                    nine_positions = rec_trail_score(board, i, j, 0, set())
                else:
                    nine_positions = rec_trail_rating(board, i, j, 0, [])
                trails_score += len(nine_positions)
    return trails_score

if __name__ == '__main__':
    file_path = 'example.txt'
    board = read_file(file_path)

    ## Part 1
    start = time.time()
    trails_score = get_trails_score(board)
    end = time.time()
    print(f"Time: {end - start}")
    print(f"Part 1: {trails_score}")

    ## Part 2
    start = time.time()
    trails_score = get_trails_score(board, part2=True)
    end = time.time()
    print(f"Time: {end - start}")
    print(f"Part 2: {trails_score}")