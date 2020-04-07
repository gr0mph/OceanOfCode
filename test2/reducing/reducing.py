import sys
sys.path.append('../../')

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
        me = PathSolving(None)
        me.set_up(TREASURE_MAP)
        print("PathSolving Len {}".format(len(me.legal)))

        #for l1 in me.legal:
        #    print(l1)

        me.update()

        for t_r in me.grid:
            print(t_r)


if __name__ == '__main__':
    unittest.main()
