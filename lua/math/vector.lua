local Vector = {}

local function add(v1, v2)
    return Vector.init(v1.x + v2.x, v1.y + v2.y)
end

local function sub(v1, v2)
    return Vector.init(v1.x - v2.x, v1.y - v2.y)
end

local Vector_mt = {
    __add=add,
    __sub=sub,
}

setmetatable(Vector, {__call=Vector.init, __index=Vector})

function Vector.init(x, y)
    local self = {
        x=x or 0,
        y=y or 0
    }
    setmetatable(self, Vector_mt)
    return self
end


v1 = Vector.init(1, 3)
v2 = Vector.init(1, 3)

x = v1 + v2
print(x.x)
