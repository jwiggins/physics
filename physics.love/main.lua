
--local world, boxBody, groundBody

function love.load()
    love.physics.setMeter(64)
    world = love.physics.newWorld(0.0, 9.8*64, true)

    local width, height = love.graphics.getDimensions()
    groundBody = love.physics.newBody(world, width/2, height-30, "static")
    local shape = love.physics.newRectangleShape(width, 15)
    local fixture = love.physics.newFixture(groundBody, shape, 0.0)
    fixture:setRestitution(0.5)


    boxBody = love.physics.newBody(world, width/2, 100, "dynamic")
    local shape = love.physics.newRectangleShape(40, 40)
    local fixture = love.physics.newFixture(boxBody, shape, 0.0)
    fixture:setRestitution(0.75)
end

function love.update(dt)
    world:update(dt)
end

function love.draw()
    local width, height = love.graphics.getDimensions()
    love.graphics.push()
    love.graphics.setColor(255, 0, 255, 128)
    local x, y = groundBody:getPosition()
    love.graphics.rectangle("fill", x-width/2, y-7.5, width, 15)

    x, y = boxBody:getPosition()
    love.graphics.push()
    love.graphics.rectangle("fill", x-20, y-20, 40, 40)
    love.graphics.pop()
    love.graphics.pop()
end
