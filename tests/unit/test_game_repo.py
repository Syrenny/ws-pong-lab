from uuid import UUID


async def test_get_game_repo_contains_fields(default_game, game_repo):
    await game_repo.create_or_update(default_game)

    game = await game_repo.get_by_id(default_game.id)

    participant_1 = game.participants[0]
    participant_2 = game.participants[1]

    assert isinstance(game.id, UUID)
    assert isinstance(game.participants, list)
    assert isinstance(participant_1.id, str)
    assert isinstance(participant_2.id, str)
    assert isinstance(participant_1.role, str)
    assert isinstance(participant_2.role, str)
    assert isinstance(game.field.ball.x, int)
    assert isinstance(game.field.ball.y, int)
    assert isinstance(game.field.paddles[participant_1.id].y, int)
    assert isinstance(game.field.paddles[participant_2.id].y, int)
    assert isinstance(game.score[participant_1.id], int)
    assert isinstance(game.score[participant_2.id], int)


async def test_game_state_creates_game_directory(default_game, game_repo, storage_dir):
    await game_repo.create_or_update(default_game)

    assert storage_dir.exists()


async def test_get_non_existent_game_state(game_repo):
    _game = await game_repo.get_by_id("00000000-0000-0000-0000-000000000000")

    assert _game is None


async def test_get_after_delete(default_game, game_repo):
    await game_repo.create_or_update(default_game)

    assert await game_repo.get_by_id(default_game.id) is not None

    await game_repo.delete_by_id(default_game.id)

    assert await game_repo.get_by_id(default_game.id) is None


async def test_after_delete_path_not_exists(default_game, game_repo, storage_dir):
    await game_repo.create_or_update(default_game)

    game_state_path = storage_dir / str(default_game.id) / "game.json"

    assert game_state_path.exists()

    await game_repo.delete_by_id(default_game.id)

    assert not game_state_path.exists()
