from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class Paddle(BaseModel):
    y: int


class Ball(BaseModel):
    x: int
    y: int


class Field(BaseModel):
    r_paddle: Paddle
    l_paddle: Paddle

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


class GameState(BaseModel):
    room: Room

    field: Field
