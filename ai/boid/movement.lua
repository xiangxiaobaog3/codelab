local function seek(entity, target)
    entity.desired_velocity = (target - entity.position):min(entity.max_velocity)
    entity.steering = entity.desired_velocity - entity.velocity -- force
end

local function arrival(entity, target, radius)
    local radius = radius or entity.arrival_radius
    local desired = target - entity.position
    local distance = desired:len()
    if (distance <= radius) then
        -- reduce velocity
        entity.slowing = true
        entity.desired_velocity = desired:min(entity.max_velocity) * distance/radius
    else
        entity.slowing = false
        entity.desired_velocity = desired:min(entity.max_velocity)
    end
    entity.steering = entity.desired_velocity - entity.velocity
end

local function collisionAvoidance(entity, target)
    entity.ahead = entity.velocity:clone()
    entity.ahead:normalized()
    entity.ahead = entity.position + entity.ahead * entity.max_see_ahead
    -- entity.ahead = entity.ahead * entity.max_see_ahead
    entity.ahead2 = entity.ahead * 0.5

    local mostThreateningObstacle = findMostThreateningObstacle(entity)
    local avoidance = Vector(0, 0)

    if (mostThreateningObstacle) then
        avoidance.x = entity.ahead.x - mostThreateningObstacle.center.x
        avoidance.y = entity.ahead.y - mostThreateningObstacle.center.y
        avoidance:normalized()
        avoidance = avoidance * entity.max_avoid_force
    else
        avoidance = avoidance * 0
    end
    seek(entity, target)
    entity.steering = entity.steering + avoidance
end

local function evade(entity, target)
end

local function pursit(entity, target)
end

local function wander(entity, target)
    -- move the character randomly
    local angle_change = entity.angle_change or 1
    local circle_center = entity.velocity:clone()
    local circle_distance = entity.circle_distance
    circle_center:normalized()
    circle_center = circle_center * circle_distance
    -- displacement force, which in responsible for the right or left turn
    local displacement = Vector(0, -1) * circle_distance
    displacement:setAngle(entity.wander_angle)
    entity.wander_angle = entity.wander_angle + math.random() * angle_change - angle_change * 0.5
    wander_force = circle_center + displacement
    entity.steering = wander_force - entity.velocity
end

local function flee(entity, target, radius)
    local radius = radius or entity.flee_radius
    local desired = entity.position - target
    local distance = desired:len()

    if (distance < radius) then
        -- acclerate speed
        entity.slowing = true --
        entity.desired_velocity = desired:normalized() * entity.max_velocity * (1-(distance/radius))
    else
        entity.slowing = false
        entity.desired_velocity = Vector(0, 0)
    end
    entity.steering = entity.desired_velocity - entity.velocity
end

SteeringBehavior = {
    seek=seek,
    flee=flee,
    arrival=arrival,
    pursit=pursit,
    wander=wander,
    collisionAvoidance=collisionAvoidance,
}

