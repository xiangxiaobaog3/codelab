-- Observer
--

module("Observer", package.seeall)

function new(...)
	local ins = {events={}}
	setmetatable(ins, {__index=Observer})
	ins:init(...)
	return ins
end

function init(self)
end

function addEvent(self, event, callback)
	if not self.events[event] then
		self.events[event] = {callback}
	else
		table.insert(self.events[event], callback)
	end
end

function rmEvent(self, event)
	self.events[event] = nil
end

function dispatch(self, event, ...)
	local arg = {...}
	local callbacks = self.events[event]
	if callbacks then
		for _, cb in ipairs(callbacks) do
			cb(unpack(arg))
		end
	end
end

o = Observer.new()
o:addEvent('h', function(a) print('h', a) end)
o:addEvent('h', function(a) print('h1', 'a1') end)
o:dispatch('h', 'aaa', '111')
o:rmEvent('h')
o:dispatch('h', 'aaa', '111')
