import turtle
import math
import random


class ShapeProjectorBase:
    def __init__(self, shape: list[tuple[float, float, float]]):
        self._shape = shape
        self._turtle_screen = turtle.Screen()
        self._turtle_object = turtle.Turtle()
        self._setup_turtle()
        self._mouse_states = [[], []]

        self._x_angle = 0
        self._y_angle = 0
        self._z_angle = 0
        self._scale = 50
        self._center_x = 0
        self._center_y = 0

    def _setup_turtle(self):
        self._turtle_screen.bgcolor((0, 0, 0))
        self._turtle_object.pencolor("light blue")
        self._turtle_object.pensize(3)
        self._turtle_object.hideturtle()
        self._turtle_screen.tracer(0)

    @staticmethod
    def _rotate_z(xyz_point, theta) -> tuple[float, float, float]:
        """Rotate point p by theta radians around the z-axis."""
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = cs * xyz_point[0] - sn * xyz_point[1]
        y = sn * xyz_point[0] + cs * xyz_point[1]
        z = xyz_point[2]
        return (x, y, z)

    @staticmethod
    def _rotate_x(xyz_point, theta) -> tuple[float, float, float]:
        """Rotate xyz_pointp by theta radians around the x-axis."""
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = xyz_point[0]
        y = cs * xyz_point[1] - sn * xyz_point[2]
        z = sn * xyz_point[1] + cs * xyz_point[2]
        return (x, y, z)

    @staticmethod
    def _rotate_y(xyz_point, theta) -> tuple[float, float, float]:
        """Rotate xyz_point by theta radians around the y-axis."""
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = cs * xyz_point[0] + sn * xyz_point[2]
        y = xyz_point[1]
        z = -sn * xyz_point[0] + cs * xyz_point[2]
        return (x, y, z)

    @staticmethod
    def _perspective_projection(xyz_point) -> tuple[float, float, float]:
        """Project perspective onto points by distance."""
        distance = 5

        z = 1 / (distance - xyz_point[2])
        x = xyz_point[0] * z
        y = xyz_point[1] * z
        return (x, y, z)

    def _draw_line(self, a: tuple[float, float, float], b: tuple[float, float, float]):
        """Draw a line between points a and b."""
        x1 = a[0] * self._scale + self._center_x
        y1 = a[1] * self._scale + self._center_y
        x2 = b[0] * self._scale + self._center_x
        y2 = b[1] * self._scale + self._center_y
        self._turtle_object.penup()
        self._turtle_object.goto(x1, y1)
        self._turtle_object.pendown()
        self._turtle_object.goto(x2, y2)


class ShapeProjector(ShapeProjectorBase):
    def __init__(self, shape: list[tuple[float, float, float]]):
        super().__init__(shape)

    def set_color(self, color):
        self._turtle_object.pencolor(color)

    def draw_shape(self, x, y):
        """Draw the cube using the current point positions."""
        self._center_x, self._center_y = x, y
        self._turtle_object.clear()
        self._draw_line(self._shape[0], self._shape[1])
        self._draw_line(self._shape[1], self._shape[2])
        self._draw_line(self._shape[2], self._shape[3])
        self._draw_line(self._shape[3], self._shape[0])
        self._draw_line(self._shape[4], self._shape[5])
        self._draw_line(self._shape[5], self._shape[6])
        self._draw_line(self._shape[6], self._shape[7])
        self._draw_line(self._shape[7], self._shape[4])
        self._draw_line(self._shape[0], self._shape[4])
        self._draw_line(self._shape[1], self._shape[5])
        self._draw_line(self._shape[2], self._shape[6])
        self._draw_line(self._shape[3], self._shape[7])
        self._turtle_screen.update()

    def add_x_angle_rotation(self, rotation: float):
        self._x_angle += rotation
        self._shape = [self._rotate_x(p, self._x_angle) for p in self._shape]
        return self

    def add_y_angle_rotation(self, rotation: float):
        self._y_angle += rotation
        self._shape = [self._rotate_y(p, self._y_angle) for p in self._shape]
        return self

    def add_z_angle_rotation(self, rotation: float):
        self._z_angle += rotation
        self._shape = [self._rotate_z(p, self._z_angle) for p in self._shape]
        return self

    def add_total_angle_rotation(self, rotation: float):
        self._x_angle += rotation
        self._y_angle += rotation
        self._z_angle += rotation

        self._shape = [self._rotate_x(p, self._x_angle) for p in self._shape]
        self._shape = [self._rotate_y(p, self._y_angle) for p in self._shape]
        self._shape = [self._rotate_z(p, self._z_angle) for p in self._shape]
        return self


shape = [
    (-1, -1, -1),
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, 1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
]


def get_circle_position(radius: float, step: float):
    point = ((radius * math.cos(step) + 2), (radius * math.sin(step) + 2))
    return point


projector = ShapeProjector(shape)
projector1 = ShapeProjector(shape)
projector2 = ShapeProjector(shape)
projector3 = ShapeProjector(shape)
projector4 = ShapeProjector(shape)
projector5 = ShapeProjector(shape)


projector1.set_color((0.9, 0.1, 0.4))
projector2.set_color((0.1, 0.5, 0.9))
projector3.set_color((0.8, 0.7, 0.4))
projector4.set_color((0.1, 0.4, 0.1))
projector5.set_color((0.5, 0.3, 0.9))


radius1 = 300
radius2 = 280
radius3 = 350
radius4 = 320
radius5 = 400

n1 = 0
n2 = 0.7
n3 = 2.5
n4 = 1.5
n5 = 3

point1 = get_circle_position(radius1, n1)
point2 = get_circle_position(radius2, n2)
point3 = get_circle_position(radius3, n3)
point4 = get_circle_position(radius4, n4)
point5 = get_circle_position(radius5, n5)


while True:

    projector.draw_shape(0, 0)
    projector1.draw_shape(*point1)
    projector2.draw_shape(*point2)
    projector3.draw_shape(*point3)
    projector4.draw_shape(*point4)
    projector5.draw_shape(*point5)

    projector.add_total_angle_rotation(0.00001)

    projector1.add_total_angle_rotation(0.00001)
    projector2.add_total_angle_rotation(0.00001)
    projector3.add_total_angle_rotation(0.00001)
    projector4.add_total_angle_rotation(0.00001)
    projector5.add_total_angle_rotation(0.00001)

    n1 += random.randrange(50, 100) / 2000
    n2 += random.randrange(50, 100) / 1500
    n3 += random.randrange(50, 100) / 3000
    n4 += random.randrange(50, 100) / 2000
    n5 += random.randrange(50, 100) / 2000

    radius1 += random.randrange(-100, 100) / 100
    radius2 += random.randrange(-100, 100) / 100
    radius3 += random.randrange(-100, 100) / 100
    radius4 += random.randrange(-100, 100) / 100
    radius5 += random.randrange(-100, 100) / 100

    point1 = get_circle_position(radius1, n1)
    point2 = get_circle_position(radius2, n2)
    point3 = get_circle_position(radius3, n3)
    point4 = get_circle_position(radius4, n4)
    point5 = get_circle_position(radius5, n5)
