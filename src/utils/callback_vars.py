from typing import Any
from typing import Callable
from typing import TypeAlias

CallbackTypes: TypeAlias = str | int | bool | float


class CallBack:
    def __init__(self, value: CallbackTypes) -> None:
        self.value: CallbackTypes = value
        self.callbacks: set[Callable[[Any], None]] = set()
        self.limit: CallbackTypes | None = None  # TODO add a way to add min and max not just max

    def set(self, value: CallbackTypes) -> None:
        assert isinstance(value, type(self.value)), f"expected {type(self.value).__name__}, got {type(value).__name__}"
        if self.limit is not None:
            if value > self.limit: return
        self.value = value
        self.exec_callbacks()

    def set_limit(self, limit: CallbackTypes) -> None:
        assert isinstance(limit, type(self.value)), f"expected {type(self.value).__name__}, got {type(limit).__name__}"
        self.limit = limit

    def exec_callbacks(self) -> None:
        for func in self.callbacks:
            func(self.value)

    def add_callback(self, callback_func: Callable[[Any], None]) -> None:
        if callback_func in self.callbacks: return
        self.callbacks.add(callback_func)

    def increment(self, value: CallbackTypes) -> None:
        assert isinstance(value, type(self.value)), f"expected {type(self.value).__name__}, got {type(value).__name__}"
        self.set(self.value + value)


class IntCB(CallBack):
    def __init__(self, value: int) -> None:
        super().__init__(value)

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

    def get(self) -> float:
        assert isinstance(self.value, float), "must be a float"
        return self.value
