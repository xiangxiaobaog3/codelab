string.capitalize = function(s)
	return (s:gsub("^%l", string.upper))
end

Unit = Class(nil)
function Unit:init()
	self.hp_ = 1000
	self.max_hp_ = 1000
	self.defense_ = 50
	self.atk_ = 80
	self.status_ = 'normal'
end

function Unit:setHp(val)
	local val = math.max(0, val)
	self.hp_ = val
end

function Unit:setAtk(val)
   local val = math.max(1, val)
	 self.atk_ = val
end

function Unit:setDefense(val)
   local val = math.max(1, val)
	 self.defense_ = val
end

function Unit:setStatus(status)
   self.status_ = status_
end

function Unit:setAttr(attr, value)
   local func = self[string.capitalize(attr)]
	 if func then
		 func(self, value)
	 end
   -- self[attr] = value
end

function Unit:isDead()
	return self.hp <= 0
end

function Unit:getStatus()
	-- get unit status
	return self.status_
end
