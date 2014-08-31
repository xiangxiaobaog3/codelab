require "class"

Form = Class()


function Form:init(fields)
    self.errors = {}
    self.is_bound = {}
    self._errors = {}

    self.fields = {}
    for i, field in ipairs(fields) do
        table.insert(self.fields, field)
    end
end


function Form:getErrors()
    if #self._errors ~= 0 then
        self:fullClean()
    end
    return self._errors
end


function Form:fullClean()
    -- cleans all fo self.data and populates self._errors and
    -- self.cleanedData
    self._errors = {}

    self._cleanFields()
    self._cleanForm()
    self._postClean()

    if #self._errors >= 1 then
        self.cleanedData = {}
    end

end


function Form:_cleanFields()
    for name, field in pairs(self.fields) do
        local value = self.data[name]
        local val, err = field.clean(value)
        if #err > 1 then
            self._errors[name] = err
        else
            self.cleanedData[name] = field.clean(value)
        end
    end
end


function Form:_cleanForm()
    local data, err = self.clean()
    if #err >= 1 then
        self._errors['__all__'] = err
    end
end


function Form:_postClean()
end


function Form:clean()
    return self.cleanedData, {}
end


function Form:is_valid()
    return self.is_bound and not self:hasErrors()
end


function Form:hasErrors()
    return #self.errors ~= 0
end
