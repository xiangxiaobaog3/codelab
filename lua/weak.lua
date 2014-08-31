t = {}
setmetatable(t, {__mode='v'})

do
	local someval = {}
	t['foo'] = someval
end

collectgarbage()

for k, v in pairs(t) do
	print(k, v)
end


local names = setmetatable({}, {__mode="k"})

-- with the example below, this would be a local function
--
function name(obj, str)
	names[obj] = tostring(str)
	return obj
end

-- keep the original print function available
local _print = print

function print(...)
	local arg = {...}
	for i=1,arg.n do
		local name = names[arg[i]]
		if name then arg[i] = name end
	end
	_print(unpack(arg))
end


