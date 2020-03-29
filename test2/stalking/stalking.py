import sys
sys.path.append('../../')

# Global variables
from test2.test_main import TREASURE_MAP

# From OceanOfCode
# Class
from OceanOfCode import StalkAndLegal
from OceanOfCode import StalkAndTorpedo
from OceanOfCode import Submarine
from OceanOfCode import Board

# Global
from OceanOfCode import EMPTY_SYMBOLS
from OceanOfCode import DIRS

import unittest

class _staling(unittest.TestCase):

    def test_set_up(self):
        me = StalkAndTorpedo(None)
        me.set_up(TREASURE_MAP)
        print(len(me.inp))

    def test_set_up(self):
        me = StalkAndTorpedo(None)
        me.set_up(TREASURE_MAP)
        print(len(me.inp))

        read_move = StalkAndTorpedo.read_move
        me.update(read_move,'N')
        me = StalkAndTorpedo(me)
        print(len(me.inp))

        #me.update(read_move,'E')
        #me = StalkAndTorpedo(me)
        #print(len(me.inp))


if __name__ == '__main__':
    unittest.main()
