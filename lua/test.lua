string.capitalize = function(s)
	return (s:gsub("^%l", string.upper))
end

print(string.capitalize('www'))
