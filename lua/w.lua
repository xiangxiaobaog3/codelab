pl = require "pl.pretty"
local callbacks = {}
local events = {}

function add(e, callback)
	table.insert(callbacks, callback)
	if not events[e] then
		events[e] = {callback}
	else
		table.insert(events[e], callback)
	end
end

function rmCallback(cb)
end


add('hello', function(a) return a end)
add('hello', function(a) return a end)
add('hello', function(a) return a end)
add('hello', function(a) return a end)
pl.dump(events)
