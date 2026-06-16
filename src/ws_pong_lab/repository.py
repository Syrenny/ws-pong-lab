from pathlib import Path
from uuid import UUID

import aiofiles
from aiofiles.os import makedirs, remove
from pydantic import BaseModel

from ws_pong_lab.domain.models import BaseModelT, Game


async def _asave_model(path: Path, model: BaseModel) -> None:
    json_data = model.model_dump_json()

    await makedirs(path.parent, exist_ok=True)

    async with aiofiles.open(path, "w", encoding="utf-8") as file:
        await file.write(json_data)


async def _aload_model(path: Path, model_type: type[BaseModelT]) -> BaseModelT | None:
    try:
        async with aiofiles.open(path, encoding="utf-8") as file:
            json_data = await file.read()
    except FileNotFoundError:
        return None

    return model_type.model_validate_json(json_data)


async def _adelete(path: Path) -> None:
    try:
        await remove(path)
    except FileNotFoundError:
        return


class GameRepo:
    def __init__(self, storage_dir: Path) -> None:
        self.storage_dir = storage_dir

    def _get_game_path(self, game_id: UUID) -> Path:
        return self.storage_dir / str(game_id) / "game.json"

    async def create_or_update(self, game_state: Game) -> Game:
        path = self._get_game_path(game_state.id)

        await _asave_model(path, game_state)

        return game_state

    async def get_by_id(self, game_id: UUID) -> Game | None:
        path = self._get_game_path(game_id)

        return await _aload_model(path, Game)

    async def delete_by_id(self, game_id: UUID) -> None:
        path = self._get_game_path(game_id)

        await _adelete(path)
