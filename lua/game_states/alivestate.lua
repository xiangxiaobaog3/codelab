local State = require "state"

local function enter(entity)
    print("I'm born!")
end

local function execute(entity)
    print("I'm still alive")
    entity.age = entity.age + 1
    if entity.age > 100 then
        entity.stateMachine:changeState("dead state")
    end
end

local function exit(entity)
    print("I died :(")
end

local AliveState = State:new("alive state", enter, execute, exit)
return AliveState
