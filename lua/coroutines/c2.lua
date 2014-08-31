function foo()
    print("foo", 1)
    coroutine.yield()
    print("foo", 2)
end

co = coroutine.create(foo)
print(type(co))
print(coroutine.status(co))
print(coroutine.resume(co))
print(coroutine.resume(co))
