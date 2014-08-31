require 'entity'
require 'struct'

function love.load()
    Circle = struct('mode', 'p', 'r')

    love.graphics.setBackgroundColor(255, 255, 255)
    love.graphics.setColor(0, 0, 0)
    font = love.graphics.newFont('visitor1.ttf', 24)
    love.graphics.setFont(font)
    debug_draw = true

    w = love.graphics.getWidth()
    h = love.graphics.getHeight()

    gFleeRadius = 200 -- flee
    gArrivalRadius = 200 -- arrival
    slowing = false -- flee, arrival
    nAvoidanceObstacles = 50 -- avoidance

    entity = Entity(20, 20, Vector(50, 50), Vector(0, 0), 1, 150, 150,
                    gFleeRadius, gArrivalRadius)

    pursue_evade_entity = Entity(10, 10, Vector(500, 400), Vector(0, 0), 1,
                                 300, 200, gFleeRadius, gArrivalRadius)

    -- Avoidance setup
    -- [
    avoidance_obstacles = {}
    avoidance_walls = {}

    local addObstacles =
        function(in_obstacle)
            for _, obstacle in ipairs(avoidance_obstacles) do
                if Vector.distance(in_obstacle.p, obstacle.p) <=
                   in_obstacle.r + obstacle.r + 50 then
                    return false
                end
            end
            table.insert(avoidance_obstacles, in_obstacle)
            return true
        end

    for i = 1, nAvoidanceObstacles do
        addObstacles(Circle('line', Vector(math.random(100, w-100),
                     math.random(100, h-100)), math.random(25, 40)))
    end
    -- ]

    -- Global behavior settings
    current = {
        behavior = 'avoidance',
        radius = 200,
        target_entity = nil
    }
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

    elseif current.behavior == 'avoidance' then
        entity.behavior = 'avoidance'
        entity:update(dt)
    end
end

function love.draw()
    entity:draw()

    if equalsAny(current.behavior, 'pursue', 'evade') then
        pursue_evade_entity:draw()
    end

    if current.behavior == 'avoidance' then
        for _, obstacle in ipairs(avoidance_obstacles) do
            love.graphics.setColor(0, 0, 0)
            love.graphics.circle(obstacle.mode, obstacle.p.x, obstacle.p.y, obstacle.r)
        end
    end

    -- Draw mouse position
    love.graphics.setColor(0, 0, 0)
    love.graphics.circle('line', x, y, 5, 360)

    -- Print current behavior
    love.graphics.setColor(0, 0, 0)
    love.graphics.print(current.behavior, 10, 10)
end

function love.keypressed(key)
    if key == 'd' then debug_draw = not debug_draw end
    if key == 'q' then love.event.push('quit') end
    if key == '1' then current.behavior = 'seek' end
    if key == '2' then current.behavior = 'flee'; current.radius = gFleeRadius end
    if key == '3' then current.behavior = 'arrival'; current.radius = gArrivalRadius end
    if key == '4' then current.behavior = 'pursue'; current.target_entity = entity end
    if key == '5' then current.behavior = 'evade'; current.target_entity = entity end

    if key == '6' then
        current.behavior = 'avoidance'
    end
end
