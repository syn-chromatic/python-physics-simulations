import math

from components.vectors import Vector3D
from components.utils import clamp_float
from copy import deepcopy


class Camera:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.fov = 90
        self.near_plane = 0.1
        self.far_plane = 100.0
        self.yaw = 0.0
        self.pitch = 0.0
        self.camera_position = Vector3D(0.0, 0.0, -500.0)
        self.camera_target = Vector3D(0.0, 0.0, 0.0)
        self.side_direction = Vector3D(1.0, 0.0, 0.0)
        self.up_direction = Vector3D(0.0, 1.0, 0.0)
        self.look_direction = Vector3D(0.0, 0.0, 1.0)

        self.previous_pointer = (width / 2.0, height / 2.0)
        self.save()

    def save(self):
        self.dict = deepcopy(self.__dict__)

    def apply_view_transform(self, position: Vector3D) -> Vector3D:
        look_dir = self.camera_target.subtract_vector(self.camera_position).normalize()
        side_dir = look_dir.cross_product(self.up_direction).normalize()
        up_dir = side_dir.cross_product(look_dir).normalize()

        translated_point = position.subtract_vector(self.camera_position)
        x = translated_point.dot_product(side_dir)
        y = translated_point.dot_product(up_dir)
        z = translated_point.dot_product(look_dir)

        translated_point = Vector3D(x, y, z)
        return translated_point

    def ndc_to_screen_coordinates(self, position: Vector3D) -> Vector3D:
        half_width = self.width / 2.0
        half_height = self.height / 2.0

        x = (position.x) * half_width
        y = (position.y) * half_height

        return Vector3D(x, y, position.z)

    def get_screen_coordinates(self, position: Vector3D):
        view = self.apply_view_transform(position)
        projection = self.calculate_perspective_projection(view)
        screen = self.ndc_to_screen_coordinates(projection)
        return screen

    def calculate_perspective_projection(self, position: Vector3D):
        width = self.width
        height = self.height
        fov_degrees = self.fov
        zn = self.near_plane
        zf = self.far_plane

        xi = position.x
        yi = position.y
        zi = position.z

        aspect_ratio = width / height
        fov_rad = math.tan(math.radians(fov_degrees / 2))

        xo = xi * (1 / (fov_rad * aspect_ratio))
        yo = yi * (1 / (fov_rad))
        zo = zi * ((-zf - zn) / (zn - zf)) + ((2 * zf * zn) / (zn - zf))

        if zi != 0.0:
            xo /= -zi
            yo /= -zi
            zo /= -zi

        vo = Vector3D(xo, yo, zo)
        return vo

    def handle_mouse_movement(self, x: float, y: float) -> None:
        px = self.previous_pointer[0]
        py = self.previous_pointer[1]

        dx = x - px
        dy = y - py

        sensitivity = 0.5
        self.yaw += dx * sensitivity
        self.pitch += dy * sensitivity
        self.pitch = clamp_float(self.pitch, -90.0, 90.0)

        self.previous_pointer = (x, y)

    def increment_plane(self, increment: float):
        near_plane = self.near_plane
        far_plane = self.far_plane

        if (near_plane + increment) >= 0.1:
            near_plane += increment
            far_plane += increment
            self.near_plane = clamp_float(near_plane, 0.0, float("inf"))
            self.far_plane = clamp_float(far_plane, 0.0, float("inf"))

    def increment_position_x(self, increment: float):
        self.camera_position.x += increment

    def increment_position_y(self, increment: float):
        self.camera_position.y += increment

    def increment_position_z(self, increment: float):
        self.camera_position.z += increment

    def increment_target_x(self, increment: float):
        self.camera_target.x += increment

    def increment_target_y(self, increment: float):
        self.camera_target.y += increment

    def increment_target_z(self, increment: float):
        self.camera_target.z += increment

    def reset(self):
        class_dict = deepcopy(self.dict)

        for variable, value in class_dict.items():
            self.__setattr__(variable, value)

    def calculate_yaw_projection(self, position: Vector3D) -> Vector3D:
        yaw_radians = math.radians(self.yaw)
        yaw_cos = math.cos(yaw_radians)
        yaw_sin = math.sin(yaw_radians)

        px = position.x
        py = position.y
        pz = position.z

        yaw_x = (px * yaw_cos) - (pz * yaw_sin)
        yaw_y = py
        yaw_z = (px * yaw_sin) + (pz * yaw_cos)

        yaw_vector = Vector3D(yaw_x, yaw_y, yaw_z)
        return yaw_vector

    def calculate_pitch_projection(self, position: Vector3D) -> Vector3D:
        pitch_radians = math.radians(self.pitch)
        pitch_cos = math.cos(pitch_radians)
        pitch_sin = math.sin(pitch_radians)

        px = position.x
        py = position.y
        pz = position.z

        pitch_x = px
        pitch_y = (py * pitch_cos) - (pz * pitch_sin)
        pitch_z = (py * pitch_sin) + (pz * pitch_cos)

        pitch_vector = Vector3D(pitch_x, pitch_y, pitch_z)
        return pitch_vector
