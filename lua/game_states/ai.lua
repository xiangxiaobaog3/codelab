local StateMachine = require "statemachine"
local AliveState = require "alivestate"
local DeadState = require "deadstate"

local AI = {}

function AI:new()
    local ai = {}
    ai.age = 98
    ai.stateMachine = StateMachine:new(ai, AliveState, nil)
    ai.stateMachine:addState(DeadState)
    ai.stateMachine.currentState.enter(ai)

    function ai:update()
        ai.stateMachine:update()
    end

    return ai
end


ai = AI:new()
ai.update()
ai.update()
ai.update()
ai.update()
ai.update()
