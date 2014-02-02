import math
import sys

from Box2D import b2BodyDef, b2FixtureDef, b2Shape, b2World
from pygame import init, display, draw, event, locals, Color
from pygame.time import Clock

width, height = 800, 600
black = Color(0, 0, 0)
white = Color(255, 255, 255)
world = b2World(gravity=(0, -9.8))
actors = []

def add_rect_body(kind, x, y, width, height, angle=0.0, mass=1.0, rest=0.0,
                  frict=0.75):
    body_factory = {
        'static': world.CreateStaticBody,
        'dynamic': world.CreateDynamicBody,
    }[kind]

    body = body_factory(position=(x, y), angle=angle, mass=mass)
    body.CreatePolygonFixture(box=(width, height), density=1,
                              friction=frict, restitution=rest)
    return body


def ground_arc(radius, segments, centerX, centerY):
    angle_incr = math.pi/(2.0*segments)
    for i in range(segments):
        angle = angle_incr*(i+1)
        x = centerX + math.cos(angle) * radius
        y = centerY + math.sin(angle) * radius
        add_rect_body("static", x, y, 5, 40, angle)


def collision_targets():
    for i in range(9):
        x, y = (200, 20+i*20)
        body = add_rect_body("dynamic", x, y, 30, 20, 0.0, 0.015, 0.1, 0.5)
        body.userData = (x, y+10)
        actors.append(body)


def reset_bodies():
    for a in actors:
        data = a.userData
        a.awake = False
        a.position = data
        a.angle = 0
        a.awake = True


def load():
    add_rect_body("static", width/2, height-10, width, 20)
    add_rect_body("static", 10, height/2, 20, height)
    ground_arc(width/3, 10, width*2/3, height-20-width/3)
    collision_targets()

    x, y = width-42, 100
    ball = world.CreateDynamicBody(position=(x, y), mass=10.0)
    ball.CreateCircleFixture(radius=40, density=1,
                             friction=0.75, restitution=0.5)
    ball.userData = (x, y)
    actors.append(ball)


def update(dt):
    world.Step(dt, 3, 3)


def render(surface):
    surface.fill(black)

    for bv in world:
        x, y = bv.position
        for fv in bv:
            s = fv.shape
            st = fv.shape.type
            if st == b2Shape.e_circle:
                draw.circle(surface, white, (int(x), int(y)), int(s.radius))
            elif st == b2Shape.e_polygon:
                draw.polygon(surface, white, s.vertices)


if __name__ == '__main__':
    init()
    fps_clock = Clock()
    window_surface = display.set_mode((width, height))
    display.set_caption("Pygame test")

    load()

    while True:
        for e in event.get():
            if e.type == locals.QUIT:
                sys.exit()
            elif e.type == locals.KEYDOWN:
                if e.key == ord(' '):
                    reset_bodies()

        update(fps_clock.tick(30))

        render(window_surface)
        display.update()
