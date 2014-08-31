local State = require "state"

local function enter(entity)
end

local function execute(entity)
end

local function exit(entity)
end


local DeadState = State:new("dead state", enter, execute, exit)
return DeadState
