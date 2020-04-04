import sys
sys.path.append('../../')

# Global variables
from test2.test_main import TREASURE_MAP

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

    def test_set_up(self):
        print("0. START test_set_up")
        me = MineAndTrigger(None)
        me.set_up(TREASURE_MAP)
        print(len(me.legal))

    def test_mine(self):
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


if __name__ == '__main__':
    unittest.main()
