function myFirstCoroutine(f)
    print("hello, I am a function.", f)
end

local co = coroutine.create(myFirstCoroutine)
print("status before resuming: " .. coroutine.status(co))
coroutine.resume(co)
print("status after resuming: " .. coroutine.status(co))


function compareArgs(name, age)
    print("Hello, " .. name .. "!")
    print("I am " .. (age < 5 and "old" or "younger") .. " than you.")
    local you_response = coroutine.yield("I'll pass this back to my acnestor")
    print("You have responded with: " .. you_response)
end


local co = coroutine.create(compareArgs)
local status, arg = coroutine.resume(co, "Bubba", 17)
print("The coroutine yielded and returned: " .. arg .. " status: " .. tostring(status))
coroutine.resume(co, "Sup.")
