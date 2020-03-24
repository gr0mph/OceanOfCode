# Global Data
from sector.sector import TREASURE_MAP
from sector.sector import TRANSIT_SET

# Function
from sector.sector import sector
from sector.sector import select
from sector.sector import prepare
from hamilton.hamilton import write_termios
from sector.sector import sectorb

# Class
from hamilton.hamilton import HamiltonSolver as Hamilton
from path.path import PathFinding as SimplePath


EMPTY_SPACE_SYMBOLS = '.'
STARTING_POINT_SYMBOLS = 'Ss'
OBSTACLE_SYMBOL = 'X'
DIRS = [('N',-1, 0), ('S',1, 0), ('E',0, 1), ('W',0, -1)]
TURN = 0
TRANSIT_GLOBAL = []
TRANSIT_GLOBAL.append(list('...'))
TRANSIT_GLOBAL.append(list('...'))
TRANSIT_GLOBAL.append(list('...'))

# Unittest
import unittest
import copy

def treasure_update(TREASURE_MAP,SELECT_MAP,sector):
    t_c1 = ( (0,0,0,5,5,15) , (0,5,0,5,10,15) , (0,10,0,5,15,15) )
    t_r1 = ( (0,5) , (5,10) , (10,15) )
    id_c1 = (sector - 1) % 3
    id_r1 = (sector - 1) // 3
    t1_c1, t1_c2, s1_c1, s1_c2, t2_c1, t2_c2 = t_c1[id_c1]
    t_and_s_r1, t_and_s_r2 = t_r1[id_r1]

    if id_c1 == 1 :
        print("Find it")

    for r1 in range(t_and_s_r1,t_and_s_r2):
        TREASURE_MAP[r1], SELECT_MAP[r1] = list(TREASURE_MAP[r1]), list(SELECT_MAP[r1])
        print("T_MAP[0] {} S_MAP {} T_MAP[1] {}".format(TREASURE_MAP[r1][t1_c1:t1_c2],SELECT_MAP[r1][0:5],TREASURE_MAP[r1][t2_c1:t2_c2]))
        TREASURE_MAP[r1] = TREASURE_MAP[r1][t1_c1:t1_c2] + SELECT_MAP[r1][0:5] + TREASURE_MAP[r1][t2_c1:t2_c2]
        TREASURE_MAP[r1] = ''.join(TREASURE_MAP[r1])
    return TREASURE_MAP

def treasure_next(TRANSIT_SET,TRANSIT_SECTOR,id_sector):
    start_c1, start_r1 = None, None
    finish_c1, finish_r1 = None, None

    t1 = 0
    for t in TRANSIT_SET[id_sector]:
        print('TRANSIT_SET {}'.format(t))
        print('TRANSIT_SECTOR {}'.format(len(TRANSIT_SECTOR[t])))
        for c1, r1 in TRANSIT_SECTOR[t]:
            if t1 == 0 :
                start_c1, start_r1 = c1, r1
            else :
                finish_c1, finish_r1 = c1, r1
            print('TRANSIT_SECTOR : ({},{})'.format(c1,r1))
            t1 += 1
            break
    return start_r1, start_c1, finish_r1, finish_c1

def treasure_transit(TREASURE_MAP,TRANSIT_GLOBAL):
    TRANSIT_SECTOR = prepare(TREASURE_MAP)
    if len(TRANSIT_SECTOR['1S']) == 0 and len(TRANSIT_SECTOR['1W']) == 0:
        TRANSIT_GLOBAL[0][0] = 'x'

    if len(TRANSIT_SECTOR['3S']) == 0 and len(TRANSIT_SECTOR['3E']) == 0:
        TRANSIT_GLOBAL[0][2] = 'x'

    if len(TRANSIT_SECTOR['7N']) == 0 and len(TRANSIT_SECTOR['7W']) == 0:
        TRANSIT_GLOBAL[2][0] = 'x'

    if len(TRANSIT_SECTOR['9N']) == 0 and len(TRANSIT_SECTOR['9E']) == 0:
        TRANSIT_GLOBAL[2][2] = 'x'

    for g in TRANSIT_GLOBAL:
        g = ''.join(g)

    puzzle = Hamilton(TRANSIT_GLOBAL)
    _soluce = None
    nb = 1
    while _soluce is None :
        if nb == 0 :
            puzzle.change_start()
        nb = 0
        for solution in puzzle.solve():
            nb += 1
            _soluce = solution
            break

    return (TRANSIT_SECTOR,_soluce)


