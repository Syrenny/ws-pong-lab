from dataclasses import dataclass
from math import isclose

from ws_pong_lab.domain.models import Direction


@dataclass(frozen=True)
class Collision:
    x: float
    y: float
    t: float


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


def calculate_ball_paddle_collision(
    ball_radius: int,
    ball_xy: tuple[float, float],
    ball_vx_vy: tuple[float, float],
    paddle_xy: tuple[float, float],
    paddle_wh: tuple[int, int],
) -> Collision | None:
    return NotImplemented


def calculate_ball_field_collision(
    ball_radius: int,
    ball_xy: tuple[float, float],
    ball_vx_vy: tuple[float, float],
    field_wh: tuple[int, int],
) -> Collision | None:
    return NotImplemented
