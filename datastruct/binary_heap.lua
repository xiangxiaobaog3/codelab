BinaryHeap = {}

function BinaryHeap.new()
    local self = {list={}}
    setmetatable(self, {__index=BinaryHeap})
    return self
end

function BinaryHeap:insert(v)
end
