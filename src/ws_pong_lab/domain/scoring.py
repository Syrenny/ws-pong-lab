from .collision import WallSide
from .errors import InvalidScoreError
from .models import PlayerSide


def award_goal(*, score: tuple[int, int], goal_side: WallSide) -> tuple[int, int]:
    if goal_side is WallSide.LEFT:
        score = score[0], score[1] + 1
    else:
        score = score[0] + 1, score[1]

    return score


def find_winner(score: dict[PlayerSide, int], max_score: int) -> PlayerSide | None:
    left_reached = score[PlayerSide.LEFT] >= max_score
    right_reached = score[PlayerSide.RIGHT] >= max_score

    if left_reached and right_reached:
        raise InvalidScoreError("Both players reached max score")

    for side, value in score.items():
        if value > max_score:
            raise InvalidScoreError(f"Score of {side} exceeded max_score")

        if value < 0:
            raise InvalidScoreError(f"Score of {side} is negative")

    if left_reached:
        return PlayerSide.LEFT

    if right_reached:
        return PlayerSide.RIGHT

    return None
