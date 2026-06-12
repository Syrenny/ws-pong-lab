from pathlib import Path
from uuid import UUID

import pytest

from ws_pong_lab.models import (
    Ball,
    Field,
    GameState,
    Paddle,
    Participant,
    PlayerRole,
    Room,
)
from ws_pong_lab.repository import GameStateRepo


@pytest.fixture
async def gs():
    left = Participant(nickname="left", role=PlayerRole.LEFT)
    right = Participant(nickname="right", role=PlayerRole.RIGHT)

    room = Room(
        id=UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"), participants=[left, right]
    )

    l_paddle = Paddle(y=0)
    r_paddle = Paddle(y=0)

    ball = Ball(x=0, y=0)
    field = Field(r_paddle=r_paddle, l_paddle=l_paddle, ball=ball)

    return GameState(room=room, field=field)


@pytest.fixture
def storage_dir() -> Path:
    return Path("/tmp/test_game_repo")


@pytest.fixture
def gs_repo(storage_dir):
    return GameStateRepo(storage_dir=storage_dir)


async def test_get_game_repo_contains_fields(gs, gs_repo):
    await gs_repo.create_or_update(gs)

    gs = await gs_repo.get(gs.room.id)

    assert isinstance(gs.room.id, UUID)
    assert isinstance(gs.room.participants, list)
    assert isinstance(gs.room.participants[0].nickname, str)
    assert isinstance(gs.room.participants[0].role, str)
    assert isinstance(gs.field.ball.x, int)
    assert isinstance(gs.field.ball.y, int)
    assert isinstance(gs.field.r_paddle.y, int)
    assert isinstance(gs.field.l_paddle.y, int)
    assert isinstance(gs.field.l_paddle.y, int)


async def test_game_state_creates_room_directory(gs, gs_repo, storage_dir):
    await gs_repo.create_or_update(gs)

    assert storage_dir.exists()


async def test_get_non_existent_game_state(gs_repo):
    _gs = await gs_repo.get("00000000-0000-0000-0000-000000000000")

    assert _gs is None


async def test_get_after_delete(gs, gs_repo):
    await gs_repo.create_or_update(gs)

    assert gs_repo.get(gs.room.id) is not None

    assert await gs_repo.delete_by_id(gs.room.id)

    assert gs_repo.get(gs.room.id) is None


async def test_after_delete_path_not_exists(gs, gs_repo, storage_dir):
    await gs_repo.create_or_update(gs)

    room_path = storage_dir / str(gs.room.id)

    assert room_path.exists()

    await gs_repo.delete_by_id(gs.room.id)

    assert not room_path.exists()
