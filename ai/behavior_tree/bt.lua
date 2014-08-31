local READY = "ready"
local RUNNING = "running"
local FAILED = "failed"

local Action = {}
Action.__index = Action

function Action.create(task)
    return setmetatable({task=task, completed=false}, {__index=Action})
end

function Action:update(ai)
    if self.completed then
        return READY
    end
    self.completed = self.task(ai)
    return RUNNING
end

local Condition = {}
Condition.__index = Condition
setmetatable(Condition, {__call=Condition.create})

function Condition.create(task)
    return setmetatable({task=task}, {__index=Condition})
end

function Condition:update(ai)
    return self.task(ai) and READY or FAILED
end


local Selector = {}
Selector.__index = Selector
function Selector.create(children)
    return setmetatable({children=children}, {__index=Selector})
end

function Selector:update(ai)
    for i, v in ipairs(self.children) do
        local status = v:update(ai)
        if status == RUNNING then
            return RUNNING
        elseif status == READY then
            if i == #self.children then
                self:resetChildren()
                return READY
            end
        end
    end
    return READY
end

function Selector:resetChildren()
    for ii,vv in ipairs(self.children) do
        vv.completed = false
    end
end


local Sequence = {}
Sequence.__index = Sequence
function Sequence.create(children)
    return setmetatable({children=children, completed=false}, {__index=Sequence})
end

function Sequence:update(ai)
    if self.completed then return READY end

    local last = 1

    if self.last and self.last ~= #self.children then
        last = self.last + 1
    end

    for i = last, #self.children do
        local v = self.children[i]:update(creatureAI)
        if v == RUNNING then
            self.last = i
            return RUNNING
        elseif v == FAILED then
            self.last = nil
            self:resetChildren()
            return FAILED
        elseif v == READY then
            if i == #self.children then
                self.last = nil
                self:resetChildren()
                self.completed = true
                return READY
            end
        end
    end
end

function Sequence:resetChildren()
    for ii,vv in ipairs(self.children) do
        vv.completed = false
    end
end


local TRUE = function() return true end
local FALSE = function() return false end

local isThiefNearTreasure = Condition.create(FALSE)
local stillStrongEnoughToCarryTreasure = Condition.create(TRUE)

local makeThiefFlee = Action.create(function() print("making the thief flee") return false end)
local chooseCastle = Action.create(function() print("choosing Castle") return true end)
local flyToCastle = Action.create(function() print("fly to Castle") return true end)
local fightAndEatGuards = Action.create(function() print("fighting and eating guards") return true end)
local takeGold = Action.create(function() print("picking up gold") return true end)
local flyHome = Action.create(function() print("flying home") return true end)
local putTreasureAway = Action.create(function() print("putting treasure away") return true end)
local postPicturesOfTreasureOnFacebook = Action.create(function()
    print("posting pics on facebook")
    return true
end)


local simpleBehaviour = Selector.create{
                            Sequence.create{
                                isThiefNearTreasure,
                                makeThiefFlee,
                            },
                            Sequence.create{
                                chooseCastle,
                                flyToCastle,
                                fightAndEatGuards,
                                packStuffAndGoHome

                            },
                            Sequence.create{
                                postPicturesOfTreasureOnFacebook
                            }
                        }


function exampleLoop()
    for i=1,10 do
        simpleBehaviour:update()
    end
end

exampleLoop()
