# encoding: utf-8

from random import randrange
from entity import Dispatcher


class BaseState(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BaseState, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def update(self, miner):
        # raise NotImplemented("to be implemented!")
        pass

    def enter(self, miner):
        # raise NotImplemented("to be implemented!")
        pass

    def exit(self, miner):
        # raise NotImplemented("to be implemented!")
        pass

    def on_message(self, sender, entity, msg):
        return False


class EnterMineAndDigForNugget(BaseState):
    def enter(self, miner):
        print('{0} enter state EnterMineAndDigForNugget'.format(miner))
        if miner.location != 'goldmine':
            print('{0} walking to the gold mine'.format(miner))
            miner.change_location('goldmine')

    def exit(self, miner):
        print('{0} exit state EnterMineAndDigForNugget'.format(miner))

    def update(self, miner):
        print('dig for gold')
        miner.increase_fatigue()
        miner.add_gold_carried(1)
        if miner.is_pocket_full():
            miner.fsm.change_state(VisitBankAndDepositGold())
        if miner.is_thirsty():
            miner.fsm.change_state(QuenchThirst())


class VisitBankAndDepositGold(BaseState):
    def enter(self, miner):
        print('{0} enter state VisitBankAndDepositGold'.format(miner))

    def exit(self, miner):
        print('{0} exit state VisitBankAndDepositGold'.format(miner))

    def update(self, miner):
        pass


class GoHomeAndSleepTilRested(BaseState):
    def enter(self, miner):
        Dispatcher().dispatch(miner.id, 2, 'HOME')
        print('{0} enter state GoHomeAndSleepTilRested'.format(miner))

    def exit(self, miner):
        print('{0} exit state GoHomeAndSleepTilRested'.format(miner))

    def update(self, miner):
        if miner.fatigue == 0:
            miner.fsm.change_state(EnterMineAndDigForNugget())
        else:
            miner.fatigue -= 1

    def on_message(self, sender, entity, msg):
        if msg == 'EatStew':
            entity.fsm.change_state(EatStew())


class QuenchThirst(BaseState):
    def enter(self, miner):
        print('{0} enter state QuenchThirst'.format(miner))

    def exit(self, miner):
        print('{0} exit state QuenchThirst'.format(miner))

    def update(self, miner):
        miner.thirsty = 0
        miner.fsm.change_state(GoHomeAndSleepTilRested())


class CookStew(BaseState):
    def enter(self, entity):
        print('{0} enter state CookStew'.format(entity))

    def exit(self, entity):
        print('{0} exit state CookStew'.format(entity))

    def update(self, entity):
        print('cooking')
        if randrange(1, 10) >= 7:
            entity.fsm.change_state(VisitBathroom())
            Dispatcher().dispatch(entity.id, 1, 'EatStew')
            entity.fsm.set_global_state(None)


class DoHouseWork(BaseState):
    def enter(self, entity):
        print('{0} enter state DoHouseWork'.format(entity))

    def exit(self, entity):
        print('{0} exit state DoHouseWork'.format(entity))

    def update(self, entity):
        print('do house work')
        if randrange(1, 10) >= 7:
            entity.fsm.revert_to_previous_state()


class VisitBathroom(BaseState):
    def enter(self, entity):
        print('{0} enter state VisitBathroom'.format(entity))

    def exit(self, entity):
        print('{0} exit state VisitBathroom'.format(entity))

    def update(self, entity):
        print('visit bathroom')
        if randrange(1, 10) >= 8:
            entity.fsm.revert_to_previous_state()

class EatStew(BaseState):

    def update(self, entity):
        print('eat Stew')


class WifeGlobalState(BaseState):

    def on_message(self, sender, entity, msg):
        if msg == 'HOME':
            entity.fsm.change_state(CookStew())
            return True



