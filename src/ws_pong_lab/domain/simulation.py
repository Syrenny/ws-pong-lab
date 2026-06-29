from .collision import (
    WallSide,
    calculate_ball_horizontal_wall_collision,
    calculate_ball_motion_after_goal,
    calculate_ball_motion_without_collision,
    calculate_ball_speed_after_horizontal_wall_collision,
    calculate_ball_vertical_wall_collision,
)
from .models import Game, GameStateId, PlayerSide
from .scoring import award_goal, find_winner


def _handle_vertical_wall_collision(game: Game, wall_side: WallSide) -> Game:
    ball_motion = calculate_ball_motion_after_goal(
        ball_vx_vy=game.ball_vx_vy,
        field_wh=game.field_wh,
    )
    ball = game.field.ball.model_copy(
        update={
            "x": ball_motion.ball_xy[0],
            "y": ball_motion.ball_xy[1],
            "vx": ball_motion.ball_vx_vy[0],
            "vy": ball_motion.ball_vx_vy[1],
        }
    )

    field = game.field.model_copy(update={"ball": ball})

    left_score, right_score = award_goal(
        score=(game.score[PlayerSide.LEFT], game.score[PlayerSide.RIGHT]),
        goal_side=wall_side,
    )

    score = {PlayerSide.LEFT: left_score, PlayerSide.RIGHT: right_score}

    return game.model_copy(update={"field": field, "score": score})


def _handle_horizontal_wall_collision(game: Game) -> Game:
    ball_vx, ball_vy = calculate_ball_speed_after_horizontal_wall_collision(
        ball_vx_vy=game.ball_vx_vy
    )

    ball = game.field.ball.model_copy(
        update={
            "vx": ball_vx,
            "vy": ball_vy,
        }
    )

    field = game.field.model_copy(update={"ball": ball})

    return game.model_copy(update={"field": field})


def _move_ball_without_collision(game: Game, delta_time: float) -> Game:
    ball_motion = calculate_ball_motion_without_collision(
        ball_xy=game.ball_xy,
        ball_vx_vy=game.ball_vx_vy,
        field_wh=game.field_wh,
        ball_radius=game.field.ball.radius,
        delta_time=delta_time,
    )
    ball = game.field.ball.model_copy(
        update={
            "x": ball_motion.ball_xy[0],
            "y": ball_motion.ball_xy[1],
            "vx": ball_motion.ball_vx_vy[0],
            "vy": ball_motion.ball_vx_vy[1],
        }
    )

    field = game.field.model_copy(update={"ball": ball})

    return game.model_copy(update={"field": field})


def _finish_game_if_winner_found(game: Game) -> Game:
    state = game.state
    winner = find_winner(score=game.score, max_score=game.rules.max_score)
    if winner:
        state = GameStateId.FINISHED

    return game.model_copy(update={"state": state})


def simulate_tick(game: Game, delta_time: float) -> Game:
    cases = []

    vertical_wall_collision = calculate_ball_vertical_wall_collision(
        ball_radius=game.field.ball.radius,
        ball_xy=game.ball_xy,
        ball_vx_vy=game.ball_vx_vy,
        field_wh=game.field_wh,
    )
    if vertical_wall_collision:
        cases.append(
            (
                vertical_wall_collision.collision.t,
                lambda game: _handle_vertical_wall_collision(
                    game=game, wall_side=vertical_wall_collision.side
                ),
            )
        )

    horizontal_wall_collision = calculate_ball_horizontal_wall_collision(
        ball_radius=game.field.ball.radius,
        ball_xy=game.ball_xy,
        ball_vx_vy=game.ball_vx_vy,
        field_wh=game.field_wh,
    )
    if horizontal_wall_collision:
        cases.append(
            (
                horizontal_wall_collision.collision.t,
                lambda game: _handle_horizontal_wall_collision(game=game),
            )
        )

    t, handler = min(cases, key=lambda value: value[0])

    if t > delta_time:
        game = _move_ball_without_collision(game=game, delta_time=delta_time)
    else:
        game = handler(game=game)

    game = _finish_game_if_winner_found(game=game)

    return game
