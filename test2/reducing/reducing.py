import sys
sys.path.append('../../')
import random
import copy

# Global variables
from test2.test_map import TREASURE_MAP

# From OceanOfCode
# Class
from OceanOfCode import Node
from OceanOfCode import PathSolving

# Global
from OceanOfCode import EMPTY_SYMBOLS
from OceanOfCode import DIRS
from OceanOfCode import HAMILTON
from OceanOfCode import FIRST

# Function
from OceanOfCode import sector

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
        del me.sector[5][coord]
        result,save = [], []
        for type, path in me.solve(6):
            if len(save) == 0 :
                save = path
            elif type == HAMILTON :
                save = path
        result.extend(save)
        save = []
        #me.last = result[-1]
        #k_coord = me.last.y, me.last.x
        #k_sector = sector(me.last)
        #del me.sector[k_sector][k_coord]
        me.next_sector(result)
        print(result[-1])

        for type, path in me.solve(3):
            if len(save) == 0 :
                save = path
            elif type == HAMILTON :
                save = path
        result.extend(save)
        save = []
        me.next_sector(result)
        print(result[-1])

        for type, path in me.solve(2):
            if len(save) == 0 :
                save = path
            elif type == HAMILTON :
                save = path
        result.extend(save)
        save = []
        me.next_sector(result)
        print(result[-1])

        for type, path in me.solve(1):
            if len(save) == 0 :
                save = path
            elif type == HAMILTON :
                save = path
        result.extend(save)
        save = []
        me.next_sector(result)
        print(result[-1])

        for type, path in me.solve(4):
            if len(save) == 0 and type == FIRST:
                save = copy.deepcopy(path)  # This data is ephemerate
            elif type == HAMILTON :
                save = path

        result.extend(save)
        save = []
        me.next_sector(result)
        print(result[-1])

        for type, path in me.solve(7):
            if len(save) == 0 and type == FIRST:
                save = copy.deepcopy(path)  # This data is ephemerate
            elif type == HAMILTON :
                save = path
        result.extend(save)
        save = []
        me.next_sector(result)
        print(result[-1])

        for type, path in me.solve(8):
            if len(save) == 0 and type == FIRST:
                save = copy.deepcopy(path)  # This data is ephemerate
            elif type == HAMILTON :
                save = path
        result.extend(save)
        save = []
        me.next_sector(result)
        print(result[-1])

        for type, path in me.solve(9):
            if len(save) == 0 and type == FIRST:
                save = copy.deepcopy(path)  # This data is ephemerate
            elif type == HAMILTON :
                save = path
        result.extend(save)
        save = []
        me.next_sector(result)
        print(result[-1])

        #for r1 in result :
        #    print(r1)

if __name__ == '__main__':
    unittest.main()
