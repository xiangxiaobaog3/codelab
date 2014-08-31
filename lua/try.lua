function try(f, catch_f)
	local status, exception = pcall(f)
	if not status then
		catch_f(exception)
	end
end

try(function()
	-- Try block
	--
	end, function(e)
	-- Exception block.
	-- Use e for conditional catch
	-- Re-raise with error(e)
	end)

_exception_mt = {__tostring=function(e) return 'ERROR: ' .. e.msg end}
somethingBad = {code=121, msg='Ooops'}
setmetatable(somethingBad, _exception_mt)

error(somethingBad)
