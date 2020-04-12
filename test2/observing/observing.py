import sys
sys.path.append('../../')

# Global variables
from test2.test_main import TREASURE_MAP

# Class
from OceanOfCode import StalkAndLegal
from OceanOfCode import StalkAndTorpedo
from OceanOfCode import Submarine
from OceanOfCode import Board

from OceanOfCode import TorpedoObserver
from OceanOfCode import ObserverQueue

# Global
from OceanOfCode import READ_COMMAND
from OceanOfCode import OBSERVER_TORPEDO

# Method
from OceanOfCode import update_order

import unittest

h_command = { ('MOVE')}

class _observing(unittest.TestCase):

    def test_usual_case(self):
        kanban_opp = StalkAndTorpedo(None)
        kanban_opp.set_up(TREASURE_MAP)

        for c1, f1, d1 in update_order('MOVE N|MOVE N'):
            print("c1 {} f1 {} d1 {}".format(c1,f1,d1))
            if f1 is not None:
                kanban_opp.update(f1,d1)
                kanban_opp = StalkAndTorpedo(kanban_opp)
                print(len(kanban_opp.inp))

        



if __name__ == '__main__':
    unittest.main()
