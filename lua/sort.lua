d = {
	{a=1},
	{a=5},
	{a=2},
}

function compare(a, b)
	return a['a'] < b['a']
end

t = table.sort(d, compare)
for _, v in ipairs(d) do
	for k, v in pairs(v) do
		print(k, '-->', v)
	end
end

