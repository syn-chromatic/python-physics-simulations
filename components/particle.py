from components.body import BodyType
from components.physics import Physics
from components.graphics import Graphics


class Particle(BodyType):
    def __init__(self, shape: list[tuple[float, float, float]]):
        self.physics = Physics(shape)
        self.color = (1.0, 1.0, 1.0)

    def _draw_circle(self, graphics: Graphics):
        x = self.physics.position.x
        y = self.physics.position.y
        z = self.physics.position.z
        scale = self.physics.scale
        relative_z = scale + z

        relative_z = min(float("inf"), max(0.5, relative_z))
        graphics.draw_circle((x, y), relative_z, self.color)

    def set_color(self, color: tuple[float, float, float]):
        self.color = color

    def draw(self, graphics: Graphics):
        self._draw_circle(graphics)
