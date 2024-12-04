import numpy as np

from collections import Counter

def read_file(file_path):
    xmas_mat = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # string to list of char
            line = list(line.strip())
            xmas_mat.append(line)
    return xmas_mat

def get_cut_coords(center, matrix_shape):
    i, j = center
    lim_x, lim_y = matrix_shape
    x_left = i - 1 if i - 1 >= 0 else 0
    x_right = i + 1 if i + 1 < lim_x else lim_x - 1
    y_top = j - 1 if j - 1 >= 0 else 0
    y_bottom = j + 1 if j + 1 < lim_y else lim_y - 1
    return x_left, x_right, y_top, y_bottom

def find_char(mat, char_to_find, center, direction):
    matrix_shape = (len(mat), len(mat[0]))
    # get a 3x3 matrix around the center, if in a border it will be 2x2
    x_left, x_right, y_top, y_bottom = get_cut_coords(center, matrix_shape)
    centers = []
    directions = []
    # if we are looking for an M, we don't know the direction yet
    if direction == 'all':
        for i in range(x_left, x_right + 1):
            for j in range(y_top, y_bottom + 1):
                # M found
                if mat[i][j] == char_to_find:
                    # record the position of the M
                    centers.append((i, j))
                    # record the direction we will be looking for A and S
                    directions.append((i - center[0], j - center[1]))
    # if we are looking for an A or S, we know the direction
    else:
        # look only in that direction
        i, j = center
        i += direction[0]
        j += direction[1]
        if 0 <= i < matrix_shape[0] and 0 <= j < matrix_shape[1]:
            if mat[i][j] == char_to_find:
                # A or S found, record the position
                centers.append((i, j))
                # record the direction we will be looking for S
                directions.append((i - center[0], j - center[1]))
    return centers, directions
    

def count_xmas(matrix):
    xmas_count = 0
    for i, row in enumerate(matrix):
        for j, char in enumerate(row):
            # if we find an X, we start looking for M, A, S
            if char == 'X':
                directions = ['all'] # we don't know the direction yet
                centers = [(i, j)] # note that we start from the X
                # we iteratively look for M, A, S
                for char_to_find in ['M', 'A', 'S']:
                    new_centers = []
                    new_directions = []
                    # for each valid position of the current char
                    for c_i, center in enumerate(centers):
                        # get the positions of the next chars, as well as the directions to them
                        cs, ds = find_char(matrix, char_to_find, center, directions[c_i])
                        new_centers.extend(cs)
                        new_directions.extend(ds)
                    centers = new_centers
                    # if we did not find any valid position, we stop for this X
                    if len(centers) == 0:
                        break
                    directions = new_directions
                    # if we found the last char, we increment the count by the number of valid positions
                    if char_to_find == 'S':
                        xmas_count += len(centers)
    return xmas_count

def check_mas(matrix):
    """the input matrix is always a 3x3 matrix, the function looks for a cross shaped MAS"""
    """For a cross shaped MAS, the center must be an A, there must be 2 Ms and 2 Ss. Moreover, the Ms and Ss can't be in the same diagonal"""
    center = matrix[1, 1]
    if center != 'A':
        return False
    top_left, top_right, bottom_left, bottom_right = matrix[0, 0], matrix[0, 2], matrix[2, 0], matrix[2, 2]
    letter_count = Counter([top_left, top_right, bottom_left, bottom_right])
    if letter_count['M'] != 2 or letter_count['S'] != 2:
        return False
    if top_left == 'M' and bottom_right == 'M':
        return False
    if top_right == 'M' and bottom_left == 'M':
        return False
    return True

def count_mas(matrix):
    matrix = np.array(matrix)
    slide_top_left = (0, 0)
    matrix_shape = (len(matrix), len(matrix[0]))
    slide_max_coords = (matrix_shape[0] - 3, matrix_shape[1] - 3)
    mas_count = 0
    for i in range(slide_top_left[0], slide_max_coords[0]+1):
        for j in range(slide_top_left[1], slide_max_coords[1]+1):
            # get the 3x3 matrix around the top left corner
            sub_matrix = matrix[i:i+3, j:j+3]
            # check if we have MAS
            if check_mas(sub_matrix):
                mas_count += 1
    return mas_count

                        
if __name__ == '__main__':
    file_path = 'input.txt'
    matrix = read_file(file_path)
    ## PART 1
    xmas_count = count_xmas(matrix)
    print(f"Part 1: {xmas_count}")
    ## PART 2
    mas_count = count_mas(matrix)
    print(f"Part 2: {mas_count}")
        