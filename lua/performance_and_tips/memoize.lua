function tmemoize(func, c)
    local c = c or {}
    return setmetatable(c, {
        __index=function(self, k)
            local v = func(k)
            self[k] = v
            return v
        end
    })
end

function test(a)
    print(a)
end

local c = {}
local mf = tmemoize(test, c)
print(mf['a'])
print(c.a)
