require 'utils'
require 'vector'

local lg = love.graphics

local function drawFutureEntityPosition(entity, color)
    love.graphics.setColor(unpack(color))
    love.graphics.circle('line',
        entity.pursue_evade_future_entity_position.x,
        entity.pursue_evade_future_entity_position.y, 5, 360)
    love.graphics.line(
        entity.pursue_evade_future_entity_position.x - 10,
        entity.pursue_evade_future_entity_position.y,
        entity.pursue_evade_future_entity_position.x + 10,
        entity.pursue_evade_future_entity_position.y)
    love.graphics.line(
        entity.pursue_evade_future_entity_position.x,
        entity.pursue_evade_future_entity_position.y - 10,
        entity.pursue_evade_future_entity_position.x,
        entity.pursue_evade_future_entity_position.y + 10)
    love.graphics.setColor(0, 0, 0)
end

local function drawSlowingArea(entity)
    lg.setColor(0, 0, 0)
    if entity.slowing then lg.setColor(255, 0, 0)
    else lg.setColor(0, 0, 0) end

    if entity.behavior == 'arrival' then
        lg.circle('line',
                  entity.seek_flee_arrival_target.x,
                  entity.seek_flee_arrival_target.y,
                  entity.arrival_radius, 360)
    elseif entity.behavior == 'flee' then
        love.graphics.circle('line',
            entity.seek_flee_arrival_target.x,
            entity.seek_flee_arrival_target.y, entity.flee_radius, 360)
    end

end

local function drawEntityVector(entity, vector_name, color)
    lg.setColor(unpack(color))
    lg.line(entity.position.x, entity.position.y,
        entity.position.x + entity[vector_name].x, entity.position.y + entity[vector_name].y)
    lg.setColor(0, 0, 0)
end

local function drawEntity(entity, borderColor, fillColor)
    lg.push()
    lg.translate(entity.position.x, entity.position.y)
    lg.rotate(entity.velocity:angle())
    lg.translate(-entity.position.x, -entity.position.y)
    lg.setLineWidth(1.5)
    lg.setColor(unpack(borderColor))
    cx = entity.position.x - entity.width/2
    cy = entity.position.y - entity.height/2
    lg.rectangle('line', cx, cy, entity.width, entity.height)
    lg.setColor(unpack(fillColor))
    lg.rectangle('fill', cx, cy , entity.width, entity.height)
    lg.pop()
end


Entity = {}
Entity.__index = Entity

function Entity.new(w, h, p, v, mass, max_v, max_f, flee_r, arrival_r)
    return setmetatable({
        width = w,
        height = h,
        position = p or Vector(0, 0),
        velocity = v or Vector(0, 0),
        desired_velocity = Vector(0, 0),
        mass = mass,
        acceleration = Vector(0, 0),
        steering = Vector(0, 0),
        steering_force = Vector(0, 0),
        max_velocity = max_v or 0,
        max_force = max_f or 0,
        max_see_ahead = 50,
        behavior = 'seek',
        seek_flee_arrival_target = nil,
        flee_radius = flee_r,
        arrival_radius = arrival_r,
        slowing = false;
        pursue_evade_entity = nil,
        pursue_evade_future_entity_position = nil
    }, Entity)
end

function Entity:draw()
    if equalsAny(self.behavior, 'seek', 'flee', 'arrival') then
        drawEntity(self, {12, 25, 50}, {50, 100, 200})
        drawSlowingArea(self)

    elseif equalsAny(self.behavior, 'pursue', 'evade') then
        drawEntity(self, {50, 12, 25}, {200, 50, 100})
        drawFutureEntityPosition(self, {200, 50, 100})
    end

    lg.setLineWidth(1.2)
    local green = {0, 255, 0}
    local black = {0, 0, 0}
    local purple = {255, 0, 255}
    lg.print('mode: ' .. self.behavior, 10, 0)
    lg.setColor(unpack(green))
    lg.print('velocity: ' .. tostring(self.velocity), 10, 10)
    lg.setColor(unpack(black))
    lg.print('desired_velocity: ' .. tostring(self.desired_velocity), 10, 30)
    lg.setColor(unpack(purple))
    lg.print('acceleration: ' .. tostring(self.acceleration), 10, 50)
    lg.setColor({0, 0, 0})
    lg.print('max force: ' .. tostring(self.max_force), 10, 70)
    lg.print('max velocity: ' .. tostring(self.max_velocity), 10, 90)
    drawEntityVector(self, 'velocity', green)
    drawEntityVector(self, 'desired_velocity', black)
    drawEntityVector(self, 'acceleration', purple)
    lg.setLineWidth(1)
end

function Entity:seek(target)
    self.desired_velocity = (target - self.position):normalized()*self.max_velocity
    self.steering = self.desired_velocity - self.velocity -- delta velocity
end

function Entity:arrival(target)
    local deltaP = target - self.position
    local distance = deltaP:len()

    if distance < self.arrival_radius then
        self.slowing = true
        self.desired_velocity = deltaP:normalized() * self.max_velocity * (distance/self.arrival_radius)
    else
        self.slowing = false
        self.desired_velocity = deltaP:normalized() * self.max_velocity
    end
    self.steering = self.desired_velocity - self.velocity

end

function Entity:evade(target)
    local distance = (target.position - self.position):len()
    local t = distance * 0.01
    self.pursue_evade_future_entity_position = target.position + target.velocity * t
    self:flee(self.pursue_evade_future_entity_position)
end

function Entity:flee(target)
    local deltaP = self.position - target
    local distance = deltaP:len()

    if distance < self.flee_radius then
        self.slowing = true
        self.desired_velocity = deltaP:normalized() * self.max_velocity * (1-(distance/self.flee_radius))
    else
        -- decrease the speed to zero
        self.slowing = false
        self.desired_velocity = Vector(0, 0)
    end
    self.steering = self.desired_velocity - self.velocity
end

function Entity:seek(target)
    self.desired_velocity = (target - self.position):normalized() * self.max_velocity
    self.steering = self.desired_velocity - self.velocity
end

function Entity:pursue(target)
    local distance = (target.position - self.position):len()
    local t = distance * 0.01
    self.pursue_evade_future_entity_position = target.position + target.velocity * t
    self:arrival(self.pursue_evade_future_entity_position)
end

function Entity:avoidance()
end

function Entity:update(dt)
    if equalsAny(self.behavior, 'seek', 'flee', 'arrival') then
        self[self.behavior](self, self.seek_flee_arrival_target)

    elseif equalsAny(self.behavior, 'pursue', 'evade') then
        self[self.behavior](self, self.pursue_evade_entity)

    elseif self.behavior == 'avoidance' then
        self:avoidance()
    end
    self.steering_force = self.steering:min(self.max_force)
    self.acceleration = self.steering_force/self.mass
    self.velocity = (self.velocity + self.acceleration * dt):min(self.max_velocity)
    self.position = self.position + self.velocity*dt
end

setmetatable(Entity, {__call = function(_, ...) return Entity.new(...) end})
