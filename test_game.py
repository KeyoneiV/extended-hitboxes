import pygame
import sys
import math

from extended_hitboxes import CircleHitbox, TriangleHitbox, RotatedRectHitbox, check_collision

# --- Pygame Initialisation ---
pygame.init()

# --- Screen Setup ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Extended Hitboxes - All Collision Tests")

# --- Clock for Frame Rate ---
clock = pygame.time.Clock()
FPS = 60

# --- Colors for Drawing ---
COLLIDE_COLOR = (0, 255, 0)  # Green
NO_COLLIDE_COLOR_1 = (255, 0, 0)  # Red
NO_COLLIDE_COLOR_2 = (0, 255, 255)  # Cyan
NO_COLLIDE_COLOR_3 = (255, 255, 0)  # Yellow
NO_COLLIDE_COLOR_4 = (255, 0, 255)  # Magenta
AABB_COLOR = (100, 100, 100)  # Dark Grey

# --- Create Hitbox Objects ---

# 1. Circles
circle1 = CircleHitbox(position=[150, 150], radius=50, owner="Circle_A")
circle2 = CircleHitbox(position=[300, 150], radius=40, owner="Circle_B")

# 2. Triangles
triangle_size = 100
triangle_height = triangle_size * (math.sqrt(3) / 2)  # Height of an equilateral triangle
triangle_vertices_local = [
    (0, -triangle_height / 2),  # Top vertex
    (-triangle_size / 2, triangle_height / 2),  # Bottom-left
    (triangle_size / 2, triangle_height / 2)  # Bottom-right
]
triangle1 = TriangleHitbox(position=[400, 200], vertices_local=triangle_vertices_local, owner="Triangle_A")
triangle2 = TriangleHitbox(position=[550, 200], vertices_local=triangle_vertices_local,
                           owner="Triangle_B")

# 3. Rotated Rectangles
rect_width = 120
rect_height = 60
rect_angle_deg_1 = 30  # degrees
rect_angle_deg_2 = -45  # degrees

rotated_rect1 = RotatedRectHitbox(position=[200, 450], width=rect_width, height=rect_height,
                                  angle=math.radians(rect_angle_deg_1), owner="Rect_A")
rotated_rect2 = RotatedRectHitbox(position=[400, 450], width=rect_width, height=rect_height,
                                  angle=math.radians(rect_angle_deg_2), owner="Rect_B")  # Movable by mouse/keyboard

# --- Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Move Triangle2 with WASD
            if event.key == pygame.K_w: triangle2.position[1] -= 5
            if event.key == pygame.K_s: triangle2.position[1] += 5
            if event.key == pygame.K_a: triangle2.position[0] -= 5
            if event.key == pygame.K_d: triangle2.position[0] += 5

            # Move RotatedRect2 with Arrow Keys
            if event.key == pygame.K_UP: rotated_rect2.position[1] -= 5
            if event.key == pygame.K_DOWN: rotated_rect2.position[1] += 5
            if event.key == pygame.K_LEFT: rotated_rect2.position[0] -= 5
            if event.key == pygame.K_RIGHT: rotated_rect2.position[0] += 5

            # Rotate RotatedRect2 with Q/E
            if event.key == pygame.K_q: rotated_rect2.angle -= math.radians(5)
            if event.key == pygame.K_e: rotated_rect2.angle += math.radians(5)

    # --- Update Movable Objects ---
    mouse_x, mouse_y = pygame.mouse.get_pos()
    circle2.position = [mouse_x, mouse_y]
    # --- Collision Checks ---

    # Circle-Circle
    collide_c_c = check_collision(circle1, circle2)
    color_c1 = COLLIDE_COLOR if collide_c_c else NO_COLLIDE_COLOR_1
    color_c2 = COLLIDE_COLOR if collide_c_c else NO_COLLIDE_COLOR_2

    # Circle-Triangle (test circle2 against triangle1)
    collide_c_t = check_collision(circle2, triangle1)
    # Update triangle1 color based on if circle2 is colliding with it
    color_t1_base = NO_COLLIDE_COLOR_3
    color_t1 = COLLIDE_COLOR if collide_c_t else color_t1_base

    # Triangle-Triangle
    collide_t_t = check_collision(triangle1, triangle2)
    color_t2 = COLLIDE_COLOR if collide_t_t else NO_COLLIDE_COLOR_4

    # RotatedRect-RotatedRect
    collide_r_r = check_collision(rotated_rect1, rotated_rect2)
    color_r1 = COLLIDE_COLOR if collide_r_r else NO_COLLIDE_COLOR_1
    color_r2 = COLLIDE_COLOR if collide_r_r else NO_COLLIDE_COLOR_2

    # --- Drawing ---
    screen.fill((0, 0, 0))  # Fill background with black

    # Draw Circles
    circle1.draw(screen, color_c1, 2)
    circle2.draw(screen, color_c2, 2)
    pygame.draw.rect(screen, AABB_COLOR, circle1.get_aabb(), 1)
    pygame.draw.rect(screen, AABB_COLOR, circle2.get_aabb(), 1)

    # Draw Triangles
    triangle1.draw(screen, color_t1, 2)  # Triangle1 color is affected by C-T collision
    triangle2.draw(screen, color_t2, 2)  # Triangle2 color affected by T-T collision
    pygame.draw.rect(screen, AABB_COLOR, triangle1.get_aabb(), 1)
    pygame.draw.rect(screen, AABB_COLOR, triangle2.get_aabb(), 1)

    # Draw Rotated Rectangles
    rotated_rect1.draw(screen, color_r1, 2)
    rotated_rect2.draw(screen, color_r2, 2)
    pygame.draw.rect(screen, AABB_COLOR, rotated_rect1.get_aabb(), 1)
    pygame.draw.rect(screen, AABB_COLOR, rotated_rect2.get_aabb(), 1)

    # --- Update Display ---
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(FPS)

# --- Pygame Shutdown ---
pygame.quit()
sys.exit()
