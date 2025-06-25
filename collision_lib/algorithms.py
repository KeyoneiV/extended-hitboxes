
import math
from .hitboxes import CircleHitbox, TriangleHitbox, RotatedRectHitbox

def _get_distance_sq(p1, p2):
    """Helper to calculate squared distance between two points."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return dx*dx + dy*dy

def _collide_circle_circle(circle1: CircleHitbox, circle2: CircleHitbox) -> bool:
    """Checks collision between two circles."""
    return _get_distance_sq(circle1.position, circle2.position) <= (circle1.radius + circle2.radius)**2

def _get_closest_point_on_segment_to_point(segment_start, segment_end, point):
    """
    Helper function: Finds the closest point on a line segment to a given point.
    Used for Circle-LineSegment collision.
    """

    ax, ay = segment_start
    bx, by = segment_end
    px, py = point

    ab_x, ab_y = bx - ax, by - ay
    ap_x, ap_y = px - ax, py - ay

    ab_length_sq = ab_x*ab_x + ab_y*ab_y
    if ab_length_sq == 0:
        return segment_start

    dot_product = ap_x*ab_x + ap_y*ab_y
    t = dot_product / ab_length_sq
    t = max(0, min(1, t))

    closest_x = ax + t * ab_x
    closest_y = ay + t * ab_y
    return (closest_x, closest_y)


def _sign(p1, p2, p3):
    """
    Calculates the 2D cross product of vectors (p2-p1) and (p3-p1).
    The sign indicates which side p3 is on relative to the line p1-p2.
    """
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def _point_in_triangle(pt, v1, v2, v3):
    """
    Checks if a point is inside a triangle using the 'same side' test.
    pt: (x, y) coordinates of the point to check
    v1, v2, v3: (x, y) coordinates of the triangle's vertices
    """
    s1 = _sign(v1, v2, pt)
    s2 = _sign(v2, v3, pt)
    s3 = _sign(v3, v1, pt)

    has_neg = (s1 < 0) or (s2 < 0) or (s3 < 0)
    has_pos = (s1 > 0) or (s2 > 0) or (s3 > 0)


    return not (has_neg and has_pos)


def _collide_circle_triangle(circle: CircleHitbox, triangle: TriangleHitbox) -> bool:
    """Checks collision between a circle and a triangle."""

    tri_vertices = triangle._get_world_vertices()
    vertex_A = tri_vertices[0]
    vertex_B = tri_vertices[1]
    vertex_C = tri_vertices[2]

    if _point_in_triangle(circle.position, vertex_A, vertex_B, vertex_C):
        return True

    edges = [
        (vertex_A, vertex_B),
        (vertex_B, vertex_C),
        (vertex_C, vertex_A)
    ]

    for edge_start, edge_end in edges:
        closest_pt = _get_closest_point_on_segment_to_point(edge_start, edge_end, circle.position)
        if _get_distance_sq(circle.position, closest_pt) <= circle.radius**2:
            return True


    return False

def _project_polygon_onto_axis(vertices, axis):
    """Projects a polygon's vertices onto an axis and returns the min/max projection."""
    pass

def _get_axis_normals(vertices):
    """Calculates normalized perpendicular normals for polygon edges."""
    pass

