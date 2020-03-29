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
        print(me)


if __name__ == '__main__':
    unittest.main()
