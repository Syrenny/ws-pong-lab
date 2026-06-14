from enum import StrEnum
from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel

BaseModelT = TypeVar("BaseModelT", bound=BaseModel)


class PlayerSide(StrEnum):
    LEFT = "left"
    RIGHT = "right"


class Paddle(BaseModel):
    y: int


class Ball(BaseModel):
    x: int
    y: int


class GameField(BaseModel):
    x: int
    y: int
    
    paddles: dict[PlayerSide, Paddle]

    ball: Ball


class PlayerRole(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    SPECTATOR = "spectator"


class Participant(BaseModel):
    nickname: str
    role: PlayerRole


class Room(BaseModel):
    id: UUID

    participants: list[Participant]


class Game(BaseModel):
    room: Room

    field: GameField

    score: dict[PlayerSide, int]
