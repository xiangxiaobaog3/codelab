# encoding: utf-8

import states
from entity import BaseGameEntity
from statemachine import StateMachine


class Miner(BaseGameEntity):

    def __init__(self, name):
        self.name = name
        self.location = None
        self.gold = 0
        self.fatigue = 0
        self.thirsty = 0
        self.fsm = StateMachine(self)
        self.fsm.set_current_state(states.GoHomeAndSleepTilRested())

        self.pocket_limit = 10
        self.thirsty_limit = 10
        self.fatigue_limit = 10

    def __repr__(self):
        return '<Miner {0}>'.format(self.name)

    def change_location(self, location):
        self.location = location

    def is_pocket_full(self):
        return self.gold >= self.pocket_limit

    def add_gold_carried(self, n):
        self.gold += n

    def increase_fatigue(self):
        self.fatigue += 1
        self.thirsty += 1

    def is_thirsty(self):
        return self.thirsty >= self.thirsty_limit


class Wife(BaseGameEntity):
    def __init__(self, name):
        self.name = name
        self.fsm = StateMachine(self)
        self.fsm.set_current_state(states.DoHouseWork())
        self.fsm.set_global_state(states.WifeGlobalState())

    def update(self):
        self.fsm.update()

    def handle_msg(self, sender, msg):
        return self.fsm.handle_message(sender, self, msg)