class _path_solver(unittest.TestCase):

    def _previous_0_sector(self):
        print()
        print('x {} y {} s {} '.format(3,9,sector(3,9)))

    def _previous_1_select(self):
        print()
        r, c, SELECT_MAP = select(5,TREASURE_MAP)
        for line in SELECT_MAP:
            print(line)

    def _previous_2_hamilton(self):
        print()
        global TURN
        r, c, SELECT_MAP = select(5,TREASURE_MAP)
        puzzle = Hamilton(SELECT_MAP)
        _soluce = None
        for solution in puzzle.solve():
            _soluce = solution
            break

        for i in range(len(_soluce)):
            o, r, c = puzzle.read_turn(solution,i)
            l_road = list(SELECT_MAP[r])
            l_road[c] = o
            SELECT_MAP[r] = ''.join(l_road)
            write_termios(SELECT_MAP, len(SELECT_MAP), TURN)
            TURN += 1

    def _previous_3_prepare(self):
        print()
        TRANSIT_GLOBAL = []
        TRANSIT_GLOBAL.append(list('...'))
        TRANSIT_GLOBAL.append(list('...'))
        TRANSIT_GLOBAL.append(list('...'))

        # TODO: Incomplete
        TRANSIT_SECTOR = prepare(TREASURE_MAP)
        if len(TRANSIT_SECTOR['1S']) == 0 and len(TRANSIT_SECTOR['1W']) == 0:
            TRANSIT_GLOBAL[0][0] = 'x'

        if len(TRANSIT_SECTOR['3S']) == 0 and len(TRANSIT_SECTOR['3E']) == 0:
            TRANSIT_GLOBAL[0][2] = 'x'

        if len(TRANSIT_SECTOR['7N']) == 0 and len(TRANSIT_SECTOR['7W']) == 0:
            TRANSIT_GLOBAL[2][0] = 'x'

        if len(TRANSIT_SECTOR['9N']) == 0 and len(TRANSIT_SECTOR['9E']) == 0:
            TRANSIT_GLOBAL[2][2] = 'x'

        for g in TRANSIT_GLOBAL:
            g = ''.join(g)

        puzzle = Hamilton(TRANSIT_GLOBAL)
        _soluce = None
        nb = 1
        while _soluce is None :
            if nb == 0 :
                puzzle.change_start()
            nb = 0
            for solution in puzzle.solve():
                nb += 1
                _soluce = solution
                break

        TURN = 1
        for i in range(len(_soluce)):
            o, r, c = puzzle.read_turn(_soluce,i)
            l_road = list(TRANSIT_GLOBAL[r])
            l_road[c] = o
            TRANSIT_GLOBAL[r] = ''.join(l_road)
            write_termios(TRANSIT_GLOBAL, len(TRANSIT_GLOBAL), TURN)
            TURN += 1

    def _previous_4_easy_big_map(self):
        # Big map 3 x 3
        TEST = []
        TEST.append('...')
        TEST.append('...')
        TEST.append('...')

        global TURN
        TURN = 1
        _soluce = None
        puzzle = Hamilton(TEST)
        for solution in puzzle.solve():
            _soluce = solution
            break

        for i in range(len(_soluce)):
            o, r, c = puzzle.read_turn(_soluce,i)
            l_road = list(TEST[r])
            l_road[c] = o
            TEST[r] = ''.join(l_road)
            write_termios(TEST, len(TEST), TURN)
            TURN += 1

    def _previous_5_medium_big_map(self):
        print()
        global PUZZLE_GLOBAL
        TRANSIT_SECTOR,_soluce = treasure_transit(TREASURE_MAP,TRANSIT_GLOBAL)

        TURN = 1
        for i in range(len(_soluce)):
            o, r, c = _soluce[i]
            l_road = list(TRANSIT_GLOBAL[r])
            l_road[c] = o
            TRANSIT_GLOBAL[r] = ''.join(l_road)
            write_termios(TRANSIT_GLOBAL, len(TRANSIT_GLOBAL), TURN)
            TURN += 1

        o, r, c = _soluce[0]
        s1 = sectorb(r,c)

        start_r1, start_c1, finish_r1, finish_c1 = treasure_next(TRANSIT_SET,TRANSIT_SECTOR,s1)

        # Find a path
        TURN = 1
        r, c, SELECT_MAP = select(s1,TREASURE_MAP)

        l_road = list(SELECT_MAP[start_r1])
        l_road[start_c1] = 'S'
        SELECT_MAP[start_r1] = ''.join(l_road)

        l_road = list(SELECT_MAP[finish_r1])
        l_road[finish_c1] = 'F'
        SELECT_MAP[finish_r1] = ''.join(l_road)

        for line in SELECT_MAP:
            print(line)

        puzzle = SimplePath(SELECT_MAP)
        _soluce = None
        for solution in puzzle.solve():
            _soluce = solution
            break

        for i in range(len(_soluce)):
            o, r, c = puzzle.read_turn(solution,i)
            l_road = list(SELECT_MAP[r])
            l_road[c] = 'S'
            SELECT_MAP[r] = ''.join(l_road)
            write_termios(SELECT_MAP, len(SELECT_MAP), TURN)
            TURN += 1

    def _previous_6_hard_big_map(self):
        print()
        global PUZZLE_GLOBAL
        global TREASURE_MAP
        TRANSIT_SECTOR,TREASURE_SOLUCE = treasure_transit(TREASURE_MAP,TRANSIT_GLOBAL)

        TURN = 1
        for i in range(len(TREASURE_SOLUCE)):
            o, r, c = TREASURE_SOLUCE[i]
            l_road = list(TRANSIT_GLOBAL[r])
            l_road[c] = o
            TRANSIT_GLOBAL[r] = ''.join(l_road)
            #print("o {} r {} c {} ".format(o,r,c))
            write_termios(TRANSIT_GLOBAL, len(TRANSIT_GLOBAL), TURN)
            TURN += 1

        o, r, c = TREASURE_SOLUCE[0]
        s1 = sectorb(r,c)

        start_r1, start_c1, finish_r1, finish_c1 = treasure_next(TRANSIT_SET,TRANSIT_SECTOR,s1)

        # Find a path
        TURN = 1
        r, c, SELECT_MAP = select(s1,TREASURE_MAP)

        l_road = list(SELECT_MAP[start_r1])
        l_road[start_c1] = 'S'
        SELECT_MAP[start_r1] = ''.join(l_road)

        l_road = list(SELECT_MAP[finish_r1])
        l_road[finish_c1] = 'F'
        SELECT_MAP[finish_r1] = ''.join(l_road)

        for line in SELECT_MAP:
            print(line)

        puzzle = SimplePath(SELECT_MAP)
        _soluce = None
        for solution in puzzle.solve():
            _soluce = solution
            break

        for i in range(len(_soluce)):
            o, r, c = puzzle.read_turn(solution,i)
            l_road = list(SELECT_MAP[r])
            l_road[c] = o
            SELECT_MAP[r] = ''.join(l_road)
            write_termios(SELECT_MAP, len(SELECT_MAP), TURN)
            TURN += 1

        print("Near end for planning")
        TREASURE_MAP = treasure_update(TREASURE_MAP,SELECT_MAP,s1)
        write_termios(TREASURE_MAP, len(TREASURE_MAP), 0)

        o, r, c = TREASURE_SOLUCE[1]
        print("Before new sector {} {}".format(r,c))
        s1 = sectorb(r,c)
        print("New sector {}".format(s1))

        start_r1, start_c1, finish_r1, finish_c1 = treasure_next(TRANSIT_SET,TRANSIT_SECTOR,s1)

        # Find a path
        TURN = 1
        r, c, SELECT_MAP = select(s1,TREASURE_MAP)

        l_road = list(SELECT_MAP[start_r1])
        l_road[start_c1 % 5] = 'S'
        SELECT_MAP[start_r1 % 5] = ''.join(l_road)

        l_road = list(SELECT_MAP[finish_r1])
        l_road[finish_c1 % 5] = 'F'
        SELECT_MAP[finish_r1 % 5] = ''.join(l_road)

        puzzle = SimplePath(SELECT_MAP)
        _soluce = None
        for solution in puzzle.solve():
            _soluce = solution
            break

        for i in range(len(_soluce)):
            o, r, c = puzzle.read_turn(solution,i)
            l_road = list(SELECT_MAP[r])
            l_road[c] = o
            SELECT_MAP[r] = ''.join(l_road)
            write_termios(SELECT_MAP, len(SELECT_MAP), TURN)
            TURN += 1

        print("Near end for planning {}".format(s1))
        TREASURE_MAP = treasure_update(TREASURE_MAP,SELECT_MAP,s1)
        write_termios(TREASURE_MAP, len(TREASURE_MAP), 0)

    def test_previous_7_hard_big_map(self):
        print()
        global PUZZLE_GLOBAL
        global TREASURE_MAP
        TRANSIT_SECTOR,TREASURE_SOLUCE = treasure_transit(TREASURE_MAP,TRANSIT_GLOBAL)

        TURN = 1
        for i in range(len(TREASURE_SOLUCE)):
            o, r, c = TREASURE_SOLUCE[i]
            l_road = list(TRANSIT_GLOBAL[r])
            l_road[c] = o
            TRANSIT_GLOBAL[r] = ''.join(l_road)
            #print("o {} r {} c {} ".format(o,r,c))
            write_termios(TRANSIT_GLOBAL, len(TRANSIT_GLOBAL), TURN)
            TURN += 1

        o, r, c = TREASURE_SOLUCE[0]
        s1 = sectorb(r,c)

        start_r1, start_c1, finish_r1, finish_c1 = treasure_next(TRANSIT_SET,TRANSIT_SECTOR,s1)

        # Find a path
        TURN = 1
        r, c, SELECT_MAP = select(s1,TREASURE_MAP)

        l_road = list(SELECT_MAP[start_r1])
        l_road[start_c1] = 'S'
        SELECT_MAP[start_r1] = ''.join(l_road)

        l_road = list(SELECT_MAP[finish_r1])
        l_road[finish_c1] = 'F'
        SELECT_MAP[finish_r1] = ''.join(l_road)

        for line in SELECT_MAP:
            print(line)

        puzzle = SimplePath(SELECT_MAP)
        _soluce = None
        for solution in puzzle.solve():
            _soluce = solution
            break

        for i in range(len(_soluce)):
            o, r, c = puzzle.read_turn(solution,i)
            l_road = list(SELECT_MAP[r])
            l_road[c] = o
            SELECT_MAP[r] = ''.join(l_road)
            write_termios(SELECT_MAP, len(SELECT_MAP), TURN)
            TURN += 1

        print("Near end for planning")
        TREASURE_MAP = treasure_update(TREASURE_MAP,SELECT_MAP,s1)
        write_termios(TREASURE_MAP, len(TREASURE_MAP), 0)

        o, r, c = TREASURE_SOLUCE[1]
        print("Before new sector {} {}".format(r,c))
        s1 = sectorb(r,c)
        print("New sector {}".format(s1))

        start_r1, start_c1, finish_r1, finish_c1 = treasure_next(TRANSIT_SET,TRANSIT_SECTOR,s1)

        # Find a path
        TURN = 1
        r, c, SELECT_MAP = select(s1,TREASURE_MAP)

        l_road = list(SELECT_MAP[start_r1])
        l_road[start_c1 % 5] = 'S'
        SELECT_MAP[start_r1 % 5] = ''.join(l_road)

        l_road = list(SELECT_MAP[finish_r1])
        l_road[finish_c1 % 5] = 'F'
        SELECT_MAP[finish_r1 % 5] = ''.join(l_road)

        puzzle = SimplePath(SELECT_MAP)
        _soluce = None
        for solution in puzzle.solve():
            _soluce = solution
            break

        for i in range(len(_soluce)):
            o, r, c = puzzle.read_turn(solution,i)
            l_road = list(SELECT_MAP[r])
            l_road[c] = o
            SELECT_MAP[r] = ''.join(l_road)
            write_termios(SELECT_MAP, len(SELECT_MAP), TURN)
            TURN += 1

        print("Near end for planning {}".format(s1))
        TREASURE_MAP = treasure_update(TREASURE_MAP,SELECT_MAP,s1)
        write_termios(TREASURE_MAP, len(TREASURE_MAP), 0)


if __name__ == '__main__':
    unittest.main()
