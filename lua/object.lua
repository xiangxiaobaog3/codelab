-- Class

local Base -- base of the class hierarchy (forward reference)

function Class(Super)
    Super = Super or Base
    local prototype = setmetatable({}, Super)
    prototype.class = prototype
    prototype.super = Super
    prototype.__index = prototype
    return prototype
end

Base = Class()


function Base:new(...)
    local instance = setmetatable({}, self)
    instance:initialize(...)
    return instance
end


function Base:initialize()
end
