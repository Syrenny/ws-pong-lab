import pytest

from ws_pong_lab.domain.errors import GameCommandNotAllowedError
from ws_pong_lab.domain.game import (
    FinishedState,
    GameStateId,
    InProgressState,
    WaitingState,
)


class TestWaitingState:
    def test_start_game(self, make_game_context):
        ctx = make_game_context(state=WaitingState())

        ctx.start_game()

        assert ctx.game.state == GameStateId.IN_PROGRESS

    def test_paddles_moves(self, make_game_context):
        ctx = make_game_context(state=WaitingState())

        with pytest.raises(GameCommandNotAllowedError):
            ctx.start_game()

    def reset_game(self, make_game_context):
        ctx = make_game_context(state=WaitingState())

        with pytest.raises(GameCommandNotAllowedError):
            ctx.reset_game()


class TestInProgressState:
    def test_start_game(self, make_game_context):
        ctx = make_game_context(state=InProgressState())

        with pytest.raises(GameCommandNotAllowedError):
            ctx.start_game()

    @pytest.mark.parametrize(
        ["initial", "movement", "expected"],
        [(0, -1, 0), (50, -1, 49), (50, 1, 51), (99, 1, 99)],
    )
    def test_paddles_moves(self, initial, movement, expected, make_game_context):
        ctx = make_game_context(
            state=InProgressState(),
        )

        player_id_1 = ctx.game.participants[0].id

        # override initial
        ctx.game.field.paddles[player_id_1].y = initial

        ctx.move_paddle(player_id_1, movement)

        assert ctx.game.field.paddles[player_id_1].y == expected

    def reset_game(self, make_game_context):
        ctx = make_game_context(state=InProgressState())

        with pytest.raises(GameCommandNotAllowedError):
            ctx.reset_game()


class TestFinishedState:
    def test_start_game(self, make_game_context):
        ctx = make_game_context(state=FinishedState())

        with pytest.raises(GameCommandNotAllowedError):
            ctx.start_game()

    def test_paddle_moves(self, make_game_context):
        ctx = make_game_context(state=FinishedState())

        with pytest.raises(GameCommandNotAllowedError):
            ctx.move_paddle(ctx.game.participants[0].id, 1)

    def reset_game(self, make_game_context):
        ctx = make_game_context(state=FinishedState())

        ctx.reset_game()

        assert ctx.game.state == GameStateId.WAITING
        assert isinstance(ctx.state, WaitingState)
