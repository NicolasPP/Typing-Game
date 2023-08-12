from typing import Any
from typing import Callable
from typing import TypeAlias

CallbackTypes: TypeAlias = str | int | bool | float


class CallBack:
    def __init__(self, value: CallbackTypes) -> None:
        self.value: CallbackTypes = value
        self.callbacks: set[Callable[[Any], None]] = set()

    def set(self, value: Any) -> None:
        assert isinstance(value, type(self.value)), f"expected {type(self.value).__name__}, got {type(value).__name__}"
        self.value = value
        self.exec_callbacks()

    def exec_callbacks(self) -> None:
        for func in self.callbacks:
            func(self.value)

    def add_callback(self, callback_func: Callable[[Any], None]) -> None:
        if callback_func in self.callbacks: return
        self.callbacks.add(callback_func)


class IntCB(CallBack):
    def __init__(self, value: int) -> None:
        super().__init__(value)
        self.limit_min: int | None = None
        self.limit_max: int | None = None

    def set(self, value: int) -> None:

        if self.limit_max is not None:
            if value > self.limit_max: return

        if self.limit_min is not None:
            if value < self.limit_min: return

        super().set(value)

    def set_limit(self, limit_min: int | None, limit_max: int | None) -> None:
        self.limit_min = limit_min
        self.limit_max = limit_max

    def increment(self, value: int) -> None:
        self.set(self.get() + value)

    def get(self) -> int:
        assert isinstance(self.value, int), "must be an int"
        return self.value


class StrCB(CallBack):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def get(self) -> str:
        assert isinstance(self.value, str), "must be an str"
        return self.value


class BoolCB(CallBack):
    def __init__(self, value: bool) -> None:
        super().__init__(value)

    def get(self) -> bool:
        assert isinstance(self.value, bool), "must be an bool"
        return self.value


class FloatCB(CallBack):
    def __init__(self, value: float) -> None:
        super().__init__(value)
        self.limit_min: float | None = None
        self.limit_max: float | None = None

    def set(self, value: float) -> None:

        if self.limit_max is not None:
            if value > self.limit_max: return

        if self.limit_min is not None:
            if value < self.limit_min: return

        super().set(value)

    def set_limit(self, limit_min: float | None, limit_max: float | None) -> None:
        self.limit_min = limit_min
        self.limit_max = limit_max

    def increment(self, value: float) -> None:
        self.set(self.get() + value)

    def get(self) -> float:
        assert isinstance(self.value, float), "must be a float"
        return self.value
