MemoryCache = {
    cache={},
    get=function(self, k)
        return self.cache[k]
    end,
    set=function(self, k, v)
        self.cache[k] = v
    end,
    delete=function(self, k)
        self.cache[k] = nil
    end,
}
