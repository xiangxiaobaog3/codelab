local W = {}
W.__index = W

function W:new()
    return setmetatable({}, self)
end

function W:fire()
    print(self, "Fire")
end

w = W:new()
w:fire()
