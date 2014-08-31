local State = {}

function State:new(name, enter, execute, exit)
    return {name=name, enter=enter, execute=execute, exit=exit}
end

return State
