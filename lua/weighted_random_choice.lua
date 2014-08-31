--[[
--
-- The `choices' table contains pairs of
-- associated (choice, weight) values:
--
--  { Lua = 20, Python = 10, Perl = 5, PHP = 2 }
--
--]]
--
--
function weighted_total(choices)
   local total = 0
	 for choice, weight in pairs(choices) do
		 total = total + weight
	 end
	 return total
end

function weighted_random_choice(choices)
	local threshold = math.random(0, weighted_total(choices))
	local last_choice

	for choice, weight in pairs(choices) do
		threshold = threshold - weight
		if threshold <= 0 then return choice end
		last_choice = choice
	end

	return last_choice

end

local choices = { Lua = 20, Python = 10, Perl = 5, PHP = 2 }
local results = {}
local iterations = 1000

for i = 1, iterations do
	local choice = weighted_random_choice(choices)
	results[choice] = (results[choice] or 0) + 1
end

local expected_total = weighted_total(choices)
local actual_total = 0

for choice, weight in pairs(results) do
	actual_total = actual_total + weight
end

local function printf(s, ...)
	io.write(s:format(...), '\n')
end

for _, choice in ipairs { 'Lua', 'Python', 'Perl', 'PHP' } do
	local expected = choices[choice] / (expected_total / 100)
	local actual = results[choice] / (actual_total / 100)
	printf('% 8s: expected %2i%%, result is %2i%%',
	choice, expected, actual)
end
