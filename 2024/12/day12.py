import numpy as np

def read_file(file_path):
    land = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            land.append(list(line.strip('\n')))
    return np.array(land)
    

class Land():
    def __init__(self, land):
        self.land = land
        self.height, self.width = land.shape
        self.regions = self.get_regions()

    @staticmethod
    def get_neighbors(pos):
        return [(pos[0]+0, pos[1]+1), (pos[0]+0, pos[1]-1), (pos[0]+1, pos[1]+0), (pos[0]-1, pos[1]+0)]
    
    @staticmethod
    def rec_region(pos, members_pos, land, id):
        # base cases
        height, width = land.shape
        if pos[0] < 0 or pos[0] >= height or pos[1] < 0 or pos[1] >= width:
            return members_pos
        if land[pos] != id:
            return members_pos
        if pos in members_pos:
            return members_pos
        # recursive cases
        members_pos.add(pos)
        neighbors = Land.get_neighbors(pos)
        for neighbor in neighbors:
            members_pos = Land.rec_region(neighbor, members_pos, land, id)
        return members_pos

        # recursive case
    def get_regions(self):
        regions = set()
        visited = set()
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) in visited:
                    continue
                region_members = Land.rec_region((row, col), set(), self.land, self.land[row, col])
                visited = visited.union(region_members)
                region = Region(region_members, self.land[row, col], self.land.shape)
                regions.add(region)
        return regions
    
    def get_region_by_id(self, id):
        regions = []
        for region in self.regions:
            if region.id == id:
                regions.append(region)
        return regions
    
    def get_price(self, use_perimeter=True):
        price = 0
        for region in self.regions:
            if use_perimeter:
                price += region.get_area() * region.get_perimeter()
            else:
                print(f"Region {region.id} has area of {region.get_area()} and {region.get_n_sides()} sides")
                price += region.get_area() * region.get_n_sides()
        return price
                
    def __str__(self):
        return str(self.land)
    
    def __repr__(self):
        return str(self.land)

class Region():
    def __init__(self, coords, id, land_shape):
        self.coords = frozenset(coords)
        self.id = id
        self.height, self.width = land_shape
    
    def get_area(self):
        return len(self.coords)
    
    def get_perimeter(self):
        perimeter = 0
        for coord in self.coords:
            neighbors = Land.get_neighbors(coord)
            for neighbor in neighbors:
                    if neighbor not in self.coords:
                        perimeter += 1
        return perimeter
    
    def get_bordering_coords(self):
        bordering_coords = set()
        for coord in self.coords:
            neighbors = Land.get_neighbors(coord)
            if not all(neighbor in self.coords for neighbor in neighbors):
                bordering_coords.add(coord)
        return bordering_coords
    
    def get_n_sides(self):
        n_sides = 0
        canvas = np.zeros((self.height+2, self.width+2), dtype=int)
        for coord in self.coords:
            coord = (coord[0]+1, coord[1]+1)
            neighbors = Land.get_neighbors(coord)
            # extend with the diagonal neighbors
            neighbors.extend([(coord[0]+1, coord[1]+1), (coord[0]+1, coord[1]-1), (coord[0]-1, coord[1]+1), (coord[0]-1, coord[1]-1)])
            # add 1 to all the neighbors
            for neighbor in neighbors:
                original_neighbor = (neighbor[0]-1, neighbor[1]-1)
                if original_neighbor not in self.coords:
                    canvas[neighbor] = 1
                    # if self.id == 'F':
                    #     print(canvas, neighbor)
        if self.id == 'X':
            print(canvas)
        for i in range(self.height+2):
            for j in range(self.width+2):
                if canvas[i, j] == 1:
                    neighbors = [(i+0, j+1), (i+0, j-1), (i+1, j+0), (i-1, j+0)]
                    ones_neighbors = []
                    for neighbor in neighbors:
                        if neighbor[0] < 0 or neighbor[0] >= self.height+2 or neighbor[1] < 0 or neighbor[1] >= self.width+2:
                            continue
                        if canvas[neighbor] == 1:
                            ones_neighbors.append(neighbor)
                    if len(ones_neighbors) == 1:
                        print(f"Adding 2 sides for {i, j} in the canvas")
                        n_sides += 2
                    if len(ones_neighbors) == 3:
                        diagonal_neighbors = [(i+1, j+1), (i+1, j-1), (i-1, j+1), (i-1, j-1)]
                        # filter the diagonal neighbors that are not in the coords
                        diagonal_neighbors = [neighbor for neighbor in diagonal_neighbors if (neighbor[0]-1, neighbor[1]-1) in self.coords]
                        for neighbor in diagonal_neighbors:
                            # get direction from i, j
                            direction = (neighbor[0]-i, neighbor[1]-j)
                            #dir = -11, TO CHECK -1,0 ; 0,1
                            to_check = [(i+direction[0], j), (i, j+direction[1])]
                            # if self.id == 'X':
                                # print(f"TO CHECK {to_check}, we are in {i, j} in the canvas and direction is {direction}")
                            if canvas[to_check[0]] == 1 and canvas[to_check[1]] == 1:
                                print(f"Adding 1 side for {i, j} in the canvas")
                                n_sides += 1
                    if len(ones_neighbors) == 2 and ones_neighbors[0][0] != ones_neighbors[1][0] and ones_neighbors[0][1] != ones_neighbors[1][1]:
                        n_sides += 1
                        print(f"Adding 1 side for {i, j} in the canvas")
                    if len(ones_neighbors) == 0:
                        print(f"Adding 4 sides for {i, j} in the canvas")
                        n_sides += 4
                    # print(ones_neighbors, n_sides)
        return n_sides
                
    def __eq__(self, other):
        if isinstance(other, Region):
            return self.coords == other.coords  # Compare based on coordinates
        return False
    
    def __hash__(self):
        # if even one coordinate is the same, the regions are the same
        return hash(frozenset(self.coords))
    
    def __repr__(self):
        height = max(coord[0] for coord in self.coords) + 1
        width = max(coord[1] for coord in self.coords) + 1
        grid = np.empty((height, width), dtype=str)
        for coord in self.coords:
            grid[coord] = self.id
        # fill the empty spaces with -
        for i in range(height):
            for j in range(width):
                if grid[i, j] == '':
                    grid[i, j] = '-'
        return str(grid)


if __name__ == '__main__':
    land = read_file('example.txt')
    land = Land(land)
    
    ## Part 1
    price = land.get_price()
    print(f"Part 1: {price}")

    ## Part 2
    # v_region = land.get_region_by_id('V')[0]
    # print(v_region.get_n_sides())
    
    price = land.get_price(use_perimeter=False)
    print(f"Part 2: {price}")