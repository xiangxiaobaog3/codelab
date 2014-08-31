# encoding: utf-8


class Singleton(object):
    """单例类

    >>> a = Singleton()
    >>> a.a = 'a'
    >>> b = Singleton()
    >>> b.a == a.a
    True
    >>> id(b) == id(a) == id(Singleton.instance())
    True
    """

    def __new__(self):
        if not hasattr(self, '_instance'):
            self._instance = self
        return  self._instance

    @classmethod
    def instance(cls):
        return cls()


class BaseGameEntity(object):
    """游戏实体基类"""
    id = None
    next_valid_id = None

    def set_id(self, id_):
        """设置新的ID"""
        self.id = id_

    def update(self):
        raise NotImplemented("update method not implemented yet!")


class Miner(BaseGameEntity):
    """矿工实体类"""

    def __init__(self, id_):
        self.set_id(id_)
        self.state_machine = StateMachine(self)
        self.state_machine.set_current_state(GoHoneAndSleepTilRested.instance())
        self.state_machine.set_global_state(MinerGlobalState.instance())
        self.location = None
        self.gold_carried = 0
        self.money_in_bank = 0
        self.thirst = 0
        self.fatigue = 0

    def update(self):
        """更新矿工的状态"""
        self.thirst += 1
        self.state_machine.update()

    def get_fsm(self):
        return self.state_machine

    def depoist(self):
        """存款"""
        self.money_in_bank += self.gold_carried
        self.gold_carried = 0

    def is_thirsty(self):
        return self.thirst >= 3

    def drink_beer(self):
        self.gold_carried -= 3
        self.thirst = 0

    def increase_fatigue(self):
        self.fatigue += 1

    def add_to_gold_carried(self, n):
        self.gold_carried += n

    def change_location(self, location):
        print("miner %s enter " % (self, location))
        self.location = location


class State(object):
    """状态机"""

    location = None

    def enter(self, obj):
        if self.location and obj.location != self.location:
            obj.change_location(self.location)

    def execute(self, obj):
        raise NotImplemented("Method not implemented yet!")

    def exit(self, obj):
        print("%s leaving %s" % (obj, self.location))
        obj.location = None


class StateMachine(BaseGameEntity):
    """状态机，用于管理管理状态"""

    def __init__(self, entity):
        self.owner = entity
        self.current_state = None
        self.previous_state = None
        self.global_state = None

    def set_current_state(self, state):
        self.current_state = state

    def set_global_state(self, state):
        self.global_state = state

    def set_previous_state(self, state):
        self.previous_state = state

    def update(self):
        [i.execute(self.owner)
         for i in [self.global_state, self.current_state] if i]

    def change_state(self, new_state):
        assert(self.current_state and new_state)
        self.previous_state = self.current_state
        self.current_state.exit(self.owner)
        self.current_state = new_state
        self.current_state.enter(self.owner)

    def revert_to_previous_state(self):
        self.change_state(self.previous_state)

    def is_in_state(self, state):
        return self.current_state == state


# Implemented states

class MinerGlobalState(Singleton, State):
    """矿工全局状态"""

    def execute(self, miner):
        print("this is global miner state")


class GoHoneAndSleepTilRested(Singleton, State):
    """回家休息"""

    location = "Home"

    def execute(self, miner):
        miner.thirst = 0
        miner.fatigue = 0


class EnterMineAndDigForNugget(Singleton, State):
    """进入矿区并挖掘金子状态"""

    location = "GoldMine"

    def execute(self, miner):
        miner.add_to_gold_carried(1)
        miner.increase_fatigue()

        print("miner %s pickin up a nugget" % miner)

        if miner.pockets_full():
            miner.change_state(VisitBankAndDepositGold.instance())
        if miner.is_thirsty():
            miner.change_state(QuenchThirst.instance())

    def exit(self, miner):
        print("Ah'm leavin the gold mine with mah pockets full sweet gold")
        miner.location = None


class VisitBankAndDepositGold(Singleton, State):
    location = 'Bank'

    def execute(self, miner):
        miner.depoist()


class QuenchThirst(Singleton, State):
    location = 'Bar'

    def enter(self):
        super(QuenchThirst, self).enter()
        Dispatch.instance().dispatch(SEND_MSG_IMMEDIATELY,
                                     self.id,
                                     ent_Elsa, # 接收者ID
                                     msg_HI_HONEY_IM_HOME, # 消息
                                     NO_ADDITIONAL_INFO, # 无附加信息
                                    )

    def execute(self, miner):
        if miner.gold_carried >= 1:
            miner.drink_beer()
            if not miner.is_thirsty():
                miner.change_state(EnterMineAndDigForNugget)
        else:
            miner.change_state() # GoHomeAndRest

def test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()
