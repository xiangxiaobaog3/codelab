require 'vector'
require 'utils'

Entity = {}
Entity.__index = Entity

-- An entity probably shouldn't have this many fields... ;_;
function Entity.new(w, h, p, v, mass, max_v, max_f, flee_r, arrival_r)
    return setmetatable({
        position = p or Vector(0, 0),
        velocity = v or Vector(0, 0),
        desired_velocity = Vector(0, 0),
        mass = mass,
        acceleration = Vector(0, 0),
        steering = Vector(0, 0),
        steering_force = Vector(0, 0),
        max_velocity = max_v or 0,
        max_force = max_f or 0,
        width = w,
        height = h,
        behavior = 'seek',
        seek_flee_arrival_target = nil,
        flee_radius = flee_r,
        arrival_radius = arrival_r,
        slowing = false;
        pursue_evade_entity = nil,
        pursue_evade_future_entity_position = nil
    }, Entity)
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
    self.velocity = (self.velocity + self.acceleration*dt):min(self.max_velocity)
    self.position = self.position + self.velocity*dt
end

-- target: Vector
function Entity:seek(target)
    self.desired_velocity = (target - self.position):normalized()*self.max_velocity
    self.steering = self.desired_velocity - self.velocity
end

-- target: Vector
function Entity:flee(target)
    self.desired_velocity = (self.position - target)
    local distance = self.desired_velocity:len()

    if distance < self.flee_radius then
        self.slowing = true
        self.desired_velocity =
        self.desired_velocity:normalized()*self.max_velocity*(1-(distance/self.flee_radius))
    else
        self.slowing = false
        self.desired_velocity = Vector(0, 0)
    end

    self.steering = self.desired_velocity - self.velocity
end

-- target: Vector
function Entity:arrival(target)
    self.desired_velocity = (target - self.position)
    local distance = self.desired_velocity:len()

    if distance < self.arrival_radius then
        self.slowing = true
        self.desired_velocity =
        self.desired_velocity:normalized()*self.max_velocity*(distance/self.arrival_radius)
    else
        self.slowing = false
        self.desired_velocity =
        self.desired_velocity:normalized()*self.max_velocity
    end

    self.steering = self.desired_velocity - self.velocity
end

-- target: Entity
function Entity:pursue(target)
    local distance = (target.position - self.position):len()
    local t = distance*0.01
    self.pursue_evade_future_entity_position = target.position + target.velocity*t
    self:arrival(self.pursue_evade_future_entity_position)
end

-- target: Entity
function Entity:evade(target)
    local distance = (target.position - self.position):len()
    local t = distance*0.01
    self.pursue_evade_future_entity_position = target.position + target.velocity*t
    self:flee(self.pursue_evade_future_entity_position)
end

function Entity:avoidance()

end

local function drawEntity(entity, borderColor, fillColor)
    love.graphics.push()
    love.graphics.translate(entity.position.x, entity.position.y)
    love.graphics.rotate(entity.velocity:angle())
    love.graphics.translate(-entity.position.x, -entity.position.y)
    love.graphics.setLineWidth(1.5)
    love.graphics.setColor(unpack(borderColor))
    love.graphics.rectangle('line', entity.position.x - entity.width/2,
        entity.position.y - entity.height/2, entity.width, entity.height)
    love.graphics.setColor(unpack(fillColor))
    love.graphics.rectangle('fill', entity.position.x - entity.width/2,
        entity.position.y - entity.height/2, entity.width, entity.height)
    love.graphics.pop()
end

local function drawEntityVector(entity, vector_name, color)
    love.graphics.setColor(unpack(color))
    love.graphics.line(entity.position.x, entity.position.y,
        entity.position.x + entity[vector_name].x, entity.position.y + entity[vector_name].y)
    love.graphics.setColor(0, 0, 0)
end

local function drawSlowingArea(entity)
    love.graphics.setColor(0, 0, 0)
    if entity.slowing then love.graphics.setColor(255, 0, 0)
    else love.graphics.setColor(0, 0, 0) end

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

function Entity:draw()
    if equalsAny(self.behavior, 'seek', 'flee', 'arrival') then
        drawEntity(self, {12, 25, 50}, {50, 100, 200})
        drawSlowingArea(self)

    elseif equalsAny(self.behavior, 'pursue', 'evade') then
        drawEntity(self, {50, 12, 25}, {200, 50, 100})
        if debug_draw then drawFutureEntityPosition(self, {200, 50, 100}) end
    end

    if debug_draw then
        love.graphics.setLineWidth(1.2)
        drawEntityVector(self, 'velocity', {0, 255, 0})
        drawEntityVector(self, 'desired_velocity', {0, 0, 0})
        drawEntityVector(self, 'acceleration', {255, 0, 255})
        love.graphics.setLineWidth(1)
    end
end

setmetatable(Entity, {__call = function(_, ...) return Entity.new(...) end})
