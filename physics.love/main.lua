local world, ballBody, groundBody, width, height
local actors = {}

local function newRectBody(kind, x, y, width, height, angle, mass, rest)
    local body = love.physics.newBody(world, x, y, kind)
    local shape = love.physics.newRectangleShape(width, height)
    local fixture = love.physics.newFixture(body, shape, 1.0)
    body:setMass(mass or 1.0)
    body:setAngle(angle or 0.0)
    fixture:setRestitution(rest or 0.5)
    fixture:setFriction(0.75)

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
        local body = newRectBody("dynamic", x, y, 30, 20, 0.0, 0.015, 0.6)
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

    groundBody = newRectBody("static", width/2, height-10, width, 20)
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
    love.graphics.push()
    love.graphics.setColor(255, 0, 255, 128)
    local x, y = groundBody:getPosition()
    love.graphics.rectangle("fill", x-width/2, y-10, width, 20)
    love.graphics.pop()
end
