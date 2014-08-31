function cap(str)
	return str:gsub("^%l", string.upper)
end

function Class(base)
	local cls_mt = {__index=base}
	local cls = {}
	setmetatable(cls, cls_mt)
	cls.new = function (...)
		local obj = {}
		local obj_mt = {__index=cls}
		setmetatable(obj, obj_mt)
		obj:init(...)
		return obj
	end
	return cls
end

property_mt = {
	__index=function(t, k)
		-- K is the propery we want access,
		-- if we have get{K}, call it first
		-- else we fallback to {K}_
		local names = {hp=true, atk=true, def=true}
		if names[k] then
			local name = 'get' .. cap(k)
			print(name, '---')
			if rawget(t, name) then
				return rawget(t, name)(t) -- call the method
			else
				name = k .. '_'
				return rawget(t, name)
			end
		else
			return rawget(t, k)
		end
	end
}

base = {}
setmetatable(base, property_mt)

BD = Class(base)

function BD:haha()
	print('HAHA')
end

D = Class(BD)

function D:init()
	self.def_ = 3
end

function D:getDef()
	return self.def_
end

d = D.new()

print(d.def)
d:haha()
