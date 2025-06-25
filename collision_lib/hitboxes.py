
# === Imports ===

import pygame
import math

# === Base Hitbox Class ===

class BaseHitbox():

    def __init__(self,position,is_static=False,owner=None):
        self.position = position
        self.owner = owner
        self.is_static = False

    def get_aabb(self):
        """
        This method must be defined in Inhereted Class methods
        """

        pass

    def draw(self):
        """
        same as method above
        """

        pass

# === Concrete Hitbox Classes ===

class CircleHitbox(BaseHitbox):

    def __init__(self,position,radius,is_staic=False,owner=None):
        super().__init__(position,is_staic,owner)
        self.radius = radius

    def get_aabb(self):
        """Calculates and returns the AABB for a circle."""
        min_x = self.position[0] - self.radius
        min_y = self.position[1] - self.radius
        max_x = self.position[0] + self.radius
        max_y = self.position[1] + self.radius
        return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def draw(self, surface: pygame.Surface, color, width=1):

        pygame.draw.circle(surface, color, (int(self.position[0]), int(self.position[1])), int(self.radius), width)

class TriangleHitbox(BaseHitbox):

    def __init__(self,position,vertices_local,is_static=False,owner=None):

        super().__init__(position,is_static=is_static,owner=owner)
        # Store vertices relative to the triangle's 'position' (center)
        # e.g., [(x1, y1), (x2, y2), (x3, y3)] where (0,0) is the triangle's center
        self.vertices_local = [list(v) for v in vertices_local]

    def _get_world_vertices(self):
        """Helper to get actual world coordinates of vertices."""
        # You'll need to add self.position to each local vertex
        return [(v[0] + self.position[0], v[1] + self.position[1]) for v in self.vertices_local]

    def get_aabb(self) -> pygame.Rect:
        """Calculates and returns the AABB for a triangle."""
        world_vertices = self._get_world_vertices()
        if not world_vertices: return pygame.Rect(0,0,0,0) # Handle empty case

        min_x = min(v[0] for v in world_vertices)
        max_x = max(v[0] for v in world_vertices)
        min_y = min(v[1] for v in world_vertices)
        max_y = max(v[1] for v in world_vertices)
        return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def draw(self, surface: pygame.Surface, color, width=1):
        """Draws the triangle on the surface."""
        pygame.draw.polygon(surface, color, self._get_world_vertices(), width)

class RotatedRectHitbox(BaseHitbox):
    def __init__(self, position, width, height, angle=0.0,is_static=False,owner=None):
        super().__init__(position,is_static,owner)
        self.width = width
        self.height = height
        self.angle = angle # Store in radians for math functions

    def _get_world_corners(self):
        """Helper to calculate the four world corners of the rotated rectangle."""
        # This is where you'll implement the rotation and translation logic
        # for the four corners based on self.position, self.width, self.height, self.angle
        # You'll need math.cos and math.sin here
        half_width = self.width / 2
        half_height = self.height / 2

        corners_local = [
            (-half_width, -half_height), # Bottom-left relative to center
            ( half_width, -half_height), # Bottom-right
            ( half_width,  half_height), # Top-right
            (-half_width,  half_height)  # Top-left
        ]

        rotated_corners = []
        cos_angle = math.cos(self.angle)
        sin_angle = math.sin(self.angle)

        for x_local, y_local in corners_local:
            x_rotated = x_local * cos_angle - y_local * sin_angle
            y_rotated = x_local * sin_angle + y_local * cos_angle
            rotated_corners.append((x_rotated + self.position[0], y_rotated + self.position[1]))
        return rotated_corners


    def get_aabb(self) -> pygame.Rect:
        """Calculates and returns the AABB for a rotated rectangle."""
        world_corners = self._get_world_corners()
        if not world_corners: return pygame.Rect(0,0,0,0)

        min_x = min(c[0] for c in world_corners)
        max_x = max(c[0] for c in world_corners)
        min_y = min(c[1] for c in world_corners)
        max_y = max(c[1] for c in world_corners)
        return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def draw(self, surface: pygame.Surface, color, width=1):
        """Draws the rotated rectangle on the surface."""
        pygame.draw.polygon(surface, color, self._get_world_corners(), width)