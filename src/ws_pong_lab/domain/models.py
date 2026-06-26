from enum import StrEnum
from typing import NewType, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field

BaseModelT = TypeVar("BaseModelT", bound=BaseModel)
PlayerId = NewType("PlayerId", str)


class Direction(StrEnum):
    UP = "up"
    DOWN = "down"


class Paddle(BaseModel):
    y: float = Field(gt=0.0)
    vy: float = Field(gt=0.0)
    width: float = Field(gt=0.0)
    height: float = Field(gt=0.0)


class Ball(BaseModel):
    x: float = Field(ge=0.0)
    y: float = Field(ge=0.0)
    vx: float
    vy: float
    radius: float = Field(gt=0.0)


class GameField(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    paddles: dict[PlayerId, Paddle]
    ball: Ball


class PlayerSide(StrEnum):
    LEFT = "left"
    RIGHT = "right"


class GameStateId(StrEnum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


class GameRules(BaseModel):
    max_score: int = Field(gt=0)


class Game(BaseModel):
    id: UUID
    state: GameStateId
    field: GameField
    score: dict[PlayerSide, int] = {PlayerSide.LEFT: 0, PlayerSide.RIGHT: 0}
    sides: dict[PlayerSide, PlayerId | None] = {
        PlayerSide.LEFT: None,
        PlayerSide.RIGHT: None,
    }
    spectators: list[PlayerId]

    rules: GameRules
