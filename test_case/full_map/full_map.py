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
from OceanOfCode import Board

# Global
from OceanOfCode import HEIGHT
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
from OceanOfCode import t_check_map

import unittest

class Planning():

    def __init__(self,clone):
        self.forward = None
        self.index = 0
        self.is_forward = True


    def __next__(self):
        distance = 0
        if self.is_forward == True and self.index != self.last :
            self.index += 1
            distance = self.last - self.index

        elif self.is_forward == True and self.index == self.last :
            self.index -= 1
            distance = self.index
            self.is_forward = False

        elif self.is_forward == False and self.index != 0 :
            self.index -= 1
            distance = self.index

        elif self.is_forward == False and self.index == 0 :
            self.index += 1
            distance = self.index
            self.is_forward = True

        print(self.index)
        return (distance, self.forward[self.index])

    @property
    def last(self):
        return len(self.forward) - 1

class StrategyStarting():

    def __init__(self,clone):
        self.previous_sector = 5
        self.previous_sector_a, self.previous_sector_b = 0, 0
        self.iter_sector_reducing, self.sector_next = None, -1
        self.turn = 0
        pass

    def set_up(self,kanban_path,TREASURE_MAP):
        kanban_path.set_up(TREASURE_MAP)
        kanban_path.update()

        REDUCE_MAP = kanban_path.grid

        print()
        print("TREASURE_MAP",end='\t')
        print("REDUCE_MAP")
        for t_r, m_r in zip(TREASURE_MAP, REDUCE_MAP):
            print(''.join(t_r),end='\t')
            print(''.join(m_r))

        kanban_path.update_sector()

        print(self.previous_sector)
        coord, kanban_path.last = next(iter(kanban_path.sector[self.previous_sector].items()))
        del kanban_path.sector[5][coord]

        path_reducing = []
        path_reducing.append(kanban_path.last)

        return path_reducing

    def path(self,kanban_path,path_reducing):
        #self.turn+= 1
        if self.sector_next == 0 :
            pass

        elif self.sector_next == -1:
            k_next_tuple = SECTOR_TRANSIT[self.previous_sector]
            type, result = kanban_path.solve_sector(k_next_tuple)
            path_reducing.extend(result[1:])
            kanban_path.next_sector(path_reducing)
            if type == k_PATH_LAST :
                # PERDU pour PERDU
                self.sector_next = 0

            elif self.previous_sector_a == 0:
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
            type, result = kanban_path.solve_sector([self.sector_next])
            path_reducing.extend(result[1:])
            kanban_path.next_sector(path_reducing)
            if type == k_PATH_LAST :
                # PERDU pour PERDU
                self.sector_next = 0

        return path_reducing

    def movement(self, submarine, kanban_path, planning):
        self.turn += 1

        if self.turn < 10 :
            planning.forward = self.path(kanban_path,planning.forward)

        if submarine.silence == 0 :
            distance, p1_next = planning.__next__()
            y_row, x_col = p1_next.y, p1_next.x
            dir = GET_DIRS[ (y_row - submarine.y, x_col - submarine.x)]
            submarine.y, submarine.x = y_row, x_col
            submarine.write_silence(dir,1)

            distance, p1_next = planning.__next__()
            return (True, p1_next)

        else :
            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.write_surface()
            return (False, p1_next)

class StrategyDiscrete():

    def __init__(self,clone):
        self.turn = 0
        if clone is not None :
            self.turn = clone.turn

    def movement(self, submarine, kanban_path, planning):
        self.turn += 1

        if submarine.silence == 0 and submarine.mine == 0 :
            distance, p1_next = planning.__next__()
            if distance < 5 :
                planning.is_forward = False if planning.is_forward else True
                submarine.write_surface()

            y_row, x_col = p1_next.y, p1_next.x
            dir = GET_DIRS[ (y_row - submarine.y, x_col - submarine.x)]
            submarine.y, submarine.x = y_row, x_col
            submarine.write_silence(dir,1)

            distance, p1_next = planning.__next__()
            return (True, p1_next)

        else :
            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.write_surface()
            return (False, p1_next)

class StrategySearching():

    def __init__(self,clone):
        self.turn = 0
        if clone is not None :
            self.turn = clone.turn

    def movement(self, submarine, kanban_path, planning):
        self.turn += 1

        distance, p1_next = planning.__next__()
        if distance == 0 :
            submarine.write_surface()
        return (False, p1_next)

