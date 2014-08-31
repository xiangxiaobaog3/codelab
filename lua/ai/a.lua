-- colors
local COLORS = {1, 2, 3, 4, 5}

local precise = 1.0 -- 精度
local speed = 1.0 -- 速度

local SLOTS = {
	{},
	{},
	{},
	{}
}


Slots = {
	new = function(idx)
		local self = {}
		self.idx = idx
		return self
	end
}


Card = {
	new = function(i)
		local self = {}
		self.color_ = i

		-- 移动到某个槽
		self.moveTo = function(i)
		end

		return self
	end,
}

-- 计算卡牌移动的路径，并移动
function calcCardMove(slots, card)
end

-- 随机一张卡牌出来
function randomCard(cards)
	return cards[math.random(1, #cards)]
end
