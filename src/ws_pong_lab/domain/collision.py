from dataclasses import dataclass
from enum import StrEnum
from math import cos, hypot, inf, isclose, radians, sin

from ws_pong_lab.domain.models import Direction


@dataclass(frozen=True)
class Collision:
    x: float
    y: float
    t: float


class WallSide(StrEnum):
    LEFT = "left"
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"


@dataclass(frozen=True)
class WallCollision:
    collision: Collision
    side: WallSide


def _clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


def calculate_next_paddle_y(
    paddle_y: float,
    paddle_height: int,
    paddle_vy: float,
    direction: Direction,
    field_height: int,
) -> float:
    if direction is Direction.UP:
        paddle_y -= paddle_vy
    else:
        paddle_y += paddle_vy

    return _clamp(value=paddle_y, min_value=0, max_value=field_height - paddle_height)


def calculate_axis_collision_t(
    initial: float,
    target: float,
    velocity: float,
) -> float | None:
    if initial < target and velocity < 0:
        return None

    if initial > target and velocity > 0:
        return None

    if isclose(initial, target, rel_tol=1e-9, abs_tol=1e-12):
        return 0

    if velocity == 0:
        return None

    return (target - initial) / velocity


def calculate_axis_enter_exit_t(
    *,
    initial: float,
    velocity: float,
    min_value: float,
    max_value: float,
) -> tuple[float, float] | None:
    if isclose(velocity, 0.0, rel_tol=1e-9, abs_tol=1e-12):
        if min_value <= initial <= max_value:
            return -inf, inf

        return None

    t1 = (min_value - initial) / velocity
    t2 = (max_value - initial) / velocity

    return min(t1, t2), max(t1, t2)


def intersect_ranges(
    a: tuple[float, float], b: tuple[float, float]
) -> tuple[float, float] | None:
    if a[1] < a[0] or b[1] < b[0]:
        raise ValueError(f"Ranges must be sorted, got a={str(a)} b={str(b)}")

    start = max(a[0], b[0])

    end = min(a[1], b[1])

    if start <= end:
        return (start, end)

    return None


def calculate_ball_paddle_collision(
    ball_radius: int,
    ball_xy: tuple[float, float],
    ball_vx_vy: tuple[float, float],
    paddle_xy: tuple[float, float],
    paddle_wh: tuple[int, int],
) -> Collision | None:
    left_extended_x = paddle_xy[0] - ball_radius
    right_extended_x = paddle_xy[0] + paddle_wh[0] + ball_radius

    x_enter_exit_t = calculate_axis_enter_exit_t(
        initial=ball_xy[0],
        velocity=ball_vx_vy[0],
        min_value=left_extended_x,
        max_value=right_extended_x,
    )

    if x_enter_exit_t is None:
        return None

    top_extended_y = paddle_xy[1] - ball_radius
    bottom_extended_y = paddle_xy[1] + paddle_wh[1] + ball_radius

    y_enter_exit_t = calculate_axis_enter_exit_t(
        initial=ball_xy[1],
        velocity=ball_vx_vy[1],
        min_value=top_extended_y,
        max_value=bottom_extended_y,
    )

    if y_enter_exit_t is None:
        return None

    intersection = intersect_ranges(x_enter_exit_t, y_enter_exit_t)

    if intersection is None:
        return None

    t = intersection[0]

    x, y = ball_xy[0] + ball_vx_vy[0] * t, ball_xy[1] + ball_vx_vy[1] * t

    return Collision(x=x, y=y, t=t)


def _calculate_horizontal_wall_collision(
    *,
    ball_xy: tuple[float, float],
    ball_vx_vy: tuple[float, float],
    wall_y: float,
    min_x: float,
    max_x: float,
) -> Collision | None:
    t = calculate_axis_collision_t(
        initial=ball_xy[1],
        target=wall_y,
        velocity=ball_vx_vy[1],
    )

    if t is None:
        return None

    x = ball_xy[0] + ball_vx_vy[0] * t

    if not min_x <= x <= max_x:
        return None

    return Collision(x=x, y=wall_y, t=t)


