# encoding: utf-8

class State(object):

    """Finite State Machine"""

    def __init__(self):
        """构造函数"""

    def enter(self, obj):
        """进入状态触发的函数
        :returns: @todo

        """

    def exit(self, obj):
        """退出状态触发的函数"""

    def execute(self, obj):
        """状态触发执行的函数"""


class Miner(object):

    def change_state(self, new_state):
        self.current_state.exit(self)
        self.current_state = new_state
        self.current_state.enter(self)

    def update(self, obj):
        obj.thirst += 1
        self.current_state.execute(self)


class QuenchThist(State):

    """口渴状态"""

    def enter(self, obj):
        """喝水"""

    def execute(self, obj):
        obj.thirst -= 1

    def exit(self, obj):
        """状态对象不再口渴"""


class EnterMineAndDigForNugget(State):

    """Docstring for EnterMineAndDigForNugget. """

    def enter(self, miner):
        # 改变挖矿者的位置
        if miner.location != 'goldmine':
            miner.change_location('goldmine')

    def execute(self, miner):
        # 矿工挖掘金子直到拿到的金子达到最大
        # 如果矿工感到口渴了，他会停止工作并且改变状态去酒吧喝一杯威士忌
        miner.add_to_gold_carried(1)
        # mining is a hard work
        miner.increase_fatigue()
        print(miner, "up a nugget")

        if miner.is_pockets_full():
            miner.change_state(VisitBankAndDepositGold.instance())
        if miner.is_thirst():
            miner.change_state(QuenchThirst.instance())


