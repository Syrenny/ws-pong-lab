from models import GameState


class GameStateRepo:
    path_template = ""

    @classmethod
    async def create_or_update(cls, game_state: GameState) -> GameState:
        return NotImplemented

    @classmethod
    async def delete(cls, room_id) -> GameState:
        return NotImplemented
