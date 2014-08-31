require "entity"
require "movement"

local lg = love.graphics
local sb = SteeringBehavior

WIDTH = lg.getWidth()
HEIGHT = lg.getHeight()

function lineIntersectsCircle(ahead, ahead2, obstacle)
    return (Vector.distance(obstacle.center, ahead) <= obstacle.radius or
            Vector.distance(obstacle.center, ahead2))
end


function findMostThreateningObstacle(entity)
    local mostThreateningObstacle
    for _, v in ipairs(current.obstacles) do
        local collision = lineIntersectsCircle(entity.ahead, entity.ahead2, v)
        if collision then
            mostThreateningObstacle = v
        end
    end
    return mostThreateningObstacle
end

function addObstacles()
    table.insert(current.obstacles, Obstacle.new(255, 255))
    table.insert(current.obstacles, Obstacle.new(215, 215))
    table.insert(current.obstacles, Obstacle.new(115, 255))
end

function love.load()
    world = {}
    entity = Entity.new()
    current = {
        behavior='seek',
        target=Vector(0, 0),
        obstacles={},
    }
    addObstacles()
end

function love.draw()
    lg.setBackgroundColor(255, 255, 255) -- set background white
    lg.print('behavior: ' .. current.behavior, 10, 10)
    entity:draw()
    for _, v in ipairs(current.obstacles) do
        v:draw()
    end
end

function love.update(dt)
    -- update entity
    local x, y = love.mouse.getPosition()
    current.target = Vector(x, y)
    entity.seek_flee_arrival_target = current.target
    entity.behavior = current.behavior
    sb[current.behavior](entity, current.target)
    entity:update(dt)
end

function love.keypressed(key)
    -- change behavior
    if key == 'q' then love.event.push('quit') end
    if key == '1' then current.behavior = 'seek' end
    if key == '2' then current.behavior = 'arrival' end
    if key == '3' then current.behavior = 'flee' end
    if key == '4' then current.behavior = 'wander' end
    if key == '5' then current.behavior = 'collisionAvoidance' end
end
