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
