import sys
sys.path.append('../../')
import random
import copy
import time

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
from OceanOfCode import LAST
from OceanOfCode import SECTOR_REDUCING

# Function
from OceanOfCode import sector

import unittest

class _reducing(unittest.TestCase):

    def _global(self):
        for t_r in TREASURE_MAP:
            print(t_r)

    def _set_up(self):
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

        for type, path in me.solve(0):
            if len(save) == 0 and type == FIRST:
                save = copy.deepcopy(path)  # This data is ephemerate
            elif len(save) == 0 and type == LAST:
                save = copy.deepcopy(path)  # This data is ephemerate
            elif type == HAMILTON :
                save = path
        result.extend(save)
        save = []
        me.next_sector(result)
        print(result[-1])

    def test_last(self):
        me = PathSolving(None)
        me.set_up(TREASURE_MAP)
        me.update()
        me.update_sector()

        # First node
        coord, me.last = next(iter(me.sector[5].items()))
        del me.sector[5][coord]

        path_solving = []
        iter_sector_reducing, sector_next = iter(SECTOR_REDUCING), -1


        while True:
            if sector_next != 0 :
                sector_next = next(iter_sector_reducing)
                result = me.solve_sector(sector_next)
                path_solving.extend(result)
                me.next_sector(path_solving)
                print(path_solving[-1])
            else:
                break

        choice = 0

        iter_forward = iter(path_solving)
        iter_backward = iter(reversed(path_solving))

        p1_forward = next(iter_forward)
        p1_backward = next(iter_backward)
        print('({},{})'.format(p1_forward.x,p1_forward.y),flush=True)

        while True:
            if choice == 0:
                #print("FORWARD")
                p1_forward = next(iter_forward)
                time.sleep(0.1)
                print('({},{})'.format(p1_forward.x,p1_forward.y),flush=True,end='\t')

                if p1_forward == p1_backward:
                    choice = 1
                    iter_forward = iter(path_solving)
                    p1_forward = next(iter_forward)
                    print()
                    print("NEED SURFACE")

            elif choice == 1:
                #print("BACKWARD")
                p1_backward = next(iter_backward)
                time.sleep(0.1)
                print('({},{})'.format(p1_backward.x,p1_backward.y),flush=True,end='\t')

                if p1_forward == p1_backward:
                    choice = 0
                    iter_backward = iter(reversed(path_solving))
                    p1_backward = next(iter_backward)
                    print()
                    print("NEED SURFACE")

if __name__ == '__main__':
    unittest.main()
