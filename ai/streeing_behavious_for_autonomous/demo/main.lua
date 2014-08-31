require 'struct'
require 'entity'

local lg = love.graphics

function love.load()
    Circle = struct('mode', 'p', 'r')
    lg.setBackgroundColor(255, 255, 255)
    lg.setColor(0, 0, 0)
    -- font = lg.newFont('visitor1.ttf', 24)
    -- lg.setFont(font)

    w = lg.getWidth()
    h = lg.getHeight()
    gFleeRadius = 200 -- flee
    gArrivalRadius = 200 -- arrival
    slowing = false -- flee, arrival
    nAvoidanceObstacles = 50 -- avoidance

    entity = Entity(32, 32, Vector(50, 50), Vector(0, 0), 1, 150, 150,
                    gFleeRadius, gArrivalRadius)

    pursue_evade_entity = Entity(16, 16, Vector(500, 400), Vector(0, 0), 1,
                                 300, 200, gFleeRadius, gArrivalRadius)
    avoidance_obstacles = {}
    avoidance_walls = {}

    local addObstacles = function(in_obstacle)
        for _, obstacle in ipairs(avoidance_obstacles) do
            if Vector.distance(in_obstacle.p, obstacle.p) <= in_obstacle.r + obstacle.r + 50 then
                return false
            end
        end
        table.insert(avoidance_obstacles, in_obstacle)
        return true
    end

    for i=1, nAvoidanceObstacles do
        addObstacles(Circle('line',
                            Vector(math.random(100, w-100), math.random(100, h-100)),
                            math.random(25, 40)))
    end

    -- Global behavior settings
    current = {
        behavior = 'seek',
        radius = 200,
        target_entity = nil
    }
end


function love.draw()
    entity:draw()

    if equalsAny(current.behavior, 'pursue', 'evade') then
        pursue_evade_entity:draw()
    end

end


function love.update(dt)
    x, y = love.mouse.getPosition()
    if equalsAny(current.behavior, 'seek', 'flee', 'arrival') then
        entity.behavior = current.behavior
        entity.seek_flee_arrival_target = Vector(x, y)
        entity:update(dt)

    elseif equalsAny(current.behavior, 'pursue', 'evade') then
        entity.behavior = 'seek'
        entity.seek_flee_arrival_target = Vector(x, y)
        entity:update(dt)
        pursue_evade_entity.behavior = current.behavior
        pursue_evade_entity.pursue_evade_entity = current.target_entity
        pursue_evade_entity:update(dt)
    end
end


function love.keypressed(key)
    if key == 'q' then love.event.push('quit') end
    if key == '1' then current.behavior = 'avoidance' end
    if key == '2' then current.behavior = 'arrival' end
    if key == '3' then current.behavior = 'flee' end
    if key == '4' then current.behavior = 'seek' end
    if key == '5' then current.behavior = 'pursue'; current.target_entity=entity end
    if key == '6' then current.behavior = 'evade'; current.target_entity = entity end
end
