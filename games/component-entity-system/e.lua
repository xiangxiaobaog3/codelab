Velocity = setmetatable({}, {
    __call=function(self, ...)
        self:init(...)
        return self
    end,
    __index=Velocity,
    __name='Velocity',
})

function Velocity:init(x, y)
    self.x = x
    self.y = y
end


v = Velocity(10, 10)
print(v.x, v.y)
x = Velocity(100, 10)
print(x.x, x.y)
