import math
from random import randint
import sys

from Box2D import b2Shape, b2World
from pygame import init, display, draw, event, locals, Color
from pygame.time import Clock

w_width, w_height = 800, 600
black = Color(0, 0, 0)
world = b2World(gravity=(0, 9.8))
actors, colors = [], []
PPM = 64.0  # Pixels per Meter


def add_rect_body(kind, x, y, width, height, angle=0.0, mass=1.0, rest=0.0,
                  frict=0.75):
    body_factory = {
        'static': world.CreateStaticBody,
        'dynamic': world.CreateDynamicBody,
    }[kind]

    body = body_factory(position=(x/PPM, y/PPM), angle=angle, mass=mass)
    body.CreatePolygonFixture(box=(width/PPM, height/PPM), density=1,
                              friction=frict, restitution=rest)
    return body


def ground_arc(radius, segments, centerX, centerY):
    angle_incr = math.pi/(2.0*segments)
    for i in range(segments):
        angle = angle_incr*(i+1)
        x = centerX + math.cos(angle) * radius
        y = centerY + math.sin(angle) * radius
        add_rect_body("static", x, y, 2.5, 20, angle)


def collision_targets():
    for i in range(9):
        x, y = (200, w_height-20-i*20)
        body = add_rect_body("dynamic", x, y, 15, 10,
                             angle=0.0, mass=0.01, rest=0.2, frict=0.75)
        body.userData = (x/PPM, y/PPM)
        actors.append(body)


def reset_bodies():
    for a in actors:
        data = a.userData
        a.awake = False
        a.position = data
        a.angle = 0
        a.awake = True


def load():
    add_rect_body("static", w_width/2, w_height-10, w_width/2, 10)
    add_rect_body("static", 10, w_height/2, 10, w_height/2)
    ground_arc(w_width/3, 10, w_width*2/3, w_height-20-w_width/3)
    collision_targets()

    x, y = w_width-42, 100
    ball = world.CreateDynamicBody(position=(x/PPM, y/PPM), mass=10.0)
    ball.CreateCircleFixture(radius=40/PPM, density=1,
                             friction=0.75, restitution=0.5)
    ball.userData = (x/PPM, y/PPM)
    actors.append(ball)


def update(dt):
    world.Step(dt, 1, 1)


def render(surface):
    surface.fill(black)

    c = 0
    for bv in world:
        x, y = bv.position
        if c >= len(colors):
            colors.append(Color(randint(40, 255), randint(40, 255),
                                randint(40, 255)))
        color = colors[c]
        c += 1
        for fv in bv:
            s = fv.shape
            st = fv.shape.type
            if st == b2Shape.e_circle:
                draw.circle(surface, color, (int(x*PPM), int(y*PPM)),
                            int(s.radius*PPM))
            elif st == b2Shape.e_polygon:
                transformed_verts = [bv.transform * v for v in s.vertices]
                verts = [(v.x*PPM, v.y*PPM) for v in transformed_verts]
                draw.polygon(surface, color, verts)


if __name__ == '__main__':
    init()
    fps_clock = Clock()
    window_surface = display.set_mode((w_width, w_height))
    display.set_caption("Pygame test")

    load()

    while True:
        for e in event.get():
            if e.type == locals.QUIT:
                sys.exit()
            elif e.type == locals.KEYDOWN:
                if e.key == ord(' '):
                    reset_bodies()

        dt = fps_clock.tick(60)
        update(dt/1000.0)

        render(window_surface)
        display.update()
