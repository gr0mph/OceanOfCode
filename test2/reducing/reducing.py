import sys
sys.path.append('../../')
import random

# Global variables
from test2.test_map import TREASURE_MAP

# From OceanOfCode
# Class
from OceanOfCode import Node
from OceanOfCode import PathSolving

# Global
from OceanOfCode import EMPTY_SYMBOLS
from OceanOfCode import DIRS

import unittest

class _reducing(unittest.TestCase):

    def _global(self):
        for t_r in TREASURE_MAP:
            print(t_r)

    def test_set_up(self):
        print()
        for t_r in TREASURE_MAP:
            print(t_r)

        me = PathSolving(None)
        me.set_up(TREASURE_MAP)

        print("PathSolving Len {}".format(len(me.legal)))

        me.update()
        print("PathSolving Len {} Len {}".format(len(me.legal),len(me.risk)))

        for t_r in me.grid:
            print(t_r)

        me.update_sector()

        coord, me.last = next(iter(me.sector[5].items()))
        result = me.solve(6)

        for r1 in result :
            print(r1)

if __name__ == '__main__':
    unittest.main()
