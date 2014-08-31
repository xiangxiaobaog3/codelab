-- object

Class = {}

setmetatable(Class, {
    __call=function(self, ...) self:init(...); return self end,
    __index=Class})


function Class:init()
end
