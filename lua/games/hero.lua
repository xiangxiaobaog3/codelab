local Hero = {}
Hero.__index = Hero


function Hero.create(id, player, data)
    local data = data and data or {}
    local self =  cloneTable(data)
    self.id = id
    self.rawData = self:getRawData()
    self.player = player
    self.equipment = {}
    return self
end

function getEquipItemState(itemid)
    -- 获取装备某件物品的状态
    -- states: 0 能够装备, 1 不能装备, 2 英雄条件不足
end

function Hero:canEquip(state)
    return state == 0
end

function Hero:equip(itemid)
    local state = self:getEquipItemState(itemid)
    if self:canEquip(state) then
        table.insert(self.equipment, itemid)
        state = 1
        return state
    end
    return state
end

function self:getRawData()
    return Data.heroData[self.id]
end

function Hero:addExp(exp)
    self.exp = math.min(self.exp + exp, self.maxexp)
    if self:canLevelup() then
        self:onLevelup()
    end
end

function Hero:onLevelup()
    self.level = self.level + 1
    self:save()
    self:tellClientWeLevelup()
    self.exp = 0
end

function Hero:save()
    DBproxy.update("player", self.player.rid, "", table2str({}))
end


local HeroManager = {}
HeroManager =
