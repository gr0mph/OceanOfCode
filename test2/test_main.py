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

TEXT1 = 'MOVE N'
TEXT2 = 'SILENCE'
TEXT3 = 'TORPEDO 0 0|MOVE E'
TEXT4 = 'SURFACE 5'
TEXT5 = 'TORPEDO 11 1|MOVE N'
TEXT6 = 'MOVE N|SURFACE 5|TORPEDO 11 1|SILENCE'

MINE_MAP = []
MINE_MAP.append(list('               '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('  .    .    .  '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('               '))
MINE_MAP.append(list('               '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('  .    .    .  '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('               '))
MINE_MAP.append(list('               '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('  .    .    .  '))
MINE_MAP.append(list(' . .  . .  . . '))
MINE_MAP.append(list('               '))
