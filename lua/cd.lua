local cd = 3
local round = 1
local o = {}
o.cd_ = 0
o.active_skill = 11111


-- not use
-- first use
for i=1,10 do
	if o.cd_ % i == 0 then
		o.active_skill = 1111
		o.cd_ = 1
	end
end


