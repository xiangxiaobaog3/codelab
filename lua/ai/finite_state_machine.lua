local mt = {
	__index=function(self, k)
		print"ffffff"
		--return rawget(self, k)
	end,
}

local t = setmetatable({}, mt)
t.a = 'xxxx'
print(t.a)
t.x = 'a'

local t = {
	state='init',
	setState=function(self, state)
		self.state = state
	end,
	getState=function(self)
		return self.state
	end
}

print(t:getState())
print(t:setState('sss'))
print(t:getState())
