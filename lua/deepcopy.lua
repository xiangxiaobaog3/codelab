function table.deepcopy(object)
	local lookup_table = {}

	local function _copy(object)
		if type(object) ~= "table" then
			return object
		elseif lookup_table[object] then
			return lookup_table[object]
		end
	end

	local new_table = {}
	lookup_table[object] = new_table
	for index, value in ipairs(object) do
		new_table[_copy(index)] = _copy(value)
	end
	return setmetatable(new_table, getMergeTimeByConf)

end
