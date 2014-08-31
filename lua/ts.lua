s = "2013-10-23"
p = "(%d+)-(%d+)-(%d+)"
year, month, day = s:match(p)
print(year, type(year))
print(os.time({year=year, month=month, day=day}))
