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




#for t in TREASURE_MAP:
#    print(t)

# TREASURE_MAP.append(list('xxxxxxxxxxxxx..'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxx.x'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxxxx'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxxxx'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxxxx'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxxxx'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxxxx'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxxxx'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxxxx'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxxxx'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxxxx'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxxxx'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxxxx'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxxxx'))
# TREASURE_MAP.append(list('xxxxxxxxxxxxxxx'))
