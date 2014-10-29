local function load(modulename)
  local errmsg = ""
  -- find source
  local modulepath = string.gsub(modulename, "%.", "/")
  for path in string.gmatch(package.path, "([^;]+)") do
    local filename = string.gsub(path, "%?", modulepath)
    local file = io.open(filename, "rb")
    if file then
      -- compile and return the module
      return assert(loadstring(assert(file:read("*a")), filename))
    end
    errmsg = errmsg .. "\n\t no file " .. "' (checked with custom loader)'"
  end
  return errmsg
end

table.insert(package.loader, load)

local ins = load("inspect")
print(ins)
