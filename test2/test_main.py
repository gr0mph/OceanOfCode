# Unittest
import unittest
import copy

WIDTH, HEIGHT = 15, 15
TREASURE_MAP = []
TREASURE_MAP.append(list('.xx.....xx.....'))
TREASURE_MAP.append(list('........xx.....'))
TREASURE_MAP.append(list('.xx............'))
TREASURE_MAP.append(list('.xx............'))
TREASURE_MAP.append(list('....xx.........'))
TREASURE_MAP.append(list('....xx.....xx..'))
TREASURE_MAP.append(list('...........xx..'))
TREASURE_MAP.append(list('...............'))
TREASURE_MAP.append(list('..........xx...'))
TREASURE_MAP.append(list('..........xx.xx'))
TREASURE_MAP.append(list('..........xx.xx'))
TREASURE_MAP.append(list('.....xx........'))
TREASURE_MAP.append(list('.....xx........'))
TREASURE_MAP.append(list('.....xx........'))
TREASURE_MAP.append(list('.....xx........'))

class Submarine():

    def __init__(self,clone):
        self.out = ''
        self.x, self.y = 0, 0
        if clone is not None :
            self.treasure_map = copy.deepcopy(clone.treasure_map)
        else :
            self.treasure_map = TREASURE_MAP

    @property
    def sector(self):
        return 1 + (self.x // 5) + ( (self.y // 5) * 3 )

    # MOVE DIRECTION {NORTH, EAST, WEST, SOUTH} LOAD {TORPEDO,SONAR,etc}
    def write_move(self,direction,load):
        t = f'MOVE {direction} {load}'
        self.out = t if self.out == '' else f'{self.out} | {t}'

    def write_surface(self):
        self.out = 'SURFACE' if self.out == '' else f'{self.out} | SURFACE'

    def write_torpedo(self,x,y):
        t = f'TORPEDO {x} {y}'
        self.out = t if self.out == '' else f'{self.out} | {t}'

    # TODO -->
    def read_move(self,direction):
        # IF OKAY
        return True if True else None

    # TODO -->
    def read_surface(self,sector):
        # IF submarine in SECTOR
        return True if True else None

    # TODO -->
    def read_torpedo(self,x,y):
        # THE OPPONENT CAN BE STUPID TO LAUNCH A TOPEDO WHERE IT IS
        # CONSIDER THA WILL NOT DO THAT
        # Return OKAY IF X AND Y DIFFER
        return True if True else None

    def order(self):
        print(self.out)

class Board(Submarine):

    def __init__(self,clone):
        super().__init__(clone)
        self.x , self.y , self.life , self.torpedo, self.sonar, self.silence, self.mine = 0, 0, 0, 0, 0, 0, 0
        if clone is not None:
            self.x, self.y, self.life = clone.x, clone.y, clone.life
            self.torpedo, self.sonar = clone.torpedo, clone.sonar
            self.silence, self.mine = clone.silence, clone.mine