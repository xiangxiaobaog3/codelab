function createFSM()
    local patrol = PatrolState(waypoints);
    patrol.addTransition(Transition.SawPlayer, FSMStateID.Chasing)
    patrol.addTransition(Transition.NoHealth, FSMStateID.Dead)

    local dead = DeadState()
    dead.addTransition(Transition.NoHealth, FSMStateID.Dead)

    addFSMState(patrol)
end
