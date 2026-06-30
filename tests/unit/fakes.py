from uuid import UUID

from ws_pong_lab.domain.models import (
    Game,
)
from ws_pong_lab.repository import GameRepoProtocol


class FakeGameRepo(GameRepoProtocol):
    def __init__(self, game: Game | None) -> None:
        self.game = game

    async def create_or_update(self, game: Game) -> Game:
        self.game = game

        return self.game

    async def get_by_id(self, game_id: UUID) -> Game | None:
        if not self.game or game_id != self.game.id:
            return None

        return self.game

    async def delete_by_id(self, game_id: UUID) -> None:
        if not self.game or game_id != self.game.id:
            return None

        self.game = None
