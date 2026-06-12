from pathlib import Path
from uuid import UUID

from ws_pong_lab.models import GameState


class GameStateRepo:
    def __init__(self, storage_dir: Path) -> None:
        self.storage_dir = storage_dir

    def _get_room_path(self, room_id: UUID) -> Path:
        return self.storage_dir / str(room_id)

    def _get_game_state_path(self, room_id: UUID) -> Path:
        return self._get_room_path(room_id) / "game_state.json"

    def _ensure_room_path(self, room_id: UUID) -> Path:
        room_path = self._get_room_path(room_id)
        room_path.mkdir(parents=True, exist_ok=True)

        return room_path

    async def create_or_update(self, game_state: GameState) -> GameState:
        self._ensure_room_path(game_state.room.id)
        gs_path = self._get_game_state_path(game_state.room.id)

        json_data = game_state.model_dump_json()
        gs_path.write_text(json_data, encoding="utf-8")

        return game_state

    async def get(self, room_id: UUID) -> GameState | None:
        gs_path = self._get_game_state_path(room_id)

        json_data = gs_path.read_text(encoding="utf-8")

        if not json_data:
            return None

        return GameState.model_validate_json(json_data)

    async def delete_by_id(self, room_id: UUID) -> None:
        gs_path = self._get_game_state_path(room_id)

        gs_path.unlink(missing_ok=True)
