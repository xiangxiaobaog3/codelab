math.randomseed(os.time())
math.random()

local inspect = require "inspect"

function shuffled(tab)
   local n, order, res = #tab, {}, {}
	 for i=1,n do
		 order[i] = {rnd=math.random(), idx=i}
	 end
	 table.sort(order, function(a, b)
		 return a.rnd < b.rnd
	 end)
	 for i=1,n do
		 res[i] = tab[order[i].idx]
	 end
	 return res
end

local tab = {1, 2, 3, 4, 'a', 'b', 'c', 'd'}
print('original', inspect(tab))
print('shuffled 1', inspect(shuffled(tab)))
print('shuffled 2', inspect(shuffled(tab)))
print('shuffled 3', inspect(shuffled(tab)))
