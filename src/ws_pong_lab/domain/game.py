from __future__ import annotations

from abc import ABC, abstractmethod


class GameContext:
    """
    Контекст определяет интерфейс, представляющий интерес для клиентов. Он также
    хранит ссылку на экземпляр подкласса Состояния, который отображает текущее
    состояние Контекста.
    """

    _state = None
    """
    Ссылка на текущее состояние Контекста.
    """

    def __init__(self, state: GameState) -> None:
        self.transition_to(state)

    def transition_to(self, state: GameState):
        """
        Контекст позволяет изменять объект Состояния во время выполнения.
        """

        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    """
    Контекст делегирует часть своего поведения текущему объекту Состояния.
    """

    def process_command(self):
        self._state.handle1()


class GameState(ABC):
    """
    Базовый класс Состояния объявляет методы, которые должны реализовать все
    Конкретные Состояния, а также предоставляет обратную ссылку на объект
    Контекст, связанный с Состоянием. Эта обратная ссылка может использоваться
    Состояниями для передачи Контекста другому Состоянию.
    """

    @property
    def context(self) -> GameContext:
        return self._context

    @context.setter
    def context(self, context: GameContext) -> None:
        self._context = context

    @abstractmethod
    def handle1(self) -> None:
        pass

    @abstractmethod
    def handle2(self) -> None:
        pass


class ConcreteStateA(GameState):
    def handle1(self) -> None:
        print("ConcreteStateA handles request1.")
        print("ConcreteStateA wants to change the state of the context.")
        self.context.transition_to(ConcreteStateB())

    def handle2(self) -> None:
        print("ConcreteStateA handles request2.")


class ConcreteStateB(GameState):
    def handle1(self) -> None:
        print("ConcreteStateB handles request1.")

    def handle2(self) -> None:
        print("ConcreteStateB handles request2.")
        print("ConcreteStateB wants to change the state of the context.")
        self.context.transition_to(ConcreteStateA())
