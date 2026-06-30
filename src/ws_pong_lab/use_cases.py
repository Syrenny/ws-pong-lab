from uuid import UUID

from ws_pong_lab.domain import factories, operations
from ws_pong_lab.domain.models import Direction, Game, PlayerId, PlayerSide
from ws_pong_lab.repository import GameRepoProtocol


class UseCaseError(ValueError):
    pass


class GameNotFoundError(UseCaseError):
    pass


async def game_scheduler_tick(game_id: UUID, repo: GameRepoProtocol) -> Game:
    game = await repo.get_by_id(game_id=game_id)

    if game is None:
        raise GameNotFoundError

    updated = operations.advance_game(
        game=game, delta_time=game.rules.target_delta_time
    )

    return await repo.create_or_update(updated)


async def move_paddle(
    game_id: UUID,
    repo: GameRepoProtocol,
    direction: Direction,
    side: PlayerSide,
) -> Game:
    game = await repo.get_by_id(game_id)

    if game is None:
        raise GameNotFoundError

    updated = operations.move_paddle(game=game, side=side, direction=direction)

    return await repo.create_or_update(updated)


async def start_game(game_id: UUID, repo: GameRepoProtocol) -> Game:
    game = await repo.get_by_id(game_id)

    updated = operations.start_game(game)

    return await repo.create_or_update(updated)


async def create_game(
    repo: GameRepoProtocol,
    left_player_id: PlayerId | None,
    right_player_id: PlayerId | None,
) -> Game:
    game = factories.build_initial_game(
        left_player_id=left_player_id, right_player_id=right_player_id
    )
