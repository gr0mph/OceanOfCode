import sys
sys.path.append('../../')
import random
import copy
import time

# Global variables
from test_case.weird_map.test_weird_map import TREASURE_MAP
from test_case.weird_map.test_weird_map import TRANSIT_MAP

# From OceanOfCode
# Class
from OceanOfCode import Node
from OceanOfCode import PathSolving
from OceanOfCode import StrategyStarting
from OceanOfCode import Planning
from OceanOfCode import Board

# Global
from OceanOfCode import EMPTY_SYMBOLS
from OceanOfCode import DIRS
from OceanOfCode import k_PATH_HAMILTON
from OceanOfCode import k_PATH_FIRST
from OceanOfCode import k_PATH_LAST
from OceanOfCode import k_PATH_MAX

from OceanOfCode import SECTOR_REDUCING
from OceanOfCode import SECTOR_TRANSIT
from OceanOfCode import MY_ID
from OceanOfCode import GET_DIRS

# Function
from OceanOfCode import sector

import unittest

class _reducing(unittest.TestCase):

    def _global(self):
        for t_r in TREASURE_MAP:
            print(t_r)

    def _set_up(self):
        for t_r in TREASURE_MAP:
            print(''.join(t_r))
        print()

        me = PathSolving(None)
        me.set_up(TREASURE_MAP)
        me.update()

        for line1 in me.grid :
            print(''.join(line1))
        print()

        me.update_sector()

        REDUCE_MAP = me.grid

    def _tuple(self):
        print()
        t_base = (6,3,2,1,4,7,8,9)
        t_test1 = (6,3)
        t_test2 = (6,9)

        if ''.join(str(c) for c in t_test1) in ''.join(str(c) for c in t_base):
            print("OKAY test1")
        else:
            print("KO test1")

        if ''.join(str(c) for c in t_test2) in ''.join(str(c) for c in t_base):
            print("KO test2")
        else:
            print("OKAY test2")

    def _big_solving(self):

        me = PathSolving(None)
        me.set_up(TREASURE_MAP)
        me.update()

        me.update_sector()
        REDUCE_MAP = me.grid

        print()
        print("TREASURE_MAP",end='\t')
        print("REDUCE_MAP")
        for t_r, m_r in zip(TREASURE_MAP, REDUCE_MAP):
            print(''.join(t_r),end='\t')
            print(''.join(m_r))

        # First node
        previous_sector = 5
        previous_sector_a, previous_sector_b = 0,0
        coord, me.last = next(iter(me.sector[previous_sector].items()))
        del me.sector[5][coord]

        path_solving = []
        iter_sector_reducing, sector_next = None, -1

        while True:
            if sector_next == 0 :
                break
            elif sector_next == -1:
                k_next_tuple = SECTOR_TRANSIT[previous_sector]
                result = me.solve_sector(k_next_tuple)
                path_solving.extend(result)
                me.next_sector(path_solving)
                print(path_solving[-1])
                if previous_sector_a == 0:
                    previous_sector = previous_sector_a = sector(path_solving[-1])
                else :
                    previous_sector = previous_sector_b = sector(path_solving[-1])
                    t_sector_reducing = (previous_sector_a,previous_sector_b)
                    iter_sector_reducing = iter(SECTOR_REDUCING[t_sector_reducing])
                    next(iter_sector_reducing)
                    sector_next = next(iter_sector_reducing)


            else :
                sector_next = next(iter_sector_reducing)
                result = me.solve_sector([sector_next])
                path_solving.extend(result)
                me.next_sector(path_solving)
                print(path_solving[-1])

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

    def test_weird(self):

        g_strategy_state = StrategyStarting(None)
        kanban_path  = PathSolving(None)
        kanban_plan = Planning(None)
        game_board = [None, None]
        game_board[MY_ID] = Board(game_board[MY_ID])

        REDUCE_MAP = copy.deepcopy(TREASURE_MAP)
        kanban_plan.forward = g_strategy_state.set_up(kanban_path,REDUCE_MAP)
        REDUCE_MAP = kanban_path.grid

        print()
        print("TREASURE_MAP",end='\t')
        print("REDUCE_MAP")
        for t_r, m_r in zip(TREASURE_MAP, REDUCE_MAP):
            print(''.join(t_r),end='\t')
            print(''.join(m_r))


if __name__ == '__main__':
    unittest.main()
