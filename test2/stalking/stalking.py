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

# Method
from OceanOfCode import manhattan
from OceanOfCode import update_order

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

        me.update(read_move,['N'])
        me = StalkAndTorpedo(me)
        print(len(me.inp))

        me.update(read_move,['E'])
        me = StalkAndTorpedo(me)
        print(len(me.inp))

        me.update(read_move,['S'])
        me = StalkAndTorpedo(me)
        print(len(me.inp))

        me.update(read_move,['S'])
        me = StalkAndTorpedo(me)
        print(len(me.inp))

        me.update(read_move,['W'])
        me = StalkAndTorpedo(me)
        print(len(me.inp))

    def _read_surface(self):
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

    def _read_torpedo(self):
        me = StalkAndTorpedo(None)
        me.set_up(TREASURE_MAP)
        print(len(me.inp))

        read_torpedo = StalkAndTorpedo.read_torpedo

        me.update(read_torpedo,(8,4))
        me = StalkAndTorpedo(me)
        print(len(me.inp))

        me.update(read_torpedo,(6,6))
        me = StalkAndTorpedo(me)
        print(len(me.inp))

    def _read_silence(self):
        me = StalkAndTorpedo(None)
        me.set_up(TREASURE_MAP)
        print(len(me.inp))

        read_torpedo = StalkAndTorpedo.read_torpedo
        read_silence = StalkAndTorpedo.read_silence

        me.update(read_torpedo,(8,4))
        me = StalkAndTorpedo(me)
        print(len(me.inp))

        me.update(read_torpedo,(5,6))
        me = StalkAndTorpedo(me)
        print(len(me.inp))

        me.update(read_silence,None)
        me = StalkAndTorpedo(me)
        print(len(me.inp))


    def _small_read_and_update(self):
        me = StalkAndTorpedo(None)
        me.set_up(TREASURE_MAP)
        print(len(me.inp))

        for c1, f1, d1 in update_order('MOVE N'):
            print("c1 {} f1 {} d1 {}".format(c1,f1,d1))
            me.update(f1,d1)
            me = StalkAndTorpedo(me)

        print(len(me.inp))

        for c1, f1, d1 in update_order('TORPEDO 0 0|MOVE E'):
            print("c1 {} f1 {} d1 {}".format(c1,f1,d1))
            me.update(f1,d1)
            me = StalkAndTorpedo(me)

        print(len(me.inp))

        for c1, f1, d1 in update_order('SURFACE 1'):
            print("c1 {} f1 {} d1 {}".format(c1,f1,d1))
            me.update(f1,d1)
            me = StalkAndTorpedo(me)

        print(len(me.inp))


    def _medium_read_and_update(self):
        me = StalkAndTorpedo(None)
        me.set_up(TREASURE_MAP)
        print(len(me.inp))

        for c1, f1, d1 in update_order('MOVE N|SURFACE 5|TORPEDO 11 1|SILENCE'):
            print("c1 {} f1 {} d1 {}".format(c1,f1,d1))
            if f1 is not None:
                me.update(f1,d1)
                me = StalkAndTorpedo(me)

        print(len(me.inp))

    def _na_read(self):

        me = StalkAndTorpedo(None)
        me.set_up(TREASURE_MAP)
        print(len(me.inp))

        for c1, f1, d1 in update_order('NA'):
            print("c1 {} f1 {} d1 {}".format(c1,f1,d1))

    def test_silence(self):
        for t_r in TREASURE_MAP:
            print(t_r)

        me = StalkAndTorpedo(None)
        me.set_up(TREASURE_MAP)
        print(len(me.inp))

        for c1, f1, d1 in update_order('MOVE N|SILENCE'):
            print("c1 {} f1 {} d1 {}".format(c1,f1,d1))
            if f1 is not None:
                me.update(f1,d1)
                me = StalkAndTorpedo(me)
                print(len(me.inp))

        for c1, f1, d1 in update_order('MOVE N|MOVE N'):
            print("c1 {} f1 {} d1 {}".format(c1,f1,d1))
            if f1 is not None:
                me.update(f1,d1)
                me = StalkAndTorpedo(me)
                print(len(me.inp))





if __name__ == '__main__':
    unittest.main()
