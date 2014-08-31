MovementManager = {}
MovementManager.__index = MovementManager

function MovementManager.new()
    return setmetatable({
        steering = Vector(0, 0),
        desired_steering = Vector(0, 0),
        steering_force = Vector(0, 0),
        acceleration = Vector(0, 0),
    }, MovementManager)
end

-- resulting steering force

function MovementManager:seek(entity, target, slowingRadius)
    self.steering_force = self.steering_force + self:doSeek(entity, target, slowingRadius)
end

function MovementManager:doSeek(entity, target, slowingRadius)
    local slowingRadius = slowingRadius or 0
    local desired = target - entity.position
    local distance = desired:len()
    desired:normalized()
    if distance <= slowingRadius then
        desired = entity.max_velocity * distance/slowingRadius
    else
        desired = desired * entity.max_velocity
    end
    local force = desired - entity.velocity
    return force
end


function MovementManager:flee(entity, target)
end

function MovementManager:wander(entity)
end

function MovementManager:evade(entity, target)
end

function MovementManager:pursuit(entity, target)
    -- pursue
end

function MovementManager:update(entity)
    -- should be called after all behaviors have been invoked
    self.steering_force = self.steering_force:min(self.max_force)
    entity.acceleration = self.steering_force / entity.mass
    entity.velocity = entity.velocity + self.steering
end

function MovementManager:reset()
    -- reset the internal steering force
end
