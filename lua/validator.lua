local trans = {
	str=tostring,
	int=tonumber,
	email=function(x) return x end,
}

local validators = {
	str
}

local form = {
	username={
		required=true,
		type='str',
	},
	password={
		required=true,
		type='str',
	},
	time={
		required=true,
		type='int',
	},
	date={
		required=true,
		type='str',
		validator=function(x)
			return x:match("%d+-%d+-%d+")
		end
	},
	x={
		required=false,
		type='int',
	},
	y={
		required=false,
		type='int',
		default=10,
	},
	z={
		required=true,
		type='str',
		validator=function(x, clean)
			if not form[y] == x then
				return nil
			end
			return x
		end
	}
}

function validate(form, data)
	local cleanedData = {}
	local isValid = true
	local errMsg = {}
	for field, v in pairs(form) do
		local _type = form[field].type
		local _val = data[field]
		local _required = form[field].required
		local _validator = form[field].validator or nil
		local _default = form[field].default

		if not _val then
			if _required then
				isValid = false
				table.insert(errMsg, string.format("field %s required", field))
			elseif _default then
				cleanedData[field] = _default
			end
		elseif not trans[_type](_val) then
			isValid = false
			table.insert(errMsg, string.format("field %s type wasn't expected as %s", field, _type))
		else
			local val = trans[_type](_val)
			if _validator then
				val = _validator(val)
				if not val then
					isValid = false
					table.insert(errMsg, string.format("validate field: %s failed", field))
				end
			end
			cleanedData[field] = val
		end
	end

	if not isValid then
		cleanedData = nil
	end

	local ret = {
		data=cleanedData,
		err=errMsg,
	}

	return ret
end


local data = {
	username='xxx',
	password='passw',
	time='121212',
	date='2013-3-10',
	x='1',
	y='12',
	z='xx',
}

print(table.concat(validate(form, data).err))
print(validate(form, data).data.password)
print(validate(form, data).data.x)
print(validate(form, data).data.y)
print(validate(form, data).data.time)
print(validate(form, data).data.x)
print(type(validate(form, data).data.time))
print(validate(form, data).data.date)
