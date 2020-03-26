import unittest
import time
import os
import sys

TURN = 1

EMPTY_SPACE_SYMBOLS = '.'
STARTING_POINT_SYMBOLS = 'Ss'
OBSTACLE_SYMBOL = 'X'
DIRS = [('N',-1, 0), ('S',1, 0), ('E',0, 1), ('W',0, -1)]

PUZZLE_GRID = '''
S..XX
X..XX
X....
XX...
XX...
'''.split()

ROAD_GRID = []
ROAD_GRID.append('S..x..x')
ROAD_GRID.append('...x..x')
ROAD_GRID.append('......x')
ROAD_GRID.append('XX....x')
ROAD_GRID.append('......x')
ROAD_GRID.append('......x')
ROAD_GRID.append('......x')
ROAD_GRID.append('XX....x')

class HamiltonSolver:
    """Solver for a Hamilton Path problem."""

    def __init__(self, grid):
        """Initialize the HamiltonSolver instance from a grid, which must be a
        list of strings, one for each row of the grid.
        """
        self.grid = grid
        self.h = h = len(grid)
        self.w = w = len(grid[0])
        self.nb = 0
        self.start = None
        self.legal = set()
        for r, row in enumerate(grid):
            for c, item in enumerate(row):
                if item in STARTING_POINT_SYMBOLS:
                    self.start = (r, c)
                elif item in EMPTY_SPACE_SYMBOLS:
                    self.legal.add((r, c))
        if self.start == None :
            self.start = self.legal.pop()
            #print('(NO START) GET {}'.format(self.start))
            #print('(NO START) SET {}'.format(self.legal))

    def change_start(self):
        self.legal.add(self.start)
        self.start = self.legal.pop()

    def read_turn(self,path,turn):
        return path[turn]

    def format_solution(self, path):
        """Format a path as a string."""
        grid = [[OBSTACLE_SYMBOL] * self.w for _ in range(self.h)]
        for i, (o,r, c) in enumerate(path, start=1):
            print('({},{})'.format(r,c))
            grid[r][c] = i
        w = len(str(len(path) + 1)) + 1

        return '\n'.join(''.join(str(item).ljust(w) for item in row)
                         for row in grid)

    def solve(self):
        """Generate solutions as lists of coordinates."""
        r , c = self.start
        result = [ ('S',r, c)]
        path = [self.start]
        dirs = [iter(DIRS)]

        # Cache attribute lookups in local variables
        result_append = result.append
        result_pop = result.pop
        path_append = path.append
        path_pop = path.pop
        legal = self.legal
        legal_add = legal.add
        legal_remove = legal.remove
        dirs_append = dirs.append
        dirs_pop = dirs.pop

        while result:
            #r, c = path[-1]
            o, r, c = result[-1]
            for orientation, dr, dc in dirs[-1]:
                new_coord = r + dr, c + dc
                new_path = orientation, r + dr, c + dc
                if new_coord in legal:
                    result_append(new_path)
                    path_append(new_coord)
                    legal_remove(new_coord)
                    dirs_append(iter(DIRS))
                    if not legal:
                        yield result
                    break
            else:
                result_pop()
                legal_add(path_pop())
                dirs_pop()


def write_termios(road,height,TURN):
    #os.system('clear')
    if TURN == 0 :
        for i in range(height+2):
            print()

    for i in range(height+2):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")

    for i in range(height):
        print(road[i])
    print()
    print('Turn : {}'.format(TURN))
    time.sleep(1)


class _hamilton(unittest.TestCase):

    def _screen(self):
        global TURN
        TURN = 1
        ROAD = []
        ROAD.append('...XXX...')
        ROAD.append('XXXXXX...')
        ROAD.append('XXX......')
        ROAD.append('XXXXXXXXX')
        HEIGHT = 4

        for i in range(3):
            write_termios(ROAD,HEIGHT)
            TURN += 1

    def _hamilton(self):
        global TURN
        TURN = 0
        start_time = time.time()
        n_solutions = 0
        puzzle = HamiltonSolver(PUZZLE_GRID)
        for solution in puzzle.solve():
            if n_solutions == 0:
                #print(solution)
                for i in range(len(solution)):
                    print(puzzle.read_turn(solution,i))
                print(puzzle.format_solution(solution))
                print("Found in {} s".format(time.time() - start_time))
            n_solutions += 1
        print("{} solution found in {} s".format(n_solutions ,time.time() - start_time))

    def test_screen_hamilton(self):
        global TURN
        TURN = 0
        start_time = time.time()
        n_solutions = 0
        puzzle = HamiltonSolver(ROAD_GRID)
        _soluce = None
        for solution in puzzle.solve():
            _soluce = solution
            break

        for i in range(len(_soluce)):
            o, r, c = puzzle.read_turn(solution,i)
            l_road = list(ROAD_GRID[r])
            l_road[c] = o
            ROAD_GRID[r] = ''.join(l_road)
            write_termios(ROAD_GRID, len(ROAD_GRID), TURN)
            TURN += 1


if __name__ == '__main__':
    unittest.main()
