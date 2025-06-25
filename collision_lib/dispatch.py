
import pygame
from .hitboxes import BaseHitbox, CircleHitbox, TriangleHitbox, RotatedRectHitbox
from .algorithms import (
    _collide_circle_circle,
    _collide_circle_triangle,
)

_COLLISION_FUNCTIONS = {
    (CircleHitbox, CircleHitbox): _collide_circle_circle,
    (CircleHitbox, TriangleHitbox): _collide_circle_triangle,
    (TriangleHitbox, CircleHitbox): lambda t, c: _collide_circle_triangle(c, t),
}

def check_collision(hitbox_a: BaseHitbox, hitbox_b: BaseHitbox) -> bool:
    """
    Public function to check collision between two hitboxes.
    Performs a broad-phase AABB check first for efficiency,
    then dispatches to the appropriate narrow-phase algorithm.
    """

    # Ensure both objects are instances of BaseHitbox
    if not isinstance(hitbox_a, BaseHitbox) or not isinstance(hitbox_b, BaseHitbox):
        print("Error: check_collision expects BaseHitbox instances.")
        return False

    # Broad Phase
    if not hitbox_a.get_aabb().colliderect(hitbox_b.get_aabb()):
        return False

    # Narrow Phase
    type_a = type(hitbox_a)
    type_b = type(hitbox_b)

    collision_func = _COLLISION_FUNCTIONS.get((type_a, type_b))
    if collision_func:
        return collision_func(hitbox_a, hitbox_b)

    # If not found, check (TypeB, TypeA) to cover permutations
    collision_func_reversed = _COLLISION_FUNCTIONS.get((type_b, type_a))
    if collision_func_reversed:
        # Call the function with arguments swapped if the lookup was reversed
        return collision_func_reversed(hitbox_b, hitbox_a)

    # Fallback if no specific collision function is defined for the pair
    print(f"Warning: No specific narrow-phase collision defined for {type_a.__name__} and {type_b.__name__}.")
    return False