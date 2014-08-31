d = {1, 2, 3, 4}

for i, v in ipairs(d) do
	d[i] = nil
	for _, __ in ipairs(d) do
		print(__)
	end
end
print(d)
