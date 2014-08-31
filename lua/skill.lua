function Class(base)
	local cls_mt = {__index=base}
	local cls = {}
	setmetatable(cls, cls_mt)
	cls.new = function (...)
		local obj = {}
		local obj_mt = {__index=cls}
		setmetatable(obj, obj_mt)
		obj:init(...)
		return obj
	end
	return cls
end

require "unit"

Skill = Class(nil)

function moveTo(A, B)
	-- dummy function
end

function reduceHp(A, val)
	-- 减血
	local hp = math.max(0, A.getHp() - val)
	A.setAttr('hp', hp)
end

function addHp(A, val)
	-- 加血
	local hp = math.min(A.getHp() + val, A.getMaxHp())
	A.setAttr('hp', hp)
end

function setStatus(A, status)
	-- 设置目标状态
	local hp = math.min(A.getHp() + val, A.getMaxHp())
	A.setAttr('hp', hp)
end

function Skill:init(caster)
	self.name_ = "我是个一个傻技能"
	self.desc_ = "dummy skill for testing"
	self.caster = caster -- 技能施放者
	self.targets_ = {}
	self.actions_ = {
		prepare={
			[1]=function (A, B) return moveTo(A, B) end,
		},
		apply={
			[1]=function (A, B) reduceHp(B, A.atk) end,
		},
		finish={
		},
	}
end

function Skill:applyActions()
	-- apply [prepare, apply, finish] actions
	local actions = {'prepare', 'apply', 'finish'}
	for _, func in ipairs(self.actions_) do
		for _, target in ipairs(self.getTargets()) do
			func(self.caster, target)
		end
	end
end

function Skill:setTargets(targets)
	-- apply [prepare, apply, finish] actions
	self.targets_ = targets
end

function Skill:getType()
	-- 技能类型
end

function Skill:canCauseStrikeBack()
	-- 判定技能是否能引发目标反击
	return false
end

function Skill:getTargets()
   -- 技能目标
end

function Skill:isActive(dices)
	-- 判定技能施放条件是否满足
	-- @params: dices: 骰子组对象
	-- @return true|false
	return true
end

function Skill:setTargetAttr(target, attr, value)
	-- 修改目标属性
end

function Skill:setTargetStatus(target, status)
	-- 修改目标状态
end

function Skill:setTargetStatus(target, status)
	-- 修改目标状态
end

u1 = Unit.new()
u2 = Unit.new()

skill = Skill.new(u1)
print(skill:canCauseStrikeBack())
print(skill:applyActions())
