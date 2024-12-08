import numpy as np

def read_file(file_path):
    board = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            row = []
            for char in line:
                if char != '\n':
                    row.append(char)
            board.append(row)
    return np.array(board)

class Board():
    def __init__(self, board):
        self.board = board
        self.n_rows, self.n_cols = board.shape
        self.vocab = set()
        self.antinodes = self.board.copy()
        for row in board:
            for char in row:
                if char != '.':
                    self.vocab.add(char)

    def reset(self):
        self.antinodes = self.board.copy()

    def check_boundaries(self, y, x):
        return y >= 0 and y < self.n_rows and x >= 0 and x < self.n_cols
    
    def get_char_positions(self, char):
        """Function to get all positions of a character in the board"""
        positions = []
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.board[i, j] == char:
                    positions.append((i, j))
        return positions
    
    def line_eq_from_points(self, char1, char2):
        """Function to get bias and slope from two points"""
        char1_y, char1_x = char1
        char1_y, char1_x = -char1_y, char1_x
        char2_y, char2_x = char2
        char2_y, char2_x = -char2_y, char2_x
        m = (char2_y - char1_y) / (char2_x - char1_x)
        b = char1_y - m * char1_x
        return m, b
    
    def get_coords_from_line(self, char1, char2, part2 = False):
        """Function to get all coordinates that are in the line between two points"""
        """It also marks the antinodes in the board, depending on the part: part1 only calculates the nearest (int) points, part2 calculates all (int) points"""
        # get slope and bias
        m, b = self.line_eq_from_points(char1, char2)
        # convert the coordinates to the board system (x is y and y is negative)
        char1 = -char1[0], char1[1]
        char2 = -char2[0], char2[1]
        # part1
        if not part2:
            # manually calculate the nearest x in both directions
            x_diff = np.abs(char1[1] - char2[1])
            if char1[1] > char2[1]:
                x_to_mark = [char1[1] + x_diff, char2[1] - x_diff]
            else:
                x_to_mark = [char1[1] - x_diff, char2[1] + x_diff]
            # for both x, calculate the y and mark the antinode
            for x in x_to_mark:
                y = m * x + b
                # should not be necessary, but floating point errors
                y = round(y)
                if self.check_boundaries(-y, x):
                    self.antinodes[-int(y), x] = '#'
        # part2
        else:
            # this time, for each possible x in the grid, not only the nearest
            for x in range(self.n_cols):
                y = m * x + b
                rounded_y = round(y)
                # only mark if the y is an integer or very close (floating point errors)
                if np.abs(y - rounded_y) < 1e-6:
                    y = rounded_y
                    if self.check_boundaries(-y, x):
                        self.antinodes[-int(y), x] = '#'
                


    
    def place_antinodes(self, part2 = False):
        n_antinodes = 0
        # for all chars that are not '.'
        for char in self.vocab:
            positions = self.get_char_positions(char)
            # combine all possible pairs, no need to repeat
            done = set()
            for i, pos1 in enumerate(positions):
                for j, pos2 in enumerate(positions):
                    if i != j and (pos1, pos2) not in done and (pos2, pos1) not in done:
                        done.add((pos1, pos2))
                        done.add((pos2, pos1))
                        # mark the antinodes
                        self.get_coords_from_line(pos1, pos2, part2)
        # count the antinodes
        for row in self.antinodes:
            for char in row:
                if char == '#':
                    n_antinodes += 1
        return n_antinodes
    
    

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.board])
    


if __name__ == '__main__':
    board = read_file('input.txt')
    board = Board(board)

    # Part 1
    antinodes = board.place_antinodes()
    print(f"Part 1: {antinodes}")

    # Part 2
    board.reset()
    antinodes = board.place_antinodes(part2 = True)
    print(board.antinodes)
    print(f"Part 2: {antinodes}")