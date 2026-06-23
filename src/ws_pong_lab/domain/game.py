from __future__ import annotations

from typing import ClassVar, Never, override

from .errors import GameCommandNotAllowedError
from .models import Game, GameStateId, PlayerId


class GameContext:
    def __init__(self, game: Game, state: BaseState) -> None:
        self.transition_to(state)
        self._state = state
        self.game = game

    @property
    def state(self) -> BaseState:
        return self._state

    def transition_to(self, state: BaseState):
        self._state = state
        self._state.context = self

        self.game.state = self._state.state_id

    def start_game(self) -> Game:
        return self._state.start_game(game=self.game)

    def move_paddle(self, *, player_id: PlayerId, movement: int) -> Game:
        return self._state.move_paddle(
            game=self.game, player_id=player_id, movement=movement
        )

    def reset_game(self) -> Game:
        return self._state.reset_game(game=self.game)


class BaseState:
    state_id: ClassVar[GameStateId]

    @property
    def context(self) -> GameContext:
        return self._context

    @context.setter
    def context(self, context: GameContext) -> None:
        self._context = context

    def _raise_command_not_allowed(self, command: str) -> Never:
        raise GameCommandNotAllowedError(
            command=command, state=type(self.context._state).__name__
        )

    def start_game(self, game: Game) -> Game:
        self._raise_command_not_allowed("start_game")

    def move_paddle(self, *, game: Game, player_id: PlayerId, movement: int) -> Game:
        self._raise_command_not_allowed("move_paddle")

    def reset_game(self, game: Game) -> Game:
        self._raise_command_not_allowed("reset_game")


class WaitingState(BaseState):
    state_id = GameStateId.WAITING

    @override
    def start_game(self, game: Game) -> Game:
        self.context.transition_to(InProgressState())

        return self.context.game


class InProgressState(BaseState):
    state_id = GameStateId.IN_PROGRESS

    @override
    def move_paddle(self, *, game: Game, player_id: PlayerId, movement: int) -> None:
        pass


class FinishedState(BaseState):
    state_id = GameStateId.FINISHED

    @override
    def reset_game(self, game: Game) -> None:
        self.context.transition_to(WaitingState())


states_registry: dict[GameStateId, type[BaseState]] = {
    GameStateId.WAITING: WaitingState,
    GameStateId.IN_PROGRESS: InProgressState,
    GameStateId.FINISHED: FinishedState,
}
