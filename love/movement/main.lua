y, x = 20, 20
h, w = 32, 32

function love.draw()
    love.graphics.setColor(0, 24, 50)
    love.graphics.rectangle('fill', x, y, h, w)
    love.graphics.setColor(100, 24, 50)
    love.graphics.setLineWidth(1.5)
    love.graphics.rectangle('line', x, y, h, w)
end
