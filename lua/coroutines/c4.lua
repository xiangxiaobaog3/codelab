function waitSecondsTest()
    print("Hello, World")
    waitSeconds(2)
    print("I'll print this out 2 seconds after I printed out Hello, World")
end


-- This table is indexed by coroutine and simply contains the time at which the coroutine
-- should be worken up
local WAITING_ON_TIME = {}

local WAITING_ON_SIGNAL = {}

-- Keep track of how long the game has been running.
local CURRENT_TIME = 0


function waitSignal(signalName)
    -- Same check as in waitSeconds; the main thread cannot wait
    local co = coroutine.running()
    assert(co ~= nil, "The main thread cannot wait!")

    if WAITING_ON_SIGNAL[signalName] == nil then
        WAITING_ON_SIGNAL[signalName] = {co}
    else
        table.insert(WAITING_ON_SIGNAL[signalName], co)
    end
    return coroutine.yield()
end


function signal(signalName)
    local threads = WAITING_ON_SIGNAL[signalName]
    if threads == nil then return end
    WAITING_ON_SIGNAL[signalName] = nil

    for _, co in ipairs(threads) do
        coroutine.resume(co)
    end
end

function waitSeconds(seconds)
    -- Grab a reference to the current running coroutine
    local co = coroutine.running()

    -- If co is nil, that means we're on the main process, which isn't a coroutine and can't yield
    assert(co ~= nil, "The main thread cannot wait!")

    -- Store the coroutine and its wakeup time in the WAITING_ON_TIME table
    local wakeupTime = CURRENT_TIME + seconds
    WAITING_ON_TIME[co] = wakeupTime

    -- And suspend the process
    return coroutine.yield(co)
end


function wakeUpWaitingThreads(deltaTime)
    -- This function should be called once per game logic update with the amount of time
    -- that has passed since it was last called
    CURRENT_TIME = CURRENT_TIME + deltaTime

    -- First, grab a list of the threads that need to be woken up. They'll need to be removed
    -- from the WAITING_ON_TIME table which we don't want to try and do while we're iterating
    -- through that table, hence the list.
    local threadsToWake = {}
    for co, wakeupTime in pairs(WAITING_ON_TIME) do
        if wakeupTime < CURRENT_TIME then
            table.insert(threadsToWake, co)
        end
    end
end


function runProcess(func)
    -- This function is just a quick wrapper to start a coroutine
    local co = coroutine.create(func)
    return coroutine.resume(co)
end


-- And a funciton to demo it all
p = runProcess(function()
    print("Hello world. I will now astound you by waiting for 2 seconds.")
    waitSeconds(1)
    print("Haha! I did it!")
end)


runProcess(function()
    print("1: I am the first function. The second function cannot speak until I say it can.")
    waitSeconds(2)
    print("1: In two more seconds, I will allow it to speak.")
    waitSeconds(2)
    signal("ok, you can talk")
    waitSignal("function 2 done talking")
    print("1: First function again. I'm done now too.")
end)


runProcess(function()
    waitSignal("ok, you can talk")
    print("2: Hey, I'm the second function. I like talking.")
    waitSeconds(2)
    print("2: I'd talk all the time, if that jerky first funciton would let me.")
    waitSeconds(2)
    print("2: I guess I'm done now though.")
    signal("funciton 2 done talking")
end)

while true do
    wakeUpWaitingThreads(1)
end
