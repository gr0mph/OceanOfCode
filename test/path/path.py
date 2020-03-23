import unittest
import time
import os
import sys

TURN = 1

EMPTY_SPACE_SYMBOLS = '.'
STARTING_POINT_SYMBOLS = 'Ss'
FINISHING_POINT_SYMBOLS = 'Ff'
OBSTACLE_SYMBOL = 'X'
DIRS = [('N',-1, 0), ('S',1, 0), ('E',0, 1), ('W',0, -1)]

class PathFinding:
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
        self.finish = None
        self.legal = set()
        for r, row in enumerate(grid):
            for c, item in enumerate(row):
                if item in STARTING_POINT_SYMBOLS:
                    print('A START has been find')
                    self.start = (r, c)
                elif item in EMPTY_SPACE_SYMBOLS:
                    self.legal.add((r, c))
                elif item in FINISHING_POINT_SYMBOLS:
                    print('A FINISH has been find')
                    self.finish = (r,c)

    def read_turn(self,path,turn):
        return path[turn]

    def solve(self):
        """Generate solutions as lists of coordinates."""
        print("SOLVE THIS")
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
                print('New: {} Finish: {}'.format(new_coord,self.finish))
                if new_coord in legal:
                    result_append(new_path)
                    path_append(new_coord)
                    legal_remove(new_coord)
                    dirs_append(iter(DIRS))
                    break
                if new_coord == self.finish:
                    print("NEVER ?")
                    yield result

            else:
                result_pop()
                legal_add(path_pop())
                dirs_pop()


if __name__ == '__main__':
    unittest.main()
