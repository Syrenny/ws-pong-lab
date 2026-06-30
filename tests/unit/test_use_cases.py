from uuid import UUID

import pytest

from tests.unit.fakes import FakeGameRepo
from ws_pong_lab import use_cases
from ws_pong_lab.domain.models import Direction, GameStateId, PlayerId, PlayerSide
from ws_pong_lab.use_cases import (
    GameNotFoundError,
)


async def test_game_scheduler_tick_saves_game(default_game, fake_game_repo):
    fake_game_repo.game.state = GameStateId.IN_PROGRESS

    game = await use_cases.game_scheduler_tick(
        game_id=default_game.id, repo=fake_game_repo
    )

    assert fake_game_repo.game == game


async def test_game_scheduler_tick_raises_no_game(fake_game_repo):
    with pytest.raises(GameNotFoundError):
        await use_cases.game_scheduler_tick(
            game_id=UUID("e3143d5d-061c-4a89-9ce5-22dcccaabefb"), repo=fake_game_repo
        )


async def test_game_scheduler_tick_advances_game(default_game, fake_game_repo):
    fake_game_repo.game.state = GameStateId.IN_PROGRESS

    updated = await use_cases.game_scheduler_tick(
        game_id=default_game.id, repo=fake_game_repo
    )

    assert updated.field.ball.x != default_game.field.ball.x
    assert fake_game_repo.game == updated


async def test_move_paddle_moves_paddle(default_game, fake_game_repo):
    fake_game_repo.game.state = GameStateId.IN_PROGRESS

    updated = await use_cases.move_paddle(
        game_id=default_game.id,
        repo=fake_game_repo,
        direction=Direction.UP,
        side=PlayerSide.LEFT,
    )

    assert (
        updated.field.paddles[PlayerSide.LEFT].y
        == default_game.field.paddles[PlayerSide.LEFT].y
        - default_game.field.paddles[PlayerSide.LEFT].vy
    )


async def test_move_paddle_raises_no_game(fake_game_repo):
    with pytest.raises(GameNotFoundError):
        await use_cases.move_paddle(
            game_id=UUID("e3143d5d-061c-4a89-9ce5-22dcccaabefb"),
            repo=fake_game_repo,
            direction=Direction.UP,
            side=PlayerSide.LEFT,
        )


async def test_move_paddle_saves_game(default_game, fake_game_repo):
    fake_game_repo.game.state = GameStateId.IN_PROGRESS

    game = await use_cases.move_paddle(
        game_id=default_game.id,
        repo=fake_game_repo,
        direction=Direction.UP,
        side=PlayerSide.LEFT,
    )

    assert fake_game_repo.game == game


async def test_start_game_transfers_game_state(default_game, fake_game_repo):
    fake_game_repo.game.state = GameStateId.WAITING

    updated = await use_cases.start_game(game_id=default_game.id, repo=fake_game_repo)

    assert updated.state is GameStateId.IN_PROGRESS


async def test_start_game_saves_game(default_game, fake_game_repo):
    fake_game_repo.game.state = GameStateId.WAITING

    updated = await use_cases.start_game(game_id=default_game.id, repo=fake_game_repo)

    assert fake_game_repo.game == updated


@pytest.fixture
def valid_create_game_params():
    return {
        "left_player_id": PlayerId("left_player"),
        "right_player_id": PlayerId("right_player"),
    }


async def test_create_game_saves_game(
    fake_empty_game_repo: FakeGameRepo, valid_create_game_params: dict
):
    valid_create_game_params["repo"] = fake_empty_game_repo

    assert fake_empty_game_repo.game is None

    game = await use_cases.create_game(**fake_empty_game_repo)

    assert fake_empty_game_repo.game is not None
    assert fake_empty_game_repo.game.id == game.id


async def test_create_game_reads_game_settings(fake_empty_game_repo: FakeGameRepo, valid_create_game_params: dict):
    valid_create_game_params["repo"] = fake_empty_game_repo
    
    game = await use_cases.create_game(**valid_create_game_params)
    
    assert game.
