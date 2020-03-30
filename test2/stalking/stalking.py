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

    def _set_up(self):
        me = StalkAndTorpedo(None)
        me.set_up(TREASURE_MAP)
        print(len(me.inp))

    def _read_move(self):
        me = StalkAndTorpedo(None)
        me.set_up(TREASURE_MAP)
        print(len(me.inp))

        read_move = StalkAndTorpedo.read_move

        me.update(read_move,'N')
        me = StalkAndTorpedo(me)
        print(len(me.inp))

        me.update(read_move,'E')
        me = StalkAndTorpedo(me)
        print(len(me.inp))

        me.update(read_move,'S')
        me = StalkAndTorpedo(me)
        print(len(me.inp))

        me.update(read_move,'S')
        me = StalkAndTorpedo(me)
        print(len(me.inp))

        me.update(read_move,'W')
        me = StalkAndTorpedo(me)
        print(len(me.inp))

    def test_read_surface(self):
        me = StalkAndTorpedo(None)
        me.set_up(TREASURE_MAP)

        read_surface = StalkAndTorpedo.read_surface

        for i in range(0,5):
            me.update(read_surface,TREASURE_MAP)
            me = StalkAndTorpedo(me)
            board, stalk = next(iter(me.inp))
            print(len(me.inp))
            print(board.life)

        me.update(read_surface,TREASURE_MAP)
        me = StalkAndTorpedo(me)
        print()
        print(len(me.inp))






if __name__ == '__main__':
    unittest.main()
