t = {}
setmetatable(t, {__mode='v'})

do
    local someval = {}
    t['foo'] = someval
end

collectgarbage()

for k, v in pairs(t) do
    print(k, v)
end

a = {}
b = {}
setmetatable(a, {__mode='k'})


-- key = {}
-- a[key] = 1
-- key = {}
-- a[key] = 2

-- collectgarbage()

-- for k, v in pairs(a) do
--     print(v)
-- end


function test()
    local k1 = {}
    a[k1] = 1
    local k2 = {}
    a[k2] = 2
end

test()

collectgarbage()
for k, v in pairs(a) do
    print(v)
end
