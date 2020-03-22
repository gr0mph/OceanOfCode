# Global Data
from sector.sector import TREASURE_MAP

# Function
from sector.sector import sector
from sector.sector import select
from hamilton.hamilton import write_termios

# Class
from hamilton.hamilton import HamiltonSolver as Hamilton

EMPTY_SPACE_SYMBOLS = '.'
STARTING_POINT_SYMBOLS = 'Ss'
OBSTACLE_SYMBOL = 'X'
DIRS = [('N',-1, 0), ('S',1, 0), ('E',0, 1), ('W',0, -1)]
TURN = 0

# Unittest
import unittest

class _path_solver(unittest.TestCase):

    def test_previous_0_sector(self):
        print()
        print('x {} y {} s {} '.format(3,9,sector(3,9)))

    def test_previous_1_select(self):
        print()
        r, c, SELECT_MAP = select(5,TREASURE_MAP)
        for line in SELECT_MAP:
            print(line)

    def test_previous_2_hamilton(self):
        print()
        global TURN
        r, c, SELECT_MAP = select(5,TREASURE_MAP)
        puzzle = Hamilton(SELECT_MAP)
        _soluce = None
        for solution in puzzle.solve():
            _soluce = solution
            break

        for i in range(len(_soluce)):
            o, r, c = puzzle.read_turn(solution,i)
            l_road = list(SELECT_MAP[r])
            l_road[c] = o
            SELECT_MAP[r] = ''.join(l_road)
            write_termios(SELECT_MAP, len(SELECT_MAP), TURN)
            TURN += 1


if __name__ == '__main__':
    unittest.main()
