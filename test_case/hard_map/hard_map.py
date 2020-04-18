import sys
sys.path.append('../../')
import random
import copy
import time

# Global variables
from test_case.hard_map.test_hard_map import TREASURE_MAP

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

class _hard_map(unittest.TestCase):

    def test_hard(self):

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
