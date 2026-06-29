import pytest

from ws_pong_lab.domain.models import Ball, GameStateId, PlayerSide
from ws_pong_lab.domain.simulation import simulate_tick


def test_simulate_tick_moves_ball_without_collision(default_game) -> None:
    default_game.field.ball = Ball(x=50, y=25, vx=1, vy=0, radius=1)

    updated_game = simulate_tick(
        game=default_game, delta_time=default_game.rules.target_delta_time
    )

    assert (updated_game.field.ball.x, updated_game.field.ball.y) == pytest.approx(
        (
            50 + default_game.rules.target_delta_time * default_game.ball_vx_vy[0],
            25 + default_game.rules.target_delta_time * default_game.ball_vx_vy[1],
        )
    )
    assert (updated_game.field.ball.vx, updated_game.field.ball.vy) == pytest.approx(
        (1, 0)
    )


def test_simulate_tick_goal_changes_score(default_game) -> None:
    default_game.field.ball = Ball(x=99, y=25, vx=1, vy=0, radius=1)
    default_game.score[PlayerSide.LEFT] = 0

    updated_game = simulate_tick(
        game=default_game, delta_time=default_game.rules.target_delta_time
    )

    assert updated_game.score[PlayerSide.LEFT] == 1


def test_simulate_tick_ball_bounces(default_game) -> None:
    default_game.field.ball = Ball(x=50, y=49, vx=1, vy=1, radius=1)

    updated_game = simulate_tick(
        game=default_game, delta_time=default_game.rules.target_delta_time
    )

    assert updated_game.field.ball.vy == -1


def test_simulate_tick_ends_up_game(default_game) -> None:
    default_game.score[PlayerSide.LEFT] = 10
    default_game.rules.max_score = 10
    default_game.state = GameStateId.IN_PROGRESS

    updated_game = simulate_tick(
        game=default_game, delta_time=default_game.rules.target_delta_time
    )

    assert updated_game.state is GameStateId.FINISHED
