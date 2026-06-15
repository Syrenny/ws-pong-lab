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
    PlayerId,
    PlayerRole,
)
from ws_pong_lab.repository import GameRepo


@pytest.fixture
def make_player_id():
    def factory(nickname: str) -> PlayerId:
        return PlayerId(nickname=nickname)

    return factory


@pytest.fixture
def make_default_game():
    player_1 = PlayerId(nickname="player-1")
    player_2 = PlayerId(nickname="player-2")
    return Game(
        id=UUID("123e4567-e89b-12d3-a456-426655440000"),
        field=GameField(
            x=100,
            y=100,
            paddles={player_1: Paddle(y=50), player_2: Paddle(y=50)},
            ball=Ball(x=50, y=50),
        ),
        score={
            player_1: 0,
            player_2: 0,
        },
        participants=[
            Participant(id=player_1, role=PlayerRole.PLAYER),
            Participant(id=player_2, role=PlayerRole.PLAYER),
        ],
    )


@pytest.fixture
def storage_dir() -> Path:
    return Path("/tmp/test_game_repo")


@pytest.fixture
def gs_repo(storage_dir):
    return GameRepo(storage_dir=storage_dir)


@pytest.fixture
def make_game_context(make_default_game):
    def factory(*, state: GameState, game: Game | None = None):
        if game is None:
            game = make_default_game()
        return GameContext(game=game, state=state)

    return factory
