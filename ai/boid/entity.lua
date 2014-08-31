require "vector"
require "utils"

local lg = love.graphics

Entity = {}
Entity.__index = Entity

function drawObstacles()
end

local function drawEntity(entity, borderColor, fillColor)
    lg.push()
    lg.translate(entity.position.x, entity.position.y)
    lg.rotate(entity.velocity:angle())
    lg.translate(-entity.position.x, -entity.position.y)
    lg.setLineWidth(1.5)
    lg.setColor(unpack(borderColor))
    cpx = entity.position.x - entity.width/2
    cpy = entity.position.y - entity.height/2
    lg.rectangle('line', cpx, cpy, entity.width, entity.height) -- draw a border line
    lg.setColor(unpack(fillColor))
    lg.rectangle('fill', cpx, cpy, entity.width, entity.height)
    lg.pop()
end

local function drawEntityVector(entity, vector_name, color)
    lg.setColor(unpack(color))
    local vx = entity.position.x + entity[vector_name].x
    local vy = entity.position.y + entity[vector_name].y
    lg.line(entity.position.x, entity.position.y, vx, vy)
    love.graphics.setColor(0, 0, 0)
end

local function drawSlowingArea(entity)
    lg.setColor(0, 0, 0)
    if entity.slowing then
        lg.setColor(255, 0, 0)
    else
        lg.setColor(0, 0, 0)
    end

    if entity.behavior == 'flee' then
        love.graphics.circle('line',
            entity.seek_flee_arrival_target.x,
            entity.seek_flee_arrival_target.y, entity.flee_radius, 360)

    elseif entity.behavior == 'arrival' then
        love.graphics.circle('line',
            entity.seek_flee_arrival_target.x,
            entity.seek_flee_arrival_target.y, entity.arrival_radius, 360)
    end

end

function Entity.new(w, h, p, v, mass, max_v, max_f, flee_r, arrival_r)
    local self = setmetatable({
        width = w or 32,
        height = h or 32,
        position = p or Vector(0, 0),
        velocity = v or Vector(0, 0),
        mass = mass or 1,
        max_velocity = max_v or 200,
        max_force = max_f or 500,
        flee_radius = flee_r or 50,
        arrival_radius = arrival_r or 80,
        slowing = false,

        --
        acceleration = Vector(0, 0),
        steering = Vector(0, 0), -- 合成力
        steering_force = Vector(0, 0),
        desired_velocity = Vector(0, 0),
        heading = Vector(0, 0),
        perp = Vector(0, 0), -- 垂直 heading 的向量

        -- wander
        wander_angle = 0,
        angle_change = 1,
        circle_distance = 60,


        -- collision avoidance
        max_see_ahead=10,
        max_avoid_force=50,
        ahead = Vector(0, 0),
        --
        behavior = 'seek',
    }, Entity)
    return self
end

function Entity:draw()
    drawEntity(self, {12, 25, 50}, {50, 100, 200})
    if equalsAny(self.behavior, 'seek', 'flee', 'arrival', 'wander') then
        drawSlowingArea(self)
    end
    if equalsAny(self.behavior, 'collisionAvoidance') then
        drawEntityVector(self, 'ahead', {100, 100, 0})
    end
    drawEntityVector(self, 'velocity', {0, 255, 0})
    drawEntityVector(self, 'desired_velocity', {0, 0, 0})
    drawEntityVector(self, 'acceleration', {255, 0, 255})
end

function Entity:updatePosition(dt)
    -- http://gamedevelopment.tutsplus.com/tutorials/understanding-steering-behaviors-seek--gamedev-849
    self.steering_force = self.steering:min(self.max_force)
    self.acceleration = self.steering_force/self.mass
    self.velocity = (self.velocity + self.acceleration * dt):min(self.max_velocity)
    self.position = self.position + self.velocity * dt
end

function Entity:update(dt)
    self:updatePosition(dt)
end


Obstacle = {}
Obstacle.__index = Obstacle

function Obstacle.new(x, y, r)
    return setmetatable({
        center=Vector(x, y),
        radius=r or 20,
    }, Obstacle)
end

function Obstacle:draw()
    lg.circle('fill', self.center.x, self.center.y, 5, 360)
    lg.circle('line', self.center.x, self.center.y, self.radius, 360)
end
