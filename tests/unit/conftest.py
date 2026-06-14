from pathlib import Path
from uuid import UUID

import pytest

from ws_pong_lab.domain.game import GameContext, GameState
from ws_pong_lab.domain.models import (
    Ball,
    Game,
    GameField,
    Paddle,
    Participant,
    PlayerRole,
    PlayerSide,
    Room,
)
from ws_pong_lab.repository import GameRepo


@pytest.fixture
def make_game():
    def factory(
        field: tuple[int, int] = (100, 100),
        ball: tuple[int, int] = (50, 50),
        l_paddle: int = 50,
        r_paddle: int = 50,
        room_id: UUID = UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
        participants: list[Participant] | None = None,
    ) -> Game:
        if participants is None:
            left = Participant(nickname="left", role=PlayerRole.LEFT)
            right = Participant(nickname="right", role=PlayerRole.RIGHT)

            participants = [left, right]

        room = Room(id=room_id, participants=participants)

        return Game(
            room=room,
            field=GameField(
                x=field[0],
                y=field[1],
                paddles={
                    PlayerSide.LEFT: Paddle(y=l_paddle),
                    PlayerSide.RIGHT: Paddle(y=r_paddle),
                },
                ball=Ball(x=ball[0], y=ball[1]),
            ),
            score={PlayerSide.LEFT: 0, PlayerSide.RIGHT: 0},
        )

    return factory


@pytest.fixture
def storage_dir() -> Path:
    return Path("/tmp/test_game_repo")


@pytest.fixture
def gs_repo(storage_dir):
    return GameRepo(storage_dir=storage_dir)


@pytest.fixture
def make_game_context(make_game):
    def factory(*, state: GameState, game: Game | None = None):
        if game is None:
            game = make_game()
        return GameContext(game=game, state=state)

    return factory
