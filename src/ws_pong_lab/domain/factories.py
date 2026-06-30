from uuid import uuid4

from .models import (
    Ball,
    Game,
    GameField,
    GameRules,
    GameStateId,
    Paddle,
    PlayerId,
    PlayerSide,
)


def build_initial_game(
    left_player_id: PlayerId,
    right_player_id: PlayerId,
    field_wh: tuple[int, int],
    paddle_vy: float,
    paddle_wh: tuple[int, int],
    ball_vx_vy: tuple[float, float],
    ball_radius: int,
    rules: GameRules,
) -> Game:
    if left_player_id == right_player_id:
        raise ValueError("Players must be different and at least one not None")

    field_width, field_height = field_wh
    paddle_width, paddle_height = paddle_wh
    ball_vx, ball_vy = ball_vx_vy

    return Game(
        id=uuid4(),
        state=GameStateId.WAITING,
        field=GameField(
            width=field_width,
            height=field_height,
            paddles={
                PlayerSide.LEFT: Paddle(
                    y=field_height // 2,
                    vy=paddle_vy,
                    width=paddle_width,
                    height=paddle_height,
                ),
                PlayerSide.RIGHT: Paddle(
                    y=field_height // 2,
                    vy=paddle_vy,
                    width=paddle_width,
                    height=paddle_height,
                ),
            },
            ball=Ball(
                x=field_width / 2,
                y=field_height / 2,
                vx=ball_vx,
                vy=ball_vy,
                radius=ball_radius,
            ),
        ),
        score={PlayerSide.LEFT: 0, PlayerSide.RIGHT: 0},
        sides={PlayerSide.LEFT: left_player_id, PlayerSide.RIGHT: right_player_id},
        spectators=[],
        rules=rules,
    )
