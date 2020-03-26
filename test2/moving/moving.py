import sys
sys.path.append('../../')

# Global variables
from test2.test_main import TREASURE_MAP

# From OceanOfCode
# Class
from OceanOfCode import HamiltonSolver
from OceanOfCode import Submarine
from OceanOfCode import Board

# Global
from OceanOfCode import STARTING_SYMBOLS
from OceanOfCode import FINISHING_SYMBOLS
from OceanOfCode import EMPTY_SYMBOLS
from OceanOfCode import DIRS
from OceanOfCode import DEEP
from OceanOfCode import GET_DIRS

import unittest

class _moving(unittest.TestCase):

    def _global(self):
        for t_r in TREASURE_MAP:
            print(t_r)

    def _class(self):
        me = Board(None)
        me.treasure_map = TREASURE_MAP
        puzzle = HamiltonSolver(me.treasure_map)

    def test_first_position(self):
        me = Board(None)
        me.treasure_map = TREASURE_MAP
        puzzle = HamiltonSolver(me.treasure_map)
        if puzzle.start == None :
            y_row , x_col = puzzle.coord_random()
            puzzle.start = y_row, x_col
            me.treasure_map[x_col][y_row] = ' '
            puzzle.legal.remove( (y_row,x_col) )
            me.x, me.y = x_col, y_row

        # TODO PRINT

        if puzzle.finish == None :
            y_row , x_col = puzzle.coord_random()
            puzzle.finish = y_row, x_col

        print(puzzle.start)
        print(puzzle.finish)

        for t_r in me.treasure_map:
            print(t_r)

        #for solution in puzzle.solve() :
        solution = puzzle.solve()
        print('HERE')
        y_row , x_col = puzzle.read_turn(solution,1)
        me.treasure_map[x_col][y_row] = ' '
        dir = GET_DIRS[ (x_col - me.x, y_row - me.y)]
        me.write_move(dir,'TORPEDO')
        print(me.out)


if __name__ == '__main__':
    unittest.main()
