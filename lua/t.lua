require "ansicolors"

print(ansicolors.red .. 'hello from the Red world!' .. ansicolors.reset)
print(ansicolors.blue .. 'go blue!' .. ansicolors.yellow .. ' yellow ' .. ansicolors.clear) -- clear is a synonym for reset
print(ansicolors.yellow .. 'yellow!' .. ansicolors.clear) -- clear is a synonym for reset
-- print(ansicolors.underscore .. colors.yellow .. colors.onblue .. 'crazy stuff' .. ansicolors.reset)
print(ansicolors.red 'no need to worry about resetting here!') -- functional interface
print('xxxx')
