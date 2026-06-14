from uuid import UUID

from ws_pong_lab.domain.models import PlayerSide


async def test_get_game_repo_contains_fields(make_game, gs_repo):
    gs = make_game()
    await gs_repo.create_or_update(gs)

    gs = await gs_repo.get_by_id(gs.room.id)

    assert isinstance(gs.room.id, UUID)
    assert isinstance(gs.room.participants, list)
    assert isinstance(gs.room.participants[0].nickname, str)
    assert isinstance(gs.room.participants[0].role, str)
    assert isinstance(gs.field.ball.x, int)
    assert isinstance(gs.field.ball.y, int)
    assert isinstance(gs.field.paddles[PlayerSide.RIGHT].y, int)
    assert isinstance(gs.field.paddles[PlayerSide.LEFT].y, int)
    assert isinstance(gs.score[PlayerSide.RIGHT], int)
    assert isinstance(gs.score[PlayerSide.LEFT], int)


async def test_game_state_creates_room_directory(make_game, gs_repo, storage_dir):
    await gs_repo.create_or_update(make_game())

    assert storage_dir.exists()


async def test_get_non_existent_game_state(gs_repo):
    _gs = await gs_repo.get_by_id("00000000-0000-0000-0000-000000000000")

    assert _gs is None


async def test_get_after_delete(make_game, gs_repo):
    gs = make_game()
    await gs_repo.create_or_update(gs)

    assert await gs_repo.get_by_id(gs.room.id) is not None

    await gs_repo.delete_by_id(gs.room.id)

    assert await gs_repo.get_by_id(gs.room.id) is None


async def test_after_delete_path_not_exists(make_game, gs_repo, storage_dir):
    gs = make_game()
    await gs_repo.create_or_update(gs)

    game_state_path = storage_dir / str(gs.room.id) / "game_state.json"

    assert game_state_path.exists()

    await gs_repo.delete_by_id(gs.room.id)

    assert not game_state_path.exists()
