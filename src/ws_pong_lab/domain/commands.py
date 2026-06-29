from functools import wraps

from .collision import calculate_next_paddle_y
from .errors import GameCommandNotAllowedError
from .models import Direction, Game, GameStateId, PlayerSide
from .simulation import simulate_tick


def require_states(*allowed: GameStateId):
    def decorator(func):
        @wraps(func)
        def wrapper(game: Game, *args, **kwargs):
            if game.state not in allowed:
                raise GameCommandNotAllowedError()

            return func(game, *args, **kwargs)

        return wrapper

    return decorator


@require_states(GameStateId.IN_PROGRESS)
def tick_game(game: Game, delta_time: float) -> Game:
    return simulate_tick(game=game, delta_time=delta_time)


@require_states(GameStateId.WAITING)
def start_game(game: Game) -> Game:
    return game.model_copy(update={"state": GameStateId.IN_PROGRESS})


@require_states(GameStateId.IN_PROGRESS)
def move_paddle(game: Game, side: PlayerSide, direction: Direction) -> Game:
    updated = game.model_copy(deep=True)

    paddle = game.field.paddles[side]

    next_y = calculate_next_paddle_y(
        paddle_y=paddle.y,
        paddle_height=paddle.height,
        paddle_vy=paddle.vy,
        direction=direction,
        field_height=game.field.height,
    )

    updated.field.paddles[side].y = next_y

    return updated


@require_states(GameStateId.FINISHED)
def reset_game(game: Game) -> Game:
    return game.model_copy(update={"state": GameStateId.WAITING})
