function foo(x)
	print("foo", 1)
	coroutine.yield()
	print("foo", 2)
end

co = coroutine.create(foo) -- create a coroutine with foo as the entry
print(type(co))
print(coroutine.status(co))
print(coroutine.resume(co))
print(coroutine.resume(co))
print(coroutine.status(co))
print(coroutine.resume(co))


function odd(x)
	print("A: odd", x)
	coroutine.yield(x)
	print("B: odd", x)
end

function even(x)
	print("C: even", x)
	if x == 2 then return x end
	print("D: even", x)
end

co = coroutine.create(
	function (x)
		for i=1,x do
			if i==3 then coroutine.yield(-1) end
			if i % 2 == 0 then even(i) else odd(i) end
		end
	end
)

count = 1
while coroutine.status(co) ~= "dead" do
	print('----', count)
	count = count + 1
	errorfree, value = coroutine.resume(co, 5)
	print("E: errorfree, value, status", errorfree, value, coroutine.status(co))
end
