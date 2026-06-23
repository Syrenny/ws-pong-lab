class DomainError(Exception):
    """Base class for domain-level errors."""


class GameCommandNotAllowedError(DomainError):
    def __init__(self, *, command: str, state: str) -> None:
        super().__init__(f"Command '{command}' is not allowed in game state '{state}'")
