import pytest

from ws_pong_lab.domain.game import (
    FinishedState,
    GameCommandNotAllowed,
    InProgressState,
    WaitingState,
)


class TestWaitingState:
    def test_start_game(self, make_game_context):
        ctx = make_game_context(state=WaitingState())

        ctx.start_game()

        assert isinstance(ctx.state, InProgressState)

    def test_paddles_moves(self, make_game_context):
        ctx = make_game_context(state=WaitingState())

        with pytest.raises(GameCommandNotAllowed):
            ctx.start_game()

    def reset_game(self, make_game_context):
        ctx = make_game_context(state=WaitingState())

        with pytest.raises(GameCommandNotAllowed):
            ctx.reset_game()


class TestInProgressState:
    def test_start_game(self, make_game_context):
        ctx = make_game_context(state=InProgressState())

        with pytest.raises(GameCommandNotAllowed):
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

        with pytest.raises(GameCommandNotAllowed):
            ctx.reset_game()


class TestFinishedState:
    def test_start_game(self, make_game_context):
        ctx = make_game_context(state=FinishedState())

        with pytest.raises(GameCommandNotAllowed):
            ctx.start_game()

    def test_paddle_moves(self, make_game_context):
        ctx = make_game_context(state=FinishedState())

        with pytest.raises(GameCommandNotAllowed):
            ctx.move_paddle(ctx.game.participants[0].id, 1)

    def reset_game(self, make_game_context):
        ctx = make_game_context(state=FinishedState())

        ctx.reset_game()

        assert isinstance(ctx.state, WaitingState)
