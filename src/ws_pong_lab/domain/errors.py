class DomainError(ValueError):
    pass


class BallOutOfFieldError(DomainError):
    def __init__(
        self,
        *,
        ball_xy: tuple[float, float],
        ball_radius: int,
        field_wh: tuple[int, int],
    ) -> None:
        super().__init__(
            f"Ball moved outside the field: ball_xy={ball_xy}, ball_radius={ball_radius} field_wh={field_wh}"
        )


class InvalidScoreError(DomainError):
    pass


class GameCommandNotAllowedError(DomainError):
    pass
