import math
from .hitboxes import CircleHitbox, TriangleHitbox, RotatedRectHitbox


def _get_distance_sq(p1, p2):
    """Helper to calculate squared distance between two points."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return dx * dx + dy * dy


def _collide_circle_circle(circle1: CircleHitbox, circle2: CircleHitbox) -> bool:
    """Checks collision between two circles."""
    return _get_distance_sq(circle1.position, circle2.position) <= (circle1.radius + circle2.radius) ** 2


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

    ab_length_sq = ab_x * ab_x + ab_y * ab_y
    if ab_length_sq == 0:
        return segment_start

    dot_product = ap_x * ab_x + ap_y * ab_y
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
        if _get_distance_sq(circle.position, closest_pt) <= circle.radius ** 2:
            return True

    return False


def _intervals_overlap(min1, max1, min2, max2) -> bool:
    """Checks if two 1D intervals overlap."""
    return not (max1 < min2 or min1 > max2)


def _get_axis_normals(vertices) -> list[tuple[float, float]]:
    """Calculates normalized perpendicular normals for polygon edges."""
    axes = []
    num_vertices = len(vertices)

    for i in range(num_vertices):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % num_vertices]

        # Edge vector
        edge_x = p2[0] - p1[0]
        edge_y = p2[1] - p1[1]

        # Perpendicular vector (normal)
        normal_x = -edge_y
        normal_y = edge_x

        # Normalize the normal vector
        length = math.sqrt(normal_x * normal_x + normal_y * normal_y)
        if length != 0:
            normalized_normal = (normal_x / length, normal_y / length)
            if normalized_normal not in axes and (-normalized_normal[0], -normalized_normal[1]) not in axes:
                axes.append(normalized_normal)
    return axes


def _project_polygon_onto_axis(vertices, axis) -> tuple[float, float]:
    """Projects a polygon's vertices onto an axis and returns the min/max projection."""
    # Dot product: (vx, vy) . (ax, ay) = vx*ax + vy*ay

    # Get initial min/max from the first vertex
    initial_projection = vertices[0][0] * axis[0] + vertices[0][1] * axis[1]
    min_proj = initial_projection
    max_proj = initial_projection

    # Iterate through remaining vertices
    for i in range(1, len(vertices)):
        current_vertex = vertices[i]
        current_projection = current_vertex[0] * axis[0] + current_vertex[1] * axis[1]
        min_proj = min(min_proj, current_projection)
        max_proj = max(max_proj, current_projection)

    return (min_proj, max_proj)


def _collide_polygon_polygon(poly1_vertices: list[tuple[float, float]],
                             poly2_vertices: list[tuple[float, float]]) -> bool:
    """
    Checks for collision between two convex polygons using the Separating Axis Theorem (SAT).
    poly1_vertices and poly2_vertices should be lists of (x, y) world coordinates.
    """

    # Collect all potential separating axes from both polygons' edges
    axes = []
    axes.extend(_get_axis_normals(poly1_vertices))
    axes.extend(_get_axis_normals(poly2_vertices))

    # Iterate through each axis and check for a separating gap
    for axis in axes:
        min1, max1 = _project_polygon_onto_axis(poly1_vertices, axis)
        min2, max2 = _project_polygon_onto_axis(poly2_vertices, axis)

        if not _intervals_overlap(min1, max1, min2, max2):
            return False

    return True

def _collide_triangle_triangle(triangle1: TriangleHitbox, triangle2: TriangleHitbox) -> bool:
    """Checks collision between two TriangleHitbox objects using SAT."""
    t1_vertices = triangle1._get_world_vertices()
    t2_vertices = triangle2._get_world_vertices()
    return _collide_polygon_polygon(t1_vertices, t2_vertices)


def _collide_rotated_rect_rotated_rect(rect1: RotatedRectHitbox, rect2: RotatedRectHitbox) -> bool:
    """Checks collision between two RotatedRectHitbox objects using SAT."""
    r1_corners = rect1._get_world_corners()
    r2_corners = rect2._get_world_corners()
    return _collide_polygon_polygon(r1_corners, r2_corners)
