function equalsAll(value, ...)
    for _, v in ipairs({...}) do
        if value ~= v then return false end
    end
    return true
end

function equalsAny(value, ...)
    for _, v in ipairs({...}) do
        if value == v then return true end
    end
    return false
end
