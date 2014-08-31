function tap(wot)
    print("Initial value " ..  wot)
    local info = {10, 43, 43, 22, 32, 32, 22, 12, 6}
    for gg, v in ipairs(info) do
        print("Iteration loop no. " .. gg)
        local k = coroutine.yield(v)
        print("resume value " .. k)
    end
    return "teacake"
end

source = coroutine.create(tap)

counter = 1

while true do
    counter = counter * 2
    status, retval = coroutine.resume(source, counter)
    print(status, retval)
    if not status then break end
end
