import pytest

from ws_pong_lab.domain.game import GameCommandNotAllowed, WaitingState
from ws_pong_lab.domain.models import PlayerSide


class TestWaitingState:
    def test_start_game(self, make_game_context):
        ctx = make_game_context(state=WaitingState())

        with pytest.raises(GameCommandNotAllowed):
            ctx.start_game()

    @pytest.mark.parametrize(
        ["initial", "movement", "expected"],
        [(0, -1, 0), (50, -1, 49), (50, 1, 51), (99, 1, 99), ()],
    )
    def test_paddles_moves(self, initial, movement, expected, make_game_context, gs_repo, make_game):
        
        for player_side in [PlayerSide.LEFT, PlayerSide.RIGHT]:
            ctx = make_game_context(state=WaitingState(), game=make_game(field=(100, 100)), paddles=(initial, 50))
            
            ctx.move_paddle(
                player_side,
            )
            
            assert 


class TestInProgressState:
    def test_start_game(self, in_progress_context):
        pass

    def test_paddle_moves(self, in_progress_context):
        pass


class TestFinishedState:
    def test_start_game(self, finished_context):
        pass

    def test_paddle_moves(self, finished_context):
        pass
