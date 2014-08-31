#!/usr/bin/env python
# encoding: utf-8


transitions = ['saw_player', 'reach_player', 'lost_player', 'no_health']
states = ['patrolling', 'chasing', 'attacking', 'dead']

_x = lambda x: dict((k, v) for v, k in enumerate(x))

TRANSITION = _x(transitions)
FSMStateID = _x(states)


class FSMState(object):
    def reason():
        pass

    def act():
        pass


def PatrolState(FSMState):
    def reason(player, npc):
        if npc.position >= player.position:
            npc.set_transition(TRANSITION['saw_player'])

    def act(player, npc):
        print('go go go patroll')
