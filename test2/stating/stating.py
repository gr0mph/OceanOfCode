import sys
sys.path.append('../../')
import random
import copy
import time

# Global variables
from test2.test_map import TREASURE_MAP

# From OceanOfCode
# Class
from OceanOfCode import Board

# Global
from OceanOfCode import STATE_MOVE
from OceanOfCode import state

# Function
from OceanOfCode import update_agent
#from OceanOfCode import update_state

class FalseKanbanOpp():

    def __init__(self,clone):
        self.inp = [None] * 10


import unittest

class _stating(unittest.TestCase):

    def _state(self):
        global state
        kanban_opp = FalseKanbanOpp(None)
        board = Board(None)

        turn = 1
        state = update_state(state,turn,board,kanban_opp)

        print(state)

        turn = 20
        board.silence = 5
        state = update_state(state,turn,board,kanban_opp)

        print(state)

        turn = 20
        board.silence = 0
        state = update_state(state,turn,board,kanban_opp)

        print(state)

        kanban_opp.inp = [None] * 50

        state = update_state(state,turn,board,kanban_opp)

        print(state)

    def _agent(self):
        global state
        kanban_opp = FalseKanbanOpp(None)
        board = Board(None)

        turn = 1
        state = update_state(state,turn,board,kanban_opp)
        text = update_agent(state,board)

        print("Check 0 and silence")
        print(state)
        print(text)

        turn = 20
        board.silence = 5
        state = update_state(state,turn,board,kanban_opp)
        text = update_agent(state,board)

        print("Check 0 and silence")
        print(state)
        print(text)

        turn = 20
        board.silence = 0
        board.torpedo = 3
        state = update_state(state,turn,board,kanban_opp)
        text = update_agent(state,board)

        print("Check 2 and torpedo")
        print(state)
        print(text)

        board.torpedo = 0
        board.mine = 1

        state = update_state(state,turn,board,kanban_opp)
        text = update_agent(state,board)

        print("Check 2 and mine")
        print(state)
        print(text)


        kanban_opp.inp = [None] * 50

        state = update_state(state,turn,board,kanban_opp)
        text = update_agent(state,board)

        print("Check 1 and sonar")
        print(state)
        print(text)

    def test_no(self):
        print("===================================================")
        print("== update state method has been replaced by code ==")
        print("===================================================")

if __name__ == '__main__':
    unittest.main()
