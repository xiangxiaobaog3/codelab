local StateMachine = {}

function StateMachine:new(entity, currentState, previousState)
    -- only entity and currentState required
    local stateMachine = {}
    stateMachine.currentState = currentState
    stateMachine.previousState = previousState

    local states = {}

    states[currentState.name] = currentState
    if previousState then
        states[previousState.name] = previousState
    end

    function stateMachine:update()
        self.currentState.execute(entity)
    end

    function stateMachine:addState(newState)
        states[newState.name] = newState
    end

    function stateMachine:changeState(newStateName)
        self.previousState = self.currentState
        self.currentState.exit(entity)
        self.currentState = states[newStateName]
        self.currentState.enter(entity)
    end

    function stateMachine:isInState(stateName)
        return stateName == self.currentState.name
    end

    return stateMachine
end

return StateMachine