def _calculate_vertical_wall_collision(
    *,
    ball_xy: tuple[float, float],
    ball_vx_vy: tuple[float, float],
    wall_x: float,
    min_y: float,
    max_y: float,
) -> Collision | None:
    t = calculate_axis_collision_t(
        initial=ball_xy[0],
        target=wall_x,
        velocity=ball_vx_vy[0],
    )

    if t is None:
        return None

    y = ball_xy[1] + ball_vx_vy[1] * t

    if not min_y <= y <= max_y:
        return None

    return Collision(x=wall_x, y=y, t=t)


def calculate_ball_vertical_wall_collision(
    ball_radius: int,
    ball_xy: tuple[float, float],
    ball_vx_vy: tuple[float, float],
    field_wh: tuple[int, int],
) -> WallCollision | None:
    field_width, field_height = field_wh

    min_x = ball_radius
    max_x = field_width - ball_radius
    min_y = ball_radius
    max_y = field_height - ball_radius

    collisions = [
        _calculate_vertical_wall_collision(
            ball_xy=ball_xy,
            ball_vx_vy=ball_vx_vy,
            wall_x=min_x,
            min_y=min_y,
            max_y=max_y,
        ),
        _calculate_vertical_wall_collision(
            ball_xy=ball_xy,
            ball_vx_vy=ball_vx_vy,
            wall_x=max_x,
            min_y=min_y,
            max_y=max_y,
        ),
    ]

    valid_collisions = [
        collision
        for collision in collisions
        if collision is not None and collision.t >= 0
    ]

    if not valid_collisions:
        return None

    collision = min(valid_collisions, key=lambda collision: collision.t)
    side = WallSide.LEFT if collision.x == min_x else WallSide.RIGHT

    return WallCollision(collision=collision, side=side)


def calculate_ball_horizontal_wall_collision(
    ball_radius: int,
    ball_xy: tuple[float, float],
    ball_vx_vy: tuple[float, float],
    field_wh: tuple[int, int],
) -> WallCollision | None:
    field_width, field_height = field_wh

    min_x = ball_radius
    max_x = field_width - ball_radius
    min_y = ball_radius
    max_y = field_height - ball_radius

    collisions = [
        _calculate_horizontal_wall_collision(
            ball_xy=ball_xy,
            ball_vx_vy=ball_vx_vy,
            wall_y=min_y,
            min_x=min_x,
            max_x=max_x,
        ),
        _calculate_horizontal_wall_collision(
            ball_xy=ball_xy,
            ball_vx_vy=ball_vx_vy,
            wall_y=max_y,
            min_x=min_x,
            max_x=max_x,
        ),
    ]

    valid_collisions = [
        collision
        for collision in collisions
        if collision is not None and collision.t >= 0
    ]

    if not valid_collisions:
        return None

    collision = min(valid_collisions, key=lambda collision: collision.t)
    side = WallSide.TOP if collision.y == min_y else WallSide.BOTTOM

    return WallCollision(collision=collision, side=side)


def calculate_ball_speed_after_paddle_collision(
    *,
    collision_y: float,
    ball_vx_vy: tuple[float, float],
    paddle_y: float,
    paddle_height: float,
) -> tuple[float, float]:
    max_angle = radians(60)

    vx, vy = ball_vx_vy
    speed = hypot(vx, vy)

    paddle_center_y = paddle_y + paddle_height / 2
    offset = collision_y - paddle_center_y
    normalized = _clamp(offset / (paddle_height / 2), -1.0, 1.0)

    angle = normalized * max_angle

    direction_x = -1 if vx > 0 else 1

    return (
        direction_x * speed * cos(angle),
        speed * sin(angle),
    )


@dataclass(frozen=True)
class BallMotion:
    ball_xy: tuple[float, float]
    ball_vx_vy: tuple[float, float]


def resolve_goal_collision(
    ball_vx_vy: tuple[float, float],
    field_wh: tuple[float, float],
) -> BallMotion:
    return BallMotion(
        ball_xy=(field_wh[0] // 2, field_wh[1] // 2),
        ball_vx_vy=(-ball_vx_vy[0], ball_vx_vy[1]),
    )


def resolve_ball_horizontal_wall_collision(
    collision_xy: tuple[float, float],
    ball_vx_vy: tuple[float, float],
) -> tuple[float, float]:
    return NotImplemented
