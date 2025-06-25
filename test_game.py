import pygame
import sys
import math

# Import your custom hitbox classes and the main collision check function
from collision_lib import CircleHitbox, TriangleHitbox, check_collision # <-- Added TriangleHitbox here

# --- Pygame Initialisation ---
pygame.init()

# --- Screen Setup ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collision Lib Test - Two Circles and a Triangle")

# --- Clock for Frame Rate ---
clock = pygame.time.Clock()
FPS = 60

# --- Create Hitbox Objects ---
# Fixed circle
fixed_circle = CircleHitbox(position=[SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2], radius=75)

# Movable circle (controlled by mouse)
movable_circle = CircleHitbox(position=[SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2], radius=50)

# --- NEW: Create a TriangleHitbox ---
# Define local vertices relative to the triangle's center (0,0)
# This triangle will be an equilateral triangle pointing upwards
triangle_size = 80
triangle_height = triangle_size * (math.sqrt(3) / 2) # Height of an equilateral triangle

# Vertices relative to its own center
# Top vertex
v1 = (0, -triangle_height / 2)
# Bottom-left vertex
v2 = (-triangle_size / 2, triangle_height / 2)
# Bottom-right vertex
v3 = (triangle_size / 2, triangle_height / 2)

triangle_vertices_local = [v1, v2, v3]

# Create the TriangleHitbox instance
# Position it somewhere on the screen, e.g., top-left
test_triangle = TriangleHitbox(position=[150, 150], vertices_local=triangle_vertices_local)


# --- Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update Game State ---
    mouse_x, mouse_y = pygame.mouse.get_pos()
    movable_circle.position[0] = mouse_x
    movable_circle.position[1] = mouse_y

    # --- Collision Check ---

    is_colliding_circles = check_collision(fixed_circle, movable_circle)

    if check_collision(movable_circle, test_triangle):
        print("Circle is colliding with Triangle!")
    else:
        print("No collision.")

    # --- Visual Feedback (Drawing) ---
    screen.fill((0, 0, 0))


    if is_colliding_circles:
        color_fixed_circle = (0, 255, 0) # Green
        color_movable_circle = (0, 255, 0) # Green
    else:
        color_fixed_circle = (255, 0, 0) # Red
        color_movable_circle = (0, 255, 255) # Cyan

    # Draw circles
    fixed_circle.draw(screen, color_fixed_circle, 2)
    movable_circle.draw(screen, color_movable_circle, 2)

    triangle_color = (255, 255, 0) # Yellow
    test_triangle.draw(screen, triangle_color, 2)

    # Optional: Draw AABBs for debugging
    pygame.draw.rect(screen, (255, 255, 0), fixed_circle.get_aabb(), 1)
    pygame.draw.rect(screen, (255, 255, 0), movable_circle.get_aabb(), 1)
    pygame.draw.rect(screen, (255, 0, 255), test_triangle.get_aabb(), 1) # Magenta AABB for triangle


    # --- Update Display ---
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(FPS)

# --- Pygame Shutdown ---
pygame.quit()
sys.exit()