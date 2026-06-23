import pytest

from ws_pong_lab.domain.collision import (
    Collision,
    calculate_axis_collision_t,
    calculate_ball_field_collision,
    calculate_ball_paddle_collision,
    calculate_next_paddle_y,
)
from ws_pong_lab.domain.models import Direction


def _next_paddle_y_case(
    *, paddle_y: float, direction: Direction, expected_next_y: float, id: str
):
    return pytest.param(paddle_y, direction, expected_next_y)


@pytest.mark.parametrize(
    ("paddle_y", "direction", "expected_next_y"),
    [
        _next_paddle_y_case(
            paddle_y=50,
            direction=Direction.UP,
            expected_next_y=45,
            id="moves-up",
        ),
        _next_paddle_y_case(
            paddle_y=50,
            direction=Direction.DOWN,
            expected_next_y=55,
            id="moves-down",
        ),
        _next_paddle_y_case(
            paddle_y=0,
            direction=Direction.UP,
            expected_next_y=0,
            id="clamps-at-top",
        ),
        _next_paddle_y_case(
            paddle_y=0,
            direction=Direction.DOWN,
            expected_next_y=5,
            id="moves-down-from-top",
        ),
        _next_paddle_y_case(
            paddle_y=94,
            direction=Direction.UP,
            expected_next_y=89,
            id="moves-up-near-bottom",
        ),
        _next_paddle_y_case(
            paddle_y=95,
            direction=Direction.DOWN,
            expected_next_y=95,
            id="clamps-at-bottom",
        ),
        _next_paddle_y_case(
            paddle_y=3,
            direction=Direction.UP,
            expected_next_y=0,
            id="clamps-partial-top-overflow",
        ),
        _next_paddle_y_case(
            paddle_y=91,
            direction=Direction.DOWN,
            expected_next_y=95,
            id="clamps-partial-bottom-overflow",
        ),
    ],
)
def test_calculate_next_paddle_y(
    paddle_y,
    direction,
    expected_next_y,
):
    next_paddle_y = calculate_next_paddle_y(
        paddle_y=paddle_y,
        paddle_height=5,
        paddle_vy=5,
        direction=direction,
        field_height=100,
    )

    assert next_paddle_y == pytest.approx(expected_next_y)


def _axis_collision_t_case(
    *,
    initial: float,
    target: float,
    velocity: float,
    expected_t: float | None,
    id: str,
):
    return pytest.param(
        initial,
        target,
        velocity,
        expected_t,
        id=id,
    )


@pytest.mark.parametrize(
    ("initial", "target", "velocity", "expected_t"),
    [
        _axis_collision_t_case(
            initial=0,
            target=5,
            velocity=3,
            expected_t=5 / 3,
            id="reaches-after-current-tick",
        ),
        _axis_collision_t_case(
            initial=0,
            target=5,
            velocity=5,
            expected_t=1.0,
            id="intersects-at-end-of-tick",
        ),
        _axis_collision_t_case(
            initial=5,
            target=3,
            velocity=3,
            expected_t=None,
            id="wrong-direction-no-intersection",
        ),
        _axis_collision_t_case(
            initial=5,
            target=10,
            velocity=1,
            expected_t=5.0,
            id="reaches-later-with-positive-velocity",
        ),
        _axis_collision_t_case(
            initial=5,
            target=1,
            velocity=-1,
            expected_t=4.0,
            id="reaches-later-with-negative-velocity",
        ),
        _axis_collision_t_case(
            initial=0,
            target=0,
            velocity=5,
            expected_t=0.0,
            id="intersects-at-initial-point",
        ),
        _axis_collision_t_case(
            initial=0,
            target=0,
            velocity=0,
            expected_t=0.0,
            id="intersects-initial-even-with-zero-velocity",
        ),
        _axis_collision_t_case(
            initial=5,
            target=6,
            velocity=0,
            expected_t=None,
            id="zero-velocity-unreachable",
        ),
        _axis_collision_t_case(
            initial=0,
            target=1,
            velocity=-1,
            expected_t=None,
            id="negative-velocity-away-from-target",
        ),
        _axis_collision_t_case(
            initial=1.1,
            target=1.2,
            velocity=0.2,
            expected_t=0.5,
            id="reachable-floating-point",
        ),
        _axis_collision_t_case(
            initial=1.15,
            target=1.25,
            velocity=0.09,
            expected_t=10 / 9,
            id="reaches-after-current-tick-floating-point",
        ),
    ],
)
def test_calculate_axis_collision_t(
    initial: float,
    target: float,
    velocity: float,
    expected_t: float | None,
) -> None:
    collision_t = calculate_axis_collision_t(
        initial=initial,
        target=target,
        velocity=velocity,
    )

    if expected_t is None:
        assert collision_t is None
        return

    assert collision_t == pytest.approx(expected_t)


