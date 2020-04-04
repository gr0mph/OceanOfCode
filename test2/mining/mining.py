import sys
sys.path.append('../../')

# Global variables
from test2.test_main import TREASURE_MAP
from test2.test_main import MINE_MAP

# From OceanOfCode
# Class
from OceanOfCode import MineAndTrigger
from OceanOfCode import Submarine
from OceanOfCode import Board

# Global
from OceanOfCode import EMPTY_SYMBOLS
from OceanOfCode import DIRS

# Method
from OceanOfCode import square

import unittest

class _mining(unittest.TestCase):

    def _set_up(self):
        print("0. START test_set_up")
        me = MineAndTrigger(None)
        me.set_up(TREASURE_MAP)
        print(len(me.legal))

    def _mine(self):
        print("1. START test_mine")

        me = MineAndTrigger(None)
        me.set_up(TREASURE_MAP)
        print("Length: {}".format(len(me.legal)))

        board = Board(None)
        board.x,board.y = 10,3

        orientation = me.mine(board)
        for p in me.minefield:
            print(p)
        me = MineAndTrigger(me)
        print("Orientation: {} Legal Length: {} Minefield Length {}".format(
        orientation, len(me.legal), len(me.minefield)))

        orientation = me.mine(board)
        for p in me.minefield:
            print(p)
        me = MineAndTrigger(me)
        print("Orientation: {} Legal Length: {} Minefield Length {}".format(
        orientation, len(me.legal), len(me.minefield)))

        orientation = me.mine(board)
        for p in me.minefield:
            print(p)
        me = MineAndTrigger(me)
        print("Orientation: {} Legal Length: {} Minefield Length {}".format(
        orientation, len(me.legal), len(me.minefield)))

        orientation = me.mine(board)
        for p in me.minefield:
            print(p)
        me = MineAndTrigger(me)
        print("Orientation: {} Legal Length: {} Minefield Length {}".format(
        orientation, len(me.legal), len(me.minefield)))

        orientation = me.mine(board)
        for p in me.minefield:
            print(p)
        me = MineAndTrigger(me)
        print("Orientation: {} Legal Length: {} Minefield Length {}".format(
        orientation, len(me.legal), len(me.minefield)))

    def _nearby(self):
        print("3. START test_nearby")

        me = MineAndTrigger(None)
        me.set_up(TREASURE_MAP)
        print("Length: {}".format(len(me.legal)))

        board1 = Board(None)
        board1.x,board1.y = 10,3

        orientation = me.mine(board1)
        for p in me.minefield:
            print(p)
        print("Orientation: {} Legal Length: {} Minefield Length {}".format(
        orientation, len(me.legal), len(me.minefield)))

        board2 = Board(None)
        board2.x,board2.y = 10,3

        mine = me.nearby(board1,board2)
        print("Mine: {}".format(mine))

        if mine is not None:
            me.trigger(mine)

        print("Legal Length: {} Minefield Length {}".format(
        len(me.legal), len(me.minefield)))

        board1.x,board1.y = 5,5
        mine = me.nearby(board1,board2)
        print("Mine: {}".format(mine))

        if mine is not None:
            me.trigger(mine)

        print("Legal Length: {} Minefield Length {}".format(
        len(me.legal), len(me.minefield)))

    def test_filter(self):
        print("4. START test_filter")

        lambda_n = lambda t1, m1 : '.' if t1 == '.' and m1 == '.' else ' '
        for i1 in range(15):
            MINE_MAP[i1] = [ lambda_n(t1,m1) for t1, m1 in zip(TREASURE_MAP[i1],MINE_MAP[i1]) ]

        for t_r in TREASURE_MAP:
            print(t_r)
        for m_r in MINE_MAP:
            print(m_r)


if __name__ == '__main__':
    unittest.main()
