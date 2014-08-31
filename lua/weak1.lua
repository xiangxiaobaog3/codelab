a = {}
key = {}
print('a', a)
print('key', key)
a[key] = 1
key = {}
a[key] = 2

print('--')
for k, v in ipairs(a) do
	print('a', a, k, v)
end
