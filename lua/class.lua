local MyClass = {} -- the table representing the class, which will double as the metatable for the instance
MyClass.__index = MyClass

function MyClass.new(init)
	local self = setmetatable({}, MyClass)
	self.value = init
	return init
end

function MyClass.set_value(self, newval)
	self.value = newval
end

-- Inheritance
local BaseClass = {}
BaseClass.__index = BaseClass

setmetatable(BaseClass, {
	__call=function(cls, ...)
		local self = setmetatable({}, cls)
		self:_init(...)
		return self
	end
})

function BaseClass:_init(init)
	self.value = init
end

local DerivedClass = {}
DerivedClass.__index = DerivedClass

setmetatable(DerivedClass, {
	__index=BaseClass, -- this is what makes the inheritance work
	__call=function(cls, ...)
		local self = setmetatable({}, cls)
		self:_init(...)
		return self
	end
})

function DerivedClass:_init(init1, init2)
	BaseClass._init(self, init1) -- call the base class constructor
	self.value2 = init2
end

local i = DerivedClass(1, 2)
print(i.value)
print(i.value2)


-- Class creation function
function Class(...)
	-- "cls" is the new class
	local cls, bases = {}, {...}

	cls.toString = function(self)
		return string.format("Class %s", tostring(cls))
	end

	-- copy base class contents into the new class
	for i, base in ipairs(bases) do
		for k, v in pairs(base) do
			cls[k] = v
		end
	end

	-- set the class's __index, and start filling an "is_a" table that contains this class and all of its bases
	-- so you can do an "instance of" check using my_instance.is_a[MyClass]
	cls.__index, cls.is_a = cls, {[cls]=true}

	for i, base in ipairs(bases) do
		for c in pairs(base.is_a) do
			cls.is_a[c] = true
		end
		cls.is_a[base] = true
	end

	-- the class's __call metamethod
	setmetatable(cls, {
		__call=function(c, ...)
			local instance = setmetatable({}, c)
			-- run the init method if it's there
			local init = instance.init
			if init then init(instance, ...) end
			return instance
		end,
	})
	cls.__tostring=cls.toString

	-- return the new class table, that's ready for fill with methods
	return cls
end

A = Class()
function A:init(a)
	self.a = a
end

function A:p()
	print(self.a)
end

function A:toString()
	return "<A>"
end

B = Class(A)
function B:p()
	print 'bbbb'
end

C = Class(A, B)

a = A(10)
print(a)
b = B()
c = C('1121')
print('--')
c:p()

print(a.is_a[A])
print(b.is_a[A])
a:p()
b:p()


--
--
local function MyClass1(init)
	-- the new instance
	local self = {
		-- public fields go in the instance table
		public_field = 0
	}

	-- private fields are implemented using locals
	-- the are faster than table access, and are truely private, so the code
	-- that use your class can't get them

	local private_field = init

	function self.foo()
		return self.public_field + private_field
	end

	function self.bar()
	   private_field = private_field + 1
	end

	return self

end

local i = MyClass1(5)
print(i.foo())
print(i.bar())
i.bar()
print(i.foo())
