task2gateMap = {
	1=>1,
}
gate2ChapterMap = {
	1 => 1,
}


function Chapter:init(id)
end

function Chapter:getAllGates()
end

function Chapter:getGate(id)
end

function Chapter:getAllTasks()
end

function Chapter:getTask(id)
end

--

function Gate:init(id)
end

function Gate:getAllTasks()
end

function Gate:getTask()
end

--
function Task:init(id)
end

function Task:getParent()
	return self.id
end

function Task:can(player)
end


t = Task(taskID)

if t.can(player) then
	-- if t.isCompleted(player) then
	executeTask(t, player)
end


