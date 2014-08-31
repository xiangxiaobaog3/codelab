require "class"

Field = Class()


function Field:init()
    print('initialize Field')
end


function Field:clean(value)
    -- local value = self:to_lua(value)
    value = self:validate(value)
    return value, self.messages
end


function Field:validate(value)
    assert("To be implemented")
end


TextField = Field()

function TextField:init()
    print('initialize TextField')
    self.messages = {}
    self.messages.a = 'f'
end

function TextField:validate(value)
    return value
end


BooleanField = Field()

function BooleanField:init()
    print(self.messages.a)
end

tf = TextField()
tf:validate()
