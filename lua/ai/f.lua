require "pl"

function weightedTotal(choices)
	local total = 0
	for choice, weight in pairs(choices) do
		total = total + weight
	end
	return total
end

function weightedRandomChoice(choices)
	local threshold = math.random(0, weightedTotal(choices))
	local last_choice

	for choice, weight in pairs(choices) do
		threshold = threshold - weight
		if threshold <= 0 then return choice end
		last_choice = choice
	end
	return last_choice
end

-- COLORS = {1, 2, 3, 4, 5} -- 所有的颜色集合
COLORS = {'red', 'blue', 'yellow', 'green', 'purple'} -- 所有的颜色集合
math.randomseed(os.time())
math.random()

Slot = {
	new = function(c, limit)
		local limit = limit or 5

		self = {
			limit=limit,
			color=c,
			cards={},
			idx=0,
		}

		self.isFilled = function()
			return #self.cards >= self.limit
		end

		self.append = function(c)
			if not self.isFilled() then
				table.insert(self.cards, c)
			end
		end

		self.isRaceColor = function(c)
			return self.color == c
		end

		-- find out current slot color cards
		self.getRaceCards = function()
			local cs = {}
			for _, c in ipairs(self.cards) do
				if self.isRaceColor(c.color) then
					table.insert(cs, c)
				end
			end
			return cs
		end

		self.getRaceCardsNum = function()
			return #self.getRaceCards()
		end

		return self
	end
}

Slots = {
	new = function()
		local num = 4
		local self = {}
		self.slots = {}

		for i=1,num do
			local c = COLORS[math.random(1, #COLORS)]
			table.insert(self.slots, Slot.new(c))
		end

		self.getSlotIdx = function(slot)
			for _, v in ipairs(self.slots) do
				if v == slot then
					return _
				end
			end
		end

		return self

	end
}


Card = {
	new = function(c)
		local self = {}
		self.color = c

		self.moveTo = function(slot)
			-- slot object
			slot.append(self)
		end

		self.calcSlotWeight = function(slot)
			local weights = 1

			if slot.isRaceColor(self.color) then
				weights = weights + 0.5
				print('--', 'race rate, +0.5', 'weights: ', weights)
			end

			local num = slot.getRaceCardsNum()
			weights = weights + num/5 + 0.2

			print(self.color, 'to slot with weights', slot, weights)
			pretty.dump(slot)
			return weights
		end

		self.calcPath = function(slots)
			local choices = {}

			for _, s in ipairs(slots) do
				choices[_] = self.calcSlotWeight(s)
			end

			return weightedRandomChoice(choices)
		end

		return self
	end
}

Cards = {
	new = function()
		local num = 5
		local self = {cards={}}

		self.popCardFromIdx = function(idx)
			local card = self.cards[idx]
			print(string.format('pop from %s, color is: %s', idx, card.color))
			self.freshCard(idx)
			return card
		end

		self.freshCard = function(idx)
			local color = COLORS[math.random(1, #COLORS)]
			print(string.format('fresh card with color %s at idx: %d', color, idx))
			local c = Card.new(color)
			self.cards[idx] = c
		end

		self.getCardFromIdx = function(idx)
			return self.cards[idx]
		end

		self.getCardsNum = function()
			return #self.cards
		end

		for i=1,num do
			self.freshCard(i)
		end

		return self
	end
}

Battle = {
	new = function(cards, slots)

		local self = {
			cards=cards,
			slots=slots,
		}

		self.getGarbageCards = function()
			local c = {}
			local rs = {}

			for i, v in ipairs(self.slots.slots) do
				rs[v.color] = true
			end

			for i, v in ipairs(self.cards.cards) do
				if not rs[v.color] then
					v.isGarbage = true
					table.insert(c, v)
				end
			end

			return c

		end

		self.moveCardTo = function(cardIdx, slotIdx)
			print(string.format('--> move cardIdx:%d to slotIdx: %d', cardIdx, slotIdx))
			self.slots.slots[slotIdx].append(self.cards.popCardFromIdx(cardIdx))
			--self.cards.freshCard(cardIdx)
		end

		self.round = function()
			local cidx = math.random(1, self.cards.getCardsNum())
			print(string.format('random card idx: %d', cidx))
			local card = self.cards.getCardFromIdx(cidx)
			-- 废牌计算的优先级
			print(card.color, '---')
			local slotIdx = card.calcPath(self.slots.slots)
			self.moveCardTo(cidx, slotIdx)
		end

		return self

	end
}

cards = Cards.new()
slots = Slots.new()
print(#slots.slots)
battle = Battle.new(cards, slots)

for i=1, do
	battle.round()
end

