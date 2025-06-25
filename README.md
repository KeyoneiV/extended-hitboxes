Extended Hitboxes
A lightweight and extensible 2D collision detection library for Pygame applications, designed to provide accurate and flexible collision handling beyond basic rectangles.

Features
Diverse Shape Support: Includes collision detection for:

Circles: Defined by a center point and a radius.

Triangles: Defined by a center point and local vertices.

Rotated Rectangles: Defined by a center point, width, height, and rotation angle.

Efficient Collision Pipeline:

Broad-Phase AABB Check: Utilises Axis-Aligned Bounding Boxes (AABBs) for a fast initial check, powered by Pygame's Rect objects. If AABBs don't overlap, no further complex calculations are performed.

Narrow-Phase Dispatch System: Automatically selects and executes the correct, highly accurate collision algorithm for any given pair of hitbox types.

Accurate Algorithms:

Circle-Circle Collision: Uses efficient squared distance checks.

Circle-Triangle Collision: Combines closest-point-on-segment checks with a robust point-in-triangle test.

(Planned: Separating Axis Theorem (SAT) for Polygon-Polygon collisions, including Triangle-Triangle, RotatedRect-RotatedRect, and Triangle-RotatedRect.)

Easy Integration: Designed with a Pygame-like API for drawing and collision checking.

Debugging Visuals: Each hitbox type includes a draw() method for visual debugging on a Pygame surface.

Installation
Currently, "Extended Hitboxes" can be installed directly from the source code.

Clone the repository:

git clone https://github.com/KeyoneiV/extended-hitboxes.git
cd extended-hitboxes

Install locally using pip:

pip install .

(Ensure you have pygame installed in your environment: pip install pygame)

Usage
Once installed, you can import and use Extended Hitboxes in your Pygame project.

1. Creating Hitboxes
   import pygame
   from collision_lib import CircleHitbox, TriangleHitbox, RotatedRectHitbox

# Example: Create a CircleHitbox
my_circle_hitbox = CircleHitbox(position=[100, 100], radius=50, owner="Player")

# Example: Create a TriangleHitbox
# Vertices are relative to the triangle's center (0,0)
import math
triangle_size = 80
triangle_height = triangle_size * (math.sqrt(3) / 2)
triangle_vertices = [(0, -triangle_height / 2),(-triangle_size / 2, triangle_height / 2),(triangle_size / 2, triangle_height / 2)]
my_triangle_hitbox = TriangleHitbox(position=[200, 200], vertices_local=triangle_vertices, owner="Wall")

# Example: Create a RotatedRectHitbox
# Angle is in radians
my_rotated_rect_hitbox = RotatedRectHitbox(position=[300, 300], width=100, height=50, angle=math.radians(45), owner="Door")

2. Checking for Collisions
   Use the check_collision function for general collision detection between any two hitbox types.

from collision_lib import check_collision

# Assuming my_circle_hitbox and my_triangle_hitbox are already created
if check_collision(my_circle_hitbox, my_triangle_hitbox):
    print("Circle is colliding with Triangle!")
else:
    print("No collision.")

# You can check any combination:
# if check_collision(my_circle_hitbox, my_rotated_rect_hitbox):
#     print("Circle-Rotated Rect collision!")
# if check_collision(my_triangle_hitbox, my_rotated_rect_hitbox):
#     print("Triangle-Rotated Rect collision!")

3. Drawing Hitboxes (for Debugging)
   Each hitbox class has a draw() method that takes a Pygame surface, color, and optional line width.

# In your Pygame game loop:
# screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Draw the hitboxes
my_circle_hitbox.draw(screen, (255, 0, 0), 2) # Red circle outline
my_triangle_hitbox.draw(screen, (0, 255, 0), 2) # Green triangle outline
my_rotated_rect_hitbox.draw(screen, (0, 0, 255), 2) # Blue rectangle outline

# Optionally draw AABBs for broad-phase debugging:
# pygame.draw.rect(screen, (255, 255, 0), my_circle_hitbox.get_aabb(), 1)

Contributing
Contributions are welcome! If you have suggestions or want to improve the algorithms, feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Author
Keyonei Victory
