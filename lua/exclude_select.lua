d1 = {1, 2, 3, 5}
d2 = {1, 1}
d3 = {1, 1, 3}
function print_tbl(t)
	for _, v in ipairs(t) do
		print(_, v)
	end
end

function asc(t1, t2)
	return t1 < t2
end

function f(t1, t2)
	table.sort(t1, asc)
	table.sort(t2, asc)
	table.copy(t2, t3)

	for _, k in ipairs(t1) do

		for i, j in ipairs(t2) do
			if k == j then
				t1[_] = nil
				t2[i] = nil -- remove element
			end
		end

	end

	if not next(t1) then
		return true
	end
	return false

end
