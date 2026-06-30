from typing import Literal

import pytest

from ws_pong_lab.domain.collision import WallSide
from ws_pong_lab.domain.models import PlayerSide
from ws_pong_lab.domain.scoring import InvalidScoreError, award_goal, find_winner


def _award_goal_case(
    *,
    score: tuple[int, int],
    goal_side: Literal[WallSide.LEFT, WallSide.RIGHT],
    expected: tuple[int, int],
    id: str,
):
    return pytest.param(score, goal_side, expected, id=id)


@pytest.mark.parametrize(
    ("score", "goal_side", "expected"),
    (
        _award_goal_case(
            score=(0, 1),
            goal_side=WallSide.LEFT,
            expected=(0, 2),
            id="left-goal-awards-right-player",
        ),
        _award_goal_case(
            score=(1, 0),
            goal_side=WallSide.RIGHT,
            expected=(2, 0),
            id="right-goal-awards-left-player",
        ),
        _award_goal_case(
            score=(0, 0),
            goal_side=WallSide.LEFT,
            expected=(0, 1),
            id="left-goal-from-zero-score",
        ),
        _award_goal_case(
            score=(0, 0),
            goal_side=WallSide.RIGHT,
            expected=(1, 0),
            id="right-goal-from-zero-score",
        ),
        _award_goal_case(
            score=(10, 9),
            goal_side=WallSide.LEFT,
            expected=(10, 10),
            id="left-goal-keeps-left-score",
        ),
        _award_goal_case(
            score=(9, 10),
            goal_side=WallSide.RIGHT,
            expected=(10, 10),
            id="right-goal-keeps-right-score",
        ),
    ),
)
def test_award_goal(
    score: tuple[int, int],
    goal_side: Literal[WallSide.LEFT, WallSide.RIGHT],
    expected: tuple[int, int],
):
    new_score = award_goal(score=score, goal_side=goal_side)

    assert new_score == expected


def _find_winner_case(
    *,
    score: tuple[int, int],
    expected: PlayerSide | None,
    id: str,
):
    return pytest.param(score, expected, id=id)


@pytest.mark.parametrize(
    ("score", "expected"),
    (
        _find_winner_case(
            score=(0, 10),
            expected=PlayerSide.RIGHT,
            id="right-player-wins",
        ),
        _find_winner_case(
            score=(10, 0),
            expected=PlayerSide.LEFT,
            id="left-player-wins",
        ),
        _find_winner_case(
            score=(9, 9),
            expected=None,
            id="no-winner-before-max-score",
        ),
        _find_winner_case(
            score=(10, 9),
            expected=PlayerSide.LEFT,
            id="left-wins-at-max-score",
        ),
        _find_winner_case(
            score=(9, 10),
            expected=PlayerSide.RIGHT,
            id="right-wins-at-max-score",
        ),
        _find_winner_case(
            score=(0, 0),
            expected=None,
            id="no-winner-at-zero-score",
        ),
    ),
)
def test_find_winner(
    score: tuple[int, int],
    expected: PlayerSide | None,
):
    player_side = find_winner(
        score={PlayerSide.LEFT: score[0], PlayerSide.RIGHT: score[1]}, max_score=10
    )

    assert player_side == expected


def _invalid_find_winner_case(
    *,
    score: tuple[int, int],
    raises: type[Exception],
    id: str,
):
    return pytest.param(score, raises, id=id)


@pytest.mark.parametrize(
    ("score", "raises"),
    (
        _invalid_find_winner_case(
            score=(10, 10),
            raises=InvalidScoreError,
            id="both-players-reached-max-score",
        ),
        _invalid_find_winner_case(
            score=(11, 10),
            raises=InvalidScoreError,
            id="both-players-exceeded-max-score",
        ),
        _invalid_find_winner_case(
            score=(-10, 10),
            raises=InvalidScoreError,
            id="left-negative",
        ),
        _invalid_find_winner_case(
            score=(10, -10),
            raises=InvalidScoreError,
            id="right-negative",
        ),
    ),
)
def test_invalid_find_winner(
    score: tuple[int, int],
    raises: type[Exception],
):
    with pytest.raises(raises):
        find_winner(
            score={PlayerSide.LEFT: score[0], PlayerSide.RIGHT: score[1]}, max_score=10
        )
