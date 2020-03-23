# Global Data
from sector.sector import TREASURE_MAP
from sector.sector import TRANSIT_SET

# Function
from sector.sector import sector
from sector.sector import select
from sector.sector import prepare
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

    def test_previous_3_prepare(self):
        print()
        TRANSIT_GLOBAL = []
        TRANSIT_GLOBAL.append(list('...'))
        TRANSIT_GLOBAL.append(list('...'))
        TRANSIT_GLOBAL.append(list('...'))

        # TODO: Incomplete
        TRANSIT_SECTOR = prepare(TREASURE_MAP)
        if len(TRANSIT_SECTOR['1S']) == 0 and len(TRANSIT_SECTOR['1W']) == 0:
            TRANSIT_GLOBAL[0][0] = 'x'

        if len(TRANSIT_SECTOR['3S']) == 0 and len(TRANSIT_SECTOR['3E']) == 0:
            TRANSIT_GLOBAL[0][2] = 'x'

        if len(TRANSIT_SECTOR['7N']) == 0 and len(TRANSIT_SECTOR['7W']) == 0:
            TRANSIT_GLOBAL[2][0] = 'x'

        if len(TRANSIT_SECTOR['9N']) == 0 and len(TRANSIT_SECTOR['9E']) == 0:
            TRANSIT_GLOBAL[2][2] = 'x'

        for g in TRANSIT_GLOBAL:
            g = ''.join(g)
            print(g)

        TEST = []
        TEST.append('S..')
        TEST.append('...')
        TEST.append('...')

        global TURN
        TURN = 0
        _soluce = None
        puzzle = Hamilton(TEST)
        for solution in puzzle.solve():
            _soluce = solution
            break

        for i in range(len(_soluce)):
            o, r, c = puzzle.read_turn(solution,i)
            l_road = list(TEST[r])
            l_road[c] = o
            TEST[r] = ''.join(l_road)
            write_termios(TEST, len(TEST), TURN)
            TURN += 1

        TEST2 = []
        TEST2.append('...')
        TEST2.append('...')
        TEST2.append('...')
        puzzle = Hamilton(TEST2)
        iterable_hamilton = puzzle.solve()
        puzzle.change_start()
        puzzle.change_start()
        iterable_hamilton = puzzle.solve()
        for solution in iterable_hamilton:
            _soluce = solution
            break

        TURN = 0
        for i in range(len(_soluce)):
            o, r, c = puzzle.read_turn(solution,i)
            l_road = list(TEST2[r])
            l_road[c] = o
            TEST2[r] = ''.join(l_road)
            write_termios(TEST2, len(TEST2), TURN)
            TURN += 1


if __name__ == '__main__':
    unittest.main()
