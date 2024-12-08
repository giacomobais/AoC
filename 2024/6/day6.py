import numpy as np
import copy

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

class BoardGame():
    def __init__(self, board):
        self.board = board
        self.n_rows, self.n_cols = board.shape
        self.starting_position = self.get_starting_position()
        self.current_direction = (-1, 0) # this is UP
        self.tiles_visited = 0
        # dictionary to change direction in a clockwise manner
        self.next_direction_dict = {(-1, 0): (0, 1), (0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0)}
        

        
    def clean_board(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.board[i, j] == 'X':
                    self.board[i, j] = '.'
        self.board[self.starting_position] = '^'
        self.tiles_visited = 0
        self.current_direction = (-1, 0)

    def get_starting_position(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.board[i, j] =='^':
                    return i, j
    
    def check_boundaries(self, i, j):
        return i >= 0 and i < self.n_rows and j >= 0 and j < self.n_cols
        
    def start_game(self, starting_position = None, simulation = False, custom_board = None, starting_direction = None, tiles_directions = None):
        self.tiles_visited = 0
        if starting_position is None:
            starting_position = self.starting_position
        i, j = starting_position
        visited = []
        while True:
            if self.board[i, j] != 'X':
                self.tiles_visited += 1
                self.board[i, j] = 'X'
            visited.append((i, j))
            next_i, next_j = i + self.current_direction[0], j + self.current_direction[1]
            if not self.check_boundaries(next_i, next_j):
                break
            while self.board[next_i, next_j] == '#':
                self.current_direction = self.next_direction_dict[self.current_direction]
                next_i, next_j = i + self.current_direction[0], j + self.current_direction[1]

            i, j = next_i, next_j
        return self.tiles_visited, visited
    
    def check_loops(self, visited_tiles):
        # initialize a matrix to store the directions of each tile
        tiles_direction = np.empty((self.n_rows, self.n_cols), dtype = object)
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                tiles_direction[i, j] = []
        # initializa a mock board for simulation
        self.clean_board()
        mock_board = copy.deepcopy(self.board)
        loops = set()
        # start simulation for each tile except the first one
        for t in range(len(visited_tiles)-1):
            current_position_x, current_position_y = visited_tiles[t]
            next_position_x, next_position_y = visited_tiles[t+1]
            direction = (next_position_x - current_position_x, next_position_y - current_position_y)
            memory = mock_board[next_position_x, next_position_y]
            mock_board[next_position_x, next_position_y] = '#'
            mock_board[current_position_x, current_position_y] = 'X'
            print(f"Running simulation for tile {t}")
            if self.starting_position != (next_position_x, next_position_y) and memory != 'X':
                if self.loop_found(mock_board.copy(), copy.deepcopy(tiles_direction), visited_tiles[t], direction):
                    loops.add((next_position_x, next_position_y))
            mock_board[next_position_x, next_position_y] = memory
            tiles_direction[current_position_x, current_position_y].append(direction)
        return len(loops)
    
    def loop_found(self, board, tiles_direction, starting_position, direction):
        i, j = starting_position
        n = 0
        while True:
            if board[i, j] != 'X':
                board[i, j] = 'X'
            # this works as a check, as it implies a loop
            if n > self.n_cols * self.n_rows:
                return True
            # ideally this would be the better check, but it is not working
            # if direction in tiles_direction[i, j]:
            #     return True
            tiles_direction[i, j].append(direction)
            next_i, next_j = i + direction[0], j + direction[1]
            if not self.check_boundaries(next_i, next_j):
                return False
            while board[next_i, next_j] == '#':
                direction = self.next_direction_dict[direction]
                next_i, next_j = i + direction[0], j + direction[1]
            i, j = next_i, next_j
            n += 1
            
            
            

    def __str__(self):
        return str(self.board)
    
    def __repr__(self):
        return str(self.board)
            

if __name__ == '__main__':
    board = read_file('input.txt')
    game = BoardGame(board)
    # Part 1
    n_visited, visited = game.start_game()
    print(f"Part 1: {n_visited}")
    
    # Part 2
    n_loops = game.check_loops(visited)
    print(f"Part 2: {n_loops}")