def _assert_collision_equal(
    actual: Collision | None, expected: Collision | None
) -> None:
    if expected is None:
        assert actual is None
        return

    assert actual is not None
    assert actual.t == pytest.approx(expected.t)
    assert actual.x == pytest.approx(expected.x)
    assert actual.y == pytest.approx(expected.y)


def _paddle_collision_case(
    *,
    ball_xy: tuple[float, float],
    ball_vx_vy: tuple[float, float],
    paddle_xy: tuple[float, float],
    expected: Collision | None,
    id: str,
):
    return pytest.param(
        ball_xy,
        ball_vx_vy,
        paddle_xy,
        expected,
        id=id,
    )


@pytest.mark.parametrize(
    ("ball_xy", "ball_vx_vy", "paddle_y", "expected"),
    [
        _paddle_collision_case(
            ball_xy=(0, -10),
            ball_vx_vy=(9, 9),
            paddle_xy=(10, 0),
            expected=Collision(t=1.0, x=9, y=-1),
            id="hits-top-left-expanded-corner-at-45-degrees",
        ),
        _paddle_collision_case(
            ball_xy=(0, 20),
            ball_vx_vy=(9, -9),
            paddle_xy=(10, 0),
            expected=Collision(t=1.0, x=9, y=11),
            id="hits-bottom-left-expanded-corner-at-45-degrees",
        ),
        _paddle_collision_case(
            ball_xy=(0, 5),
            ball_vx_vy=(8, 0),
            paddle_xy=(10, 0),
            expected=None,
            id="does-not-reach-expanded-rect",
        ),
        _paddle_collision_case(
            ball_xy=(0, 12),
            ball_vx_vy=(10, -2),
            paddle_xy=(10, 0),
            expected=Collision(t=0.9, x=9, y=10.2),
            id="diagonal-bottom-expanded-hit",
        ),
        _paddle_collision_case(
            ball_xy=(0, -2),
            ball_vx_vy=(10, 2),
            paddle_xy=(10, 0),
            expected=Collision(t=0.9, x=9, y=-0.2),
            id="diagonal-top-expanded-hit",
        ),
        _paddle_collision_case(
            ball_xy=(0, 11.1),
            ball_vx_vy=(10, 0),
            paddle_xy=(10, 0),
            expected=None,
            id="below-expanded-zone-miss",
        ),
        _paddle_collision_case(
            ball_xy=(0, -1.1),
            ball_vx_vy=(10, 0),
            paddle_xy=(10, 0),
            expected=None,
            id="above-expanded-zone-miss",
        ),
        _paddle_collision_case(
            ball_xy=(0, 5),
            ball_vx_vy=(10, 0),
            paddle_xy=(10, 0),
            expected=Collision(t=0.9, x=9, y=5),
            id="face-center-hit",
        ),
    ],
)
def test_calculate_ball_paddle_collision(ball_xy, ball_vx_vy, paddle_y, expected):
    collision = calculate_ball_paddle_collision(
        ball_radius=1,
        ball_xy=ball_xy,
        ball_vx_vy=ball_vx_vy,
        paddle_xy=paddle_y,
        paddle_wh=(3, 10),
    )

    _assert_collision_equal(collision, expected)


