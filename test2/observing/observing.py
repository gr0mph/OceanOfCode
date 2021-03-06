import sys
sys.path.append('../../')

# Global variables
from test2.test_main import TREASURE_MAP

# Class
from OceanOfCode import StalkAndLegal
from OceanOfCode import StalkAndTorpedo
from OceanOfCode import MineAndTrigger
from OceanOfCode import Submarine
from OceanOfCode import Board

from OceanOfCode import TorpedoObserver
from OceanOfCode import TriggerObserver
from OceanOfCode import ObserverQueue

# Global
from OceanOfCode import READ_COMMAND
from OceanOfCode import OBSERVER_TORPEDO
from OceanOfCode import MINE_MAP


# Method
from OceanOfCode import update_order

import unittest

h_command = { ('MOVE')}

class _observing(unittest.TestCase):

    def _usual_case(self):
        # The map
        for t_r in TREASURE_MAP:
            print(t_r)

        # Initialize
        kanban_opp = StalkAndTorpedo(None)
        kanban_opp.set_up(TREASURE_MAP)

        for c1, f1, d1 in update_order('MOVE N|MOVE N'):
            if f1 is not None:
                kanban_opp.update(f1,d1)
                kanban_opp = StalkAndTorpedo(kanban_opp)

        for t_r in MINE_MAP:
            print(t_r)


        kanban_mine = MineAndTrigger(None)
        lambda_n = lambda t1, m1 : '.' if t1 == '.' and m1 == '.' else ' '
        for i1 in range(15):
            MINE_MAP[i1] = [ lambda_n(t1,m1) for t1, m1 in zip(TREASURE_MAP[i1],MINE_MAP[i1]) ]
        kanban_mine.set_up(MINE_MAP)

        for t_r in MINE_MAP:
            print(t_r)

        submarine_mine = Board(None)
        submarine_mine.y = 7
        submarine_mine.x = 7

        # Serious thing
        torpedo_obs = TorpedoObserver(None)

        _observer = ObserverQueue(None)

        # TURN 1

        kanban_opp = _observer.update(submarine_mine,kanban_opp,kanban_mine)

        _observer.iterator(submarine_mine,kanban_opp,kanban_mine)

        # TURN 2

        kanban_opp = _observer.update(submarine_mine,kanban_opp,kanban_mine)
        _observer.reset()

        submarine_mine.torpedo = 0
        _observer.attach(torpedo_obs)

        _observer.iterator(submarine_mine,kanban_opp,kanban_mine)

        print("Observer Torpedo {}".format(torpedo_obs))
        print("Submarine torpedo {}".format(submarine_mine.torpedo))
        print("Length {}".format(len(kanban_opp.inp)))

        kanban_opp = _observer.update(submarine_mine,kanban_opp,kanban_mine)
        _observer.reset()

        submarine_mine.torpedo = 0
        _observer.attach(torpedo_obs)

        _observer.iterator(submarine_mine,kanban_opp,kanban_mine)

        print("Observer Torpedo {}".format(torpedo_obs))
        print("Submarine torpedo {}".format(submarine_mine.torpedo))
        print("Length {}".format(len(kanban_opp.inp)))

    def test_usual_case2(self):
        # The map
        for t_r in TREASURE_MAP:
            print(t_r)

        # Initialize
        kanban_opp = StalkAndTorpedo(None)
        kanban_opp.set_up((1,2,3,4,5,6,7,8,9),TREASURE_MAP)

        for c1, f1, d1 in update_order('MOVE N|MOVE N'):
            if f1 is not None:
                kanban_opp.update(f1,d1)
                kanban_opp = StalkAndTorpedo(kanban_opp)

        kanban_mine = MineAndTrigger(None)
        lambda_n = lambda t1, m1 : '.' if t1 == '.' and m1 == '.' else ' '
        for i1 in range(15):
            MINE_MAP[i1] = [ lambda_n(t1,m1) for t1, m1 in zip(TREASURE_MAP[i1],MINE_MAP[i1]) ]
        kanban_mine.set_up(MINE_MAP)

        print()

        for t_r in MINE_MAP:
            print(t_r)

        submarine_mine = Board(None)
        submarine_mine.y = 7
        submarine_mine.x = 7

        submarine_opp = Board(None)
        submarine_opp.y = 4
        submarine_opp.x = 4

        # Serious thing
        trigger_obs = TriggerObserver(None)

        _observer = ObserverQueue(None)

        # TURN 1

        kanban_opp = _observer.update(submarine_opp,submarine_mine,kanban_opp,kanban_mine)
        _observer.reset()

        kanban_mine.mine(submarine_mine)

        _observer.iterator(submarine_mine,kanban_opp,kanban_mine)

        # TURN 2

        kanban_opp = _observer.update(submarine_opp,submarine_mine,kanban_opp,kanban_mine)
        _observer.reset()

        submarine_mine.x = 12
        submarine_mine.y = 12
        kanban_mine.mine(submarine_mine)

        _observer.attach(trigger_obs)

        _observer.iterator(submarine_mine,kanban_opp,kanban_mine)

        print("Observer Torpedo {}".format(trigger_obs))
        print("Length {}".format(len(kanban_opp.inp)))

        kanban_opp = _observer.update(submarine_opp,submarine_mine,kanban_opp,kanban_mine)
        _observer.reset()

        submarine_mine.x = 11
        submarine_mine.y = 2
        kanban_mine.mine(submarine_mine)

        _observer.attach(trigger_obs)

        _observer.iterator(submarine_mine,kanban_opp,kanban_mine)

        print("Observer Torpedo {}".format(trigger_obs))
        print("Length {}".format(len(kanban_opp.inp)))

        kanban_opp = _observer.update(submarine_opp,submarine_mine,kanban_opp,kanban_mine)
        _observer.reset()

        submarine_mine.x = 3
        submarine_mine.y = 4
        kanban_mine.mine(submarine_mine)

        _observer.attach(trigger_obs)

        _observer.iterator(submarine_mine,kanban_opp,kanban_mine)

        print("Observer Torpedo {}".format(trigger_obs))
        print("Length {}".format(len(kanban_opp.inp)))

        kanban_opp = _observer.update(submarine_opp,submarine_mine,kanban_opp,kanban_mine)
        _observer.reset()

        submarine_mine.x = 7
        submarine_mine.y = 8
        kanban_mine.mine(submarine_mine)

        _observer.attach(trigger_obs)

        _observer.iterator(submarine_mine,kanban_opp,kanban_mine)

        print("Observer Torpedo {}".format(trigger_obs))
        print("Length {}".format(len(kanban_opp.inp)))

if __name__ == '__main__':
    unittest.main()
