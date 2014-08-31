--[[
card type

● High Card：杂牌（不属于下面任何一种）。根据牌从大到小的顺序依次比较。
● Pair：有一对，加3张杂牌组成。先比较对的大小，再从大到小的顺序比较杂牌。
● Two Pairs：有两对，加1帐杂牌。先从大到小比较对的大小，再比较杂牌。
● Three of a Kind：有3张值相同的牌。比较这个值即可。
● Straingt：一条龙。即5张牌连续。比较最大的一张牌即可。
● Flush：清一色。即5张牌花色相同。和杂牌一样比较。
● Full House：3张值相同的牌，加上一对。比较三张相同的值即可。
● Four of a kind：有4张牌相同，即相当于一副“炸弹”。
● Straight flush：同花顺。即5张牌花色相同，并且连续。例如同花色的34567。


各种花色
梅花（club），方块（diamond），红桃（heart）和黑桃（spade）—— 在后面的控制台输入中会以C,D,H,S表示


Straight flush > Four of a kind > Full House > Flush > Straingt > Three of a Kind > Two Pairs > Pair > High Card
--]]
local porker = {1, 3, 4, 6, 4, 6, 8}
local psets = {}
local ordered_porker = {}
local inspect = require "inspect"

for i, v in ipairs(porker) do
	table.insert(ordered_porker, v)
	local k = tostring(v)
	local k = v
	if psets[k] then
		psets[k] = psets[k] + 1
	else
		psets[k] = 1
	end
end

table.sort(ordered_porker)
--print('ordered_porker', inspect(ordered_porker))
print(psets[1])
print(psets[2])
print(psets[3])
print(psets[4])
print(psets[5])
print(psets[6])
print('psets', inspect(psets))
--print(inspect(porker))
