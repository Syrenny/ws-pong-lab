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


class PlayerRole(StrEnum):
    PLAYER = "player"
    SPECTATOR = "spectator"


class GameField(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    paddles: dict[PlayerId, Paddle]
    ball: Ball


class Participant(BaseModel):
    id: PlayerId
    role: PlayerRole


class GameStateId(StrEnum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


class Game(BaseModel):
    id: UUID
    state: GameStateId
    field: GameField
    score: dict[PlayerId, int]
    participants: list[Participant]
