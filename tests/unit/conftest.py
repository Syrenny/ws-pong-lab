from pathlib import Path
from uuid import UUID

import pytest

from ws_pong_lab.domain.game import BaseState, GameContext
from ws_pong_lab.domain.models import (
    Ball,
    Game,
    GameField,
    GameStateId,
    Paddle,
    Participant,
    PlayerId,
    PlayerRole,
)
from ws_pong_lab.repository import GameRepo


@pytest.fixture
def default_game() -> Game:
    player_1 = PlayerId("player-1")
    player_2 = PlayerId("player-2")
    return Game(
        id=UUID("123e4567-e89b-12d3-a456-426655440000"),
        state=GameStateId.WAITING,
        field=GameField(
            width=100,
            height=100,
            paddles={
                player_1: Paddle(y=50, vy=5, width=5, height=10),
                player_2: Paddle(y=50, vy=5, width=5, height=10),
            },
            ball=Ball(x=50, y=50, radius=5, vx=5, vy=5),
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
def game_repo(storage_dir):
    return GameRepo(storage_dir=storage_dir)


@pytest.fixture
def make_game_context(default_game):
    def factory(*, state: BaseState):
        return GameContext(game=default_game, state=state)

    return factory
