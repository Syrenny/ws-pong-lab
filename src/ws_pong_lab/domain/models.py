from enum import StrEnum
from typing import NewType, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field

BaseModelT = TypeVar("BaseModelT", bound=BaseModel)
PlayerId = NewType("PlayerId", str)


class Direction(StrEnum):
    UP = "up"
    DOWN = "down"


class PlayerSide(StrEnum):
    LEFT = "left"
    RIGHT = "right"


class Paddle(BaseModel):
    y: float = Field(gt=0.0)
    vy: float = Field(gt=0.0)
    width: int = Field(gt=0.0)
    height: int = Field(gt=0.0)


class Ball(BaseModel):
    x: float = Field(ge=0.0)
    y: float = Field(ge=0.0)
    vx: float
    vy: float
    radius: int = Field(gt=0)


class GameField(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    paddles: dict[PlayerSide, Paddle]
    ball: Ball


class GameStateId(StrEnum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


class GameRules(BaseModel):
    max_score: int = Field(gt=0)

    target_delta_time: float = Field(gt=0.0)


class Game(BaseModel):
    id: UUID
    state: GameStateId
    field: GameField
    score: dict[PlayerSide, int]
    sides: dict[PlayerSide, PlayerId | None]
    spectators: list[PlayerId]

    rules: GameRules

    @property
    def ball_xy(self) -> tuple[float, float]:
        return self.field.ball.x, self.field.ball.y

    @property
    def ball_vx_vy(self) -> tuple[float, float]:
        return self.field.ball.vx, self.field.ball.vy

    @property
    def field_wh(self) -> tuple[int, int]:
        return self.field.width, self.field.height
