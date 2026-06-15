from dataclasses import dataclass
from enum import StrEnum
from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel

BaseModelT = TypeVar("BaseModelT", bound=BaseModel)


class Paddle(BaseModel):
    y: int


class Ball(BaseModel):
    x: int
    y: int


class PlayerRole(StrEnum):
    PLAYER = "player"
    SPECTATOR = "spectator"


@dataclass(frozen=True)
class PlayerId:
    nickname: str


class GameField(BaseModel):
    x: int
    y: int
    paddles: dict[PlayerId, Paddle]
    ball: Ball


class Participant(BaseModel):
    id: PlayerId
    role: PlayerRole


class Game(BaseModel):
    id: UUID
    field: GameField
    score: dict[PlayerId, int]
    participants: list[Participant]
