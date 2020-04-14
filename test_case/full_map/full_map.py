import sys
sys.path.append('../../')
import random
import copy
import time

# Global variables
from test_case.full_map.test_full_map import TREASURE_MAP

# From OceanOfCode
# Class
from OceanOfCode import Node
from OceanOfCode import PathSolving

# Global
from OceanOfCode import HEIGHT
from OceanOfCode import EMPTY_SYMBOLS
from OceanOfCode import DIRS
#from OceanOfCode import k_PATH_HAMILTON
#from OceanOfCode import k_PATH_FIRST
#from OceanOfCode import k_PATH_LAST
from OceanOfCode import SECTOR_REDUCING
from OceanOfCode import SECTOR_TRANSIT

# Function
from OceanOfCode import sector
from OceanOfCode import t_check_map

import unittest

class StrategyStarting():

    def __init__(self,clone):
        self.previous_sector = 5
        self.previous_sector_a, self.previous_sector_b = 0, 0
        self.iter_sector_reducing, self.sector_next = None, -1
        self.turn = 0
        pass

    def set_up(self,kanban_path,TREASURE_MAP):
        print("TREASURE_MAP",file=sys.stderr)
        for t_r in TREASURE_MAP:
            print(t_r,file=sys.stderr)

        kanban_path.set_up(TREASURE_MAP)
        kanban_path.update()

        REDUCE_MAP = kanban_path.grid

        print("REDUCE_MAP",file=sys.stderr)
        for t_r in REDUCE_MAP:
            print(t_r,file=sys.stderr)

        kanban_path.update_sector()

        print(self.previous_sector)
        coord, kanban_path.last = next(iter(kanban_path.sector[self.previous_sector].items()))
        del kanban_path.sector[5][coord]

        path_reducing = []
        path_reducing.append(kanban_path.last)

        return path_reducing

    def path(self,kanban_path,path_reducing):
        self.turn+= 1
        if self.sector_next == 0 :
            pass

        elif self.sector_next == -1:
            k_next_tuple = SECTOR_TRANSIT[self.previous_sector]
            result = kanban_path.solve_sector(k_next_tuple)
            path_reducing.extend(result[1:])
            kanban_path.next_sector(path_reducing)
            if self.previous_sector_a == 0:
                self.previous_sector = self.previous_sector_a = sector(path_reducing[-1])
            else :
                self.previous_sector = self.previous_sector_b = sector(path_reducing[-1])
                t_sector_reducing = (self.previous_sector_a,self.previous_sector_b)
                self.iter_sector_reducing = iter(SECTOR_REDUCING[t_sector_reducing])
                next(self.iter_sector_reducing)
                self.sector_next = next(self.iter_sector_reducing)

        else :
            self.sector_next = next(self.iter_sector_reducing)
            print("Sector next: {}".format(self.sector_next),file=sys.stderr)
            result = kanban_path.solve_sector([self.sector_next])
            path_reducing.extend(result[1:])
            kanban_path.next_sector(path_reducing)

        return path_reducing



class _reducing(unittest.TestCase):

    def _global(self):
        for t_r in TREASURE_MAP:
            print(t_r)

    def test_reducing(self):

        g_strategy_state = StrategyStarting(None)
        kanban_path  = PathSolving(None)

        path_reducing = g_strategy_state.set_up(kanban_path,TREASURE_MAP)

        # TURN 0
        iter_forward = iter(path_reducing)
        iter_backward = iter(reversed(path_reducing))

        p1_forward = next(iter_forward)
        p1_backward = next(iter_backward)

        i1 = 0
        print("TURN {} : print ({},{})".format(i1,p1_forward.x,p1_forward.y))

        for i1 in range(1,10):
                path_reducing = g_strategy_state.path(kanban_path,path_reducing)

                p1_forward = next(iter_forward)

                print("TURN {} : move ({},{})".format(i1,p1_forward.x,p1_forward.y))

                path_reducing = g_strategy_state.path(kanban_path,path_reducing)

        i1 += 1
        p1_forward = next(iter_forward)
        print("TURN {} : move ({},{})".format(i1,p1_forward.x,p1_forward.y))





if __name__ == '__main__':
    unittest.main()
