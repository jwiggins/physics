local world, width, height
local actors, colors = {}, {}

local function newRectBody(kind, x, y, width, height, angle, mass, rest, frict)
    local body = love.physics.newBody(world, x, y, kind)
    local shape = love.physics.newRectangleShape(width, height)
    local fixture = love.physics.newFixture(body, shape, 1.0)
    body:setMass(mass or 1.0)
    body:setAngle(angle or 0.0)
    fixture:setRestitution(rest or 0.5)
    fixture:setFriction(frict or 0.75)

    return body
end

local function groundArc(radius, segments, centerX, centerY)
    local angleIncr = math.pi/(2*segments)
    for i = 1, segments do
        local angle = angleIncr*i
        local x = centerX + math.cos(angle) * radius
        local y = centerY + math.sin(angle) * radius
        newRectBody("static", x, y, 5, 40, angle)
    end
end

local function collisionTargets()
    for i = 0, 8 do
        local x, y = 200, height-20-i*20
        local body = newRectBody("dynamic", x, y, 30, 20, 0.0, 0.015, 0.1, 0.5)
        body:getFixtureList()[1]:setUserData({x, y-10})
        table.insert(actors, #actors+1, body)
    end
end

local function resetBodies()
    for i, a in ipairs(actors) do
        local data = a:getFixtureList()[1]:getUserData()
        a:setAwake(false)
        a:setPosition(data[1], data[2])
        a:setAngle(0)
        a:setAwake(true)
    end
end

function love.load()
    width, height = love.graphics.getDimensions()
    love.physics.setMeter(64)
    world = love.physics.newWorld(0.0, 9.8*64, true)

    newRectBody("static", width/2, height-10, width, 20)
    newRectBody("static", 10, height/2, 20, height)
    groundArc(width/3, 10, width*2/3, height-20-width/3)
    collisionTargets()

    local x, y = width-42, 100
    local ball = love.physics.newBody(world, x, y, "dynamic")
    ball:setMass(10.0)
    local shape = love.physics.newCircleShape(40)
    local fixture = love.physics.newFixture(ball, shape, 1.0)
    fixture:setUserData({x, y})
    fixture:setFriction(0.75)
    fixture:setRestitution(0.5)
    table.insert(actors, #actors+1, ball)
end

function love.update(dt)
    world:update(dt)

    if love.keyboard.isDown(" ") then
        resetBodies()
    end
end

function love.draw()
    local g = love.graphics
    local c = 1

    for bk, bv in pairs(world:getBodyList()) do
        g.push()
        g.translate(bv:getPosition())
        g.rotate(bv:getAngle())
        if not colors[c] then
            colors[c] = {math.random(10,255),math.random(10,255),math.random(10,255)}
        end
        g.setColor(unpack(colors[c]))
        for fk, fv in pairs(bv:getFixtureList()) do
            local s = fv:getShape()
            local st = s:getType()
            if st == "circle" then
                g.circle("fill", 0, 0, s:getRadius())
            elseif st == "polygon" then
                g.polygon("fill", s:getPoints())
            end
        end
        g.pop()
        c = c + 1
    end
end
