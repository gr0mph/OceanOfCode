import sys
import math
import copy

game_board = [ None , None ]
_board = None
movement_f = { 'N': None,'S': None,'E': None,'W': None }

WIDTH, HEIGHT, MY_ID = [int(i) for i in input().split()]
OPP_ID = (MY_ID + 1) % 2
TREASURE_MAP = []
for i in range(HEIGHT):
    TREASURE_MAP.append(input())

DEEP = 3

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print("7 7")

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

class StorySubmarin(Board):

    def __init__(self,clone):
        super().__init__(clone)
        if clone is not None:
            self.previous = clone
        else :
            self.previous = None

def update(me,opp):
    me.x, me.y, me.life, opp.life, me.torpedo, me.sonar, me.silence, me.mine = [int(i) for i in input().split()]

_board = Board

while True:
    game_board[MY_ID] = _board(game_board[MY_ID])
    game_board[OPP_ID] = _board(game_board[OPP_ID])
    update(game_board[MY_ID],game_board[OPP_ID])

    sonar_result = input()
    print(sonar_result, file=sys.stderr)
    opponent_orders = input()
    print(opponent_orders, file=sys.stderr)

    print("MOVE N TORPEDO")
