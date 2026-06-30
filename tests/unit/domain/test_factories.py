from uuid import UUID

import pytest

from ws_pong_lab.domain import factories
from ws_pong_lab.domain.models import GameRules, GameStateId, PlayerId, PlayerSide


@pytest.fixture
def valid_build_game_params():
    return {
        "left_player_id": PlayerId("left_player"),
        "right_player_id": PlayerId("right_player"),
        "field_wh": (100, 50),
        "paddle_vy": 3.5,
        "paddle_wh": (2, 5),
        "ball_vx_vy": (0.7, 0.01),
        "ball_radius": 1,
        "rules": GameRules(max_score=10, target_delta_time=0.5),
    }


def test_build_initial_game(valid_build_game_params):
    left_player_id = valid_build_game_params["left_player_id"]
    right_player_id = valid_build_game_params["right_player_id"]

    field_width, field_height = valid_build_game_params["field_wh"]

    paddle_width, paddle_height = valid_build_game_params["paddle_wh"]
    paddle_vy = valid_build_game_params["paddle_vy"]

    ball_vx, ball_vy = valid_build_game_params["ball_vx_vy"]
    ball_radius = valid_build_game_params["ball_radius"]

    rules = valid_build_game_params["rules"]

    game = factories.build_initial_game(**valid_build_game_params)

    assert game.sides[PlayerSide.LEFT] == left_player_id
    assert game.sides[PlayerSide.RIGHT] == right_player_id

    assert game.score[PlayerSide.LEFT] == game.score[PlayerSide.RIGHT] == 0

    assert isinstance(game.id, UUID)

    assert game.state is GameStateId.WAITING

    assert game.field.width == field_width
    assert game.field.height == field_height

    assert game.field.paddles[PlayerSide.LEFT].y == field_height // 2
    assert game.field.paddles[PlayerSide.RIGHT].y == field_height // 2

    assert game.field.paddles[PlayerSide.LEFT].vy == paddle_vy
    assert game.field.paddles[PlayerSide.RIGHT].vy == paddle_vy

    assert game.field.paddles[PlayerSide.LEFT].width == paddle_width
    assert game.field.paddles[PlayerSide.LEFT].height == paddle_height
    assert game.field.paddles[PlayerSide.RIGHT].width == paddle_width
    assert game.field.paddles[PlayerSide.RIGHT].height == paddle_height

    assert len(game.spectators) == 0

    assert game.rules.max_score == rules.max_score
    assert game.rules.target_delta_time == rules.target_delta_time

    assert game.field.ball.x == field_width / 2
    assert game.field.ball.y == field_height / 2

    assert game.field.ball.vx == ball_vx
    assert game.field.ball.vy == ball_vy
    assert game.field.ball.radius == ball_radius


def test_build_initial_game_raises_player_id_the_same(valid_build_game_params):
    valid_build_game_params["left_player_id"] = valid_build_game_params[
        "right_player_id"
    ]

    with pytest.raises(ValueError):
        factories.build_initial_game(**valid_build_game_params)


def test_build_initial_game_left_player_id_none(valid_build_game_params):
    valid_build_game_params["left_player_id"] = None

    game = factories.build_initial_game(**valid_build_game_params)

    assert game.sides[PlayerSide.LEFT] is None


def test_build_initial_game_right_player_id_none(valid_build_game_params):
    valid_build_game_params["right_player_id"] = None

    game = factories.build_initial_game(**valid_build_game_params)

    assert game.sides[PlayerSide.RIGHT] is None


def test_build_initial_game_raises_players_both_none(valid_build_game_params):
    valid_build_game_params["right_player_id"] = None
    valid_build_game_params["left_player_id"] = None

    with pytest.raises(ValueError):
        factories.build_initial_game(**valid_build_game_params)
