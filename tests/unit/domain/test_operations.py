import pytest

from ws_pong_lab.domain.errors import GameCommandNotAllowedError
from ws_pong_lab.domain.models import Direction, GameStateId, PlayerSide
from ws_pong_lab.domain.operations import (
    advance_game,
    move_paddle,
    reset_game,
    start_game,
)


def __invalid_state_case(game_state: GameStateId, raises: type[Exception], id: str):
    return pytest.param(game_state, raises, id=id)


@pytest.mark.parametrize(
    ("game_state", "raises"),
    (
        __invalid_state_case(
            game_state=GameStateId.WAITING,
            raises=GameCommandNotAllowedError,
            id="raises-if-waiting-state",
        ),
        __invalid_state_case(
            game_state=GameStateId.FINISHED,
            raises=GameCommandNotAllowedError,
            id="raises-if-finished-state",
        ),
    ),
)
def test_advance_game_invalid_state(
    game_state: GameStateId, raises: type[Exception], default_game
):
    default_game.state = game_state

    with pytest.raises(raises):
        advance_game(default_game, delta_time=default_game.rules.target_delta_time)


@pytest.mark.parametrize(
    ("game_state", "raises"),
    (
        __invalid_state_case(
            game_state=GameStateId.IN_PROGRESS,
            raises=GameCommandNotAllowedError,
            id="raises-if-waiting-state",
        ),
        __invalid_state_case(
            game_state=GameStateId.FINISHED,
            raises=GameCommandNotAllowedError,
            id="raises-if-finished-state",
        ),
    ),
)
def test_start_game_invalid_state(
    game_state: GameStateId, raises: type[Exception], default_game
):
    default_game.state = game_state

    with pytest.raises(raises):
        start_game(default_game)


@pytest.mark.parametrize(
    ("game_state", "raises"),
    (
        __invalid_state_case(
            game_state=GameStateId.WAITING,
            raises=GameCommandNotAllowedError,
            id="raises-if-waiting-state",
        ),
        __invalid_state_case(
            game_state=GameStateId.FINISHED,
            raises=GameCommandNotAllowedError,
            id="raises-if-finished-state",
        ),
    ),
)
def test_move_paddle_invalid_state(
    game_state: GameStateId, raises: type[Exception], default_game
):
    default_game.state = game_state

    with pytest.raises(raises):
        move_paddle(game=default_game, side=PlayerSide.LEFT, direction=Direction.UP)


def test_move_paddle_moves_paddle(default_game):
    default_game.field.paddles[PlayerSide.LEFT].y = 15
    default_game.field.paddles[PlayerSide.LEFT].vy = 5
    default_game.state = GameStateId.IN_PROGRESS

    updated = move_paddle(
        game=default_game, side=PlayerSide.LEFT, direction=Direction.DOWN
    )

    assert updated.field.paddles[PlayerSide.LEFT].y == 20


def test_advance_game_not_raises_in_progress_state(default_game):
    default_game.state = GameStateId.IN_PROGRESS
    advance_game(default_game, default_game.rules.target_delta_time)


def test_start_game_transfers_to_in_progress_state(default_game):
    default_game.state = GameStateId.WAITING

    updated = start_game(game=default_game)

    assert updated.state is GameStateId.IN_PROGRESS


def test_reset_game_transfers_to_waiting_state(default_game):
    default_game.state = GameStateId.FINISHED

    updated = reset_game(game=default_game)

    assert updated.state is GameStateId.WAITING
