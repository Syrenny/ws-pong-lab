from typing import Literal

import yaml  # type: ignore
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from .domain.models import BaseModelT


class RuntimeSettings(BaseSettings):
    env: Literal["dev", "prod"]


class UvicornConfig(BaseModel):
    host: str
    port: int
    workers: int
    reload: bool


class GameConfig(BaseModel):
    paddle_size: int
    paddle_x_padding: int

    field_size_x: int
    field_size_y: int

    ball_size: int

    speed_multiplier: float
    max_ball_speed: float


class Config(BaseModel):
    cors_allow_origins: list[str]

    game: GameConfig

    uvicorn: UvicornConfig


def load_from_yaml(file_path: str, model: type[BaseModelT]) -> BaseModelT:
    with open(file_path) as f:
        raw = yaml.safe_load(f)

    return model.model_validate(raw)


runtime = RuntimeSettings()

game_config = load_from_yaml("./config/game_config.yaml", GameConfig)
app_config = load_from_yaml(f"./config/config.{runtime.env}.yaml", Config)