def _field_collision_case(
    *,
    ball_xy: tuple[float, float],
    ball_vx_vy: tuple[float, float],
    expected: Collision | None,
    id: str,
):
    return pytest.param(ball_xy, ball_vx_vy, expected, id=id)


@pytest.mark.parametrize(
    ("ball_xy", "ball_vx_vy", "expected"),
    [
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(1, 0),
            expected=None,
            id="no-collision-horizontal",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(0, 1),
            expected=None,
            id="no-collision-vertical",
        ),
        _field_collision_case(
            ball_xy=(50, 2),
            ball_vx_vy=(0, -1),
            expected=Collision(t=1.0, x=50, y=1),
            id="hits-top",
        ),
        _field_collision_case(
            ball_xy=(50, 48),
            ball_vx_vy=(0, 1),
            expected=Collision(t=1.0, x=50, y=49),
            id="hits-bottom",
        ),
        _field_collision_case(
            ball_xy=(2, 25),
            ball_vx_vy=(-1, 0),
            expected=Collision(t=1.0, x=1, y=25),
            id="hits-left",
        ),
        _field_collision_case(
            ball_xy=(98, 25),
            ball_vx_vy=(1, 0),
            expected=Collision(t=1.0, x=99, y=25),
            id="hits-right",
        ),
        _field_collision_case(
            ball_xy=(50, 1),
            ball_vx_vy=(0, -1),
            expected=Collision(t=0.0, x=50, y=1),
            id="already-at-top",
        ),
        _field_collision_case(
            ball_xy=(50, 49),
            ball_vx_vy=(0, 1),
            expected=Collision(t=0.0, x=50, y=49),
            id="already-at-bottom",
        ),
        _field_collision_case(
            ball_xy=(1, 25),
            ball_vx_vy=(-1, 0),
            expected=Collision(t=0.0, x=1, y=25),
            id="already-at-left",
        ),
        _field_collision_case(
            ball_xy=(99, 25),
            ball_vx_vy=(1, 0),
            expected=Collision(t=0.0, x=99, y=25),
            id="already-at-right",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(0, -30),
            expected=Collision(t=0.8, x=50, y=1),
            id="fast-hit-top",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(0, 30),
            expected=Collision(t=0.8, x=50, y=49),
            id="fast-hit-bottom",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(-60, 0),
            expected=Collision(t=49 / 60, x=1, y=25),
            id="fast-hit-left",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(60, 0),
            expected=Collision(t=49 / 60, x=99, y=25),
            id="fast-hit-right",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(49, -24),
            expected=Collision(t=1.0, x=99, y=1),
            id="hits-top-right-corner",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(-49, -24),
            expected=Collision(t=1.0, x=1, y=1),
            id="hits-top-left-corner",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(49, 24),
            expected=Collision(t=1.0, x=99, y=49),
            id="hits-bottom-right-corner",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(-49, 24),
            expected=Collision(t=1.0, x=1, y=49),
            id="hits-bottom-left-corner",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(0, 0),
            expected=None,
            id="zero-velocity-no-collision",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(10, 0),
            expected=None,
            id="does-not-reach-right",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(-10, 0),
            expected=None,
            id="does-not-reach-left",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(0, 10),
            expected=None,
            id="does-not-reach-bottom",
        ),
        _field_collision_case(
            ball_xy=(50, 25),
            ball_vx_vy=(0, -10),
            expected=None,
            id="does-not-reach-top",
        ),
    ],
)
def test_calculate_ball_field_collision(
    ball_xy: tuple[float, float], ball_vx_vy: tuple[float, float], expected: Collision
):
    collision = calculate_ball_field_collision(
        ball_radius=1,
        ball_xy=ball_xy,
        ball_vx_vy=ball_vx_vy,
        field_wh=(100, 50),
    )

    _assert_collision_equal(collision, expected)
