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
from OceanOfCode import SECTOR_TRANSIT

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
        global SECTOR_TRANSIT
        me = PathSolving(None)
        me.set_up(TREASURE_MAP)
        me.update()
        me.update_sector()

        # First node
        previous_sector = 5
        previous_sector_a, previous_sector_b = 0,0
        coord, me.last = next(iter(me.sector[5].items()))
        del me.sector[5][coord]

        path_reducing = []
        iter_sector_reducing, sector_next = None, -1

        # From true code
        kanban_path = me

        while True:
            if sector_next == 0 :
                break

            elif sector_next == -1:
                k_next_tuple = SECTOR_TRANSIT[previous_sector]
                result = kanban_path.solve_sector(k_next_tuple)
                path_reducing.extend(result[1:])
                kanban_path.next_sector(path_reducing)
                if previous_sector_a == 0:
                    previous_sector = previous_sector_a = sector(path_reducing[-1])
                else :
                    previous_sector = previous_sector_b = sector(path_reducing[-1])
                    t_sector_reducing = (previous_sector_a,previous_sector_b)
                    iter_sector_reducing = iter(SECTOR_REDUCING[t_sector_reducing])
                    next(iter_sector_reducing)
                    sector_next = next(iter_sector_reducing)

            else :
                sector_next = next(iter_sector_reducing)
                print("Sector next: {}".format(sector_next),file=sys.stderr)
                result = kanban_path.solve_sector([sector_next])
                path_reducing.extend(result[1:])
                kanban_path.next_sector(path_reducing)

        choice = 0

        iter_forward = iter(path_reducing)
        iter_backward = iter(reversed(path_reducing))

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
                    iter_forward = iter(path_reducing)
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
                    iter_backward = iter(reversed(path_reducing))
                    p1_backward = next(iter_backward)
                    print()
                    print("NEED SURFACE")

if __name__ == '__main__':
    unittest.main()
