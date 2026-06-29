from pathlib import Path
from uuid import UUID

import pytest

from ws_pong_lab.domain.models import (
    Ball,
    Game,
    GameField,
    GameRules,
    GameStateId,
    Paddle,
    PlayerId,
    PlayerSide,
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
            height=50,
            paddles={
                PlayerSide.LEFT: Paddle(y=25, vy=2, width=2, height=5),
                PlayerSide.RIGHT: Paddle(y=25, vy=2, width=2, height=5),
            },
            ball=Ball(x=50, y=25, radius=2, vx=5, vy=5),
        ),
        score={
            PlayerSide.LEFT: 0,
            PlayerSide.RIGHT: 0,
        },
        sides={PlayerSide.LEFT: player_1, PlayerSide.RIGHT: player_2},
        spectators=[],
        rules=GameRules(max_score=10, target_delta_time=60 / 100),
    )


@pytest.fixture
def storage_dir() -> Path:
    return Path("/tmp/test_game_repo")


@pytest.fixture
def game_repo(storage_dir):
    return GameRepo(storage_dir=storage_dir)
