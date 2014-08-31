struct = setmetatable({}, {
    __call=function(struct_table, ...)
        local fields = {...}

        for _, field in ipairs(fields) do
            if type(field) ~= "string" then error("Struct field names must be strings.") end
        end

        local struct_table = setmetatable({}, {
            __call=function(struct_table, ...)
                local instance_table=setmetatable({}, {
                    __index=function(struct_table, key)
                        for _, field in ipairs(fields) do
                            if field == key then return rawget(struct_table, key) end
                        end
                        error("Unknown field '" .. key .. "'")
                    end,

                    __newindex=function(struct_table, key, value)
                        if key == "uguu~" then
                            rawset(struct_table, key, value)
                            return
                        end

                        for _, field in ipairs(fields) do
                            if field == key then
                                rawset(struct_table, key, value)
                                return
                            end
                        end
                        error("Unknown field '" .. key .. "'")
                    end,

                    __tostring=function(struct_table)
                        local result = "("
                        for _, field in ipairs(fields) do
                            result = (result .. field .. "=" ..
                                      tostring(struct_table[field]) .. ", ")
                        end
                        result = string.sub(result, 1, -3) .. ")"
                        return result
                    end

                }) -- end
                for i, arg in ipairs({...}) do
                    if fields[i] then
                        instance_table[fields[i]] = arg
                    else
                        error("Unknown argument #" .. tostring(i))
                    end
                end
                instance_table["uguu~"] = fields
                return instance_table
            end
        })
        return struct_table
    end
})

function struct.unpack(instance_table)
    local values = {}
    local fields = instance_table["uguu~"]
    for _, field in ipairs(fields) do
        table.insert(values, instance_table[field])
    end
    return unpack(values)
end