class StrategyMining():

    def __init__(self, clone):
        self.turn = 0
        if clone is not None :
            self.turn = clone.turn

    def movement(self, submarine, kanban_path, planning):
        # In case of MINING and TORPEDO is full
        if submarine.silence == 0 :
            distance, p1_next = planning.__next__()
            if distance < 5 :
                planning.is_forward = False if planning.is_forward else True
                submarine.write_surface()

            y_row, x_col = p1_next.y, p1_next.x
            dir = GET_DIRS[ (y_row - submarine.y, x_col - submarine.x)]
            submarine.y, submarine.x = y_row, x_col
            submarine.write_silence(dir,1)

            distance, p1_next = planning.__next__()
            return (True, p1_next)

        else :
            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.write_surface()
            return (False, p1_next)

class StrategyWaring():

    def __init__(self, clone):
        self.turn = 0
        if clone is not None :
            self.turn = clone.turn

    def movement(self, submarine, kanban_path, planning):
        # In case of MINING and TORPEDO is full
        if submarine.silence == 0 :
            distance, p1_next = planning.__next__()
            if distance < 5 :
                planning.is_forward = False if planning.is_forward else True
                submarine.write_surface()

            y_row, x_col = p1_next.y, p1_next.x
            dir = GET_DIRS[ (y_row - submarine.y, x_col - submarine.x)]
            submarine.y, submarine.x = y_row, x_col
            submarine.write_silence(dir,1)

            distance, p1_next = planning.__next__()
            return (True, p1_next)

        else :
            distance, p1_next = planning.__next__()
            if distance == 0 :
                submarine.write_surface()
            return (False, p1_next)



class _reducing(unittest.TestCase):

    def _global(self):
        for t_r in TREASURE_MAP:
            print(t_r)

    def _reducing(self):

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
            g_strategy_state.turn += 1
            path_reducing = g_strategy_state.path(kanban_path,path_reducing)

            p1_forward = next(iter_forward)

            print("TURN {} : move ({},{})".format(i1,p1_forward.x,p1_forward.y))

            path_reducing = g_strategy_state.path(kanban_path,path_reducing)

        i1 += 1
        p1_forward = next(iter_forward)
        print("TURN {} : move ({},{})".format(i1,p1_forward.x,p1_forward.y))

        print("SOLUCE")
        for i1, p1_forward in enumerate(path_reducing):
            print("[{} : ({},{}) {}]".format(i1,p1_forward.x,p1_forward.y,
            sector(p1_forward)),end='\t')

    def test_movement(self):

        g_strategy_state = StrategyStarting(None)
        kanban_path  = PathSolving(None)
        kanban_plan = Planning(None)
        game_board = [None, None]
        game_board[MY_ID] = Board(game_board[MY_ID])

        kanban_plan.forward = g_strategy_state.set_up(kanban_path,TREASURE_MAP)

        print("TURN {} : print ({},{})".format(g_strategy_state.turn,
        kanban_plan.forward[0].x,kanban_plan.forward[0].y))

        game_board[MY_ID].x = kanban_plan.forward[0].x
        game_board[MY_ID].y = kanban_plan.forward[0].y
        game_board[MY_ID].silence = 3

        for i1 in range(0,200):
            _, p1_next = g_strategy_state.movement(game_board[MY_ID], kanban_path, kanban_plan)
            game_board[MY_ID].x = p1_next.x
            game_board[MY_ID].y = p1_next.y
            print(p1_next)

        g_strategy_state = StrategyDiscrete(g_strategy_state)
        for i1 in range(0,170):
            _, p1_next = g_strategy_state.movement(game_board[MY_ID], kanban_path, kanban_plan)
            game_board[MY_ID].x = p1_next.x
            game_board[MY_ID].y = p1_next.y
            print(p1_next)

        game_board[MY_ID].silence = 0
        game_board[MY_ID].mine = 0
        _, p1_next = g_strategy_state.movement(game_board[MY_ID], kanban_path, kanban_plan)
        game_board[MY_ID].x = p1_next.x
        game_board[MY_ID].y = p1_next.y
        print(p1_next)

        game_board[MY_ID].silence = 6
        game_board[MY_ID].mine = 3
        _, p1_next = g_strategy_state.movement(game_board[MY_ID], kanban_path, kanban_plan)
        game_board[MY_ID].x = p1_next.x
        game_board[MY_ID].y = p1_next.y
        print(p1_next)

        _, p1_next = g_strategy_state.movement(game_board[MY_ID], kanban_path, kanban_plan)
        game_board[MY_ID].x = p1_next.x
        game_board[MY_ID].y = p1_next.y
        print(p1_next)




if __name__ == '__main__':
    unittest.main()
