import typing

CallbackTypes: typing.TypeAlias = str | int | bool | float


class CallBack:
    def __init__(self, value: CallbackTypes) -> None:
        self.value: CallbackTypes = value
        self.callbacks: set[typing.Callable[[CallbackTypes], None]] = set()

    def set(self, value: CallbackTypes) -> None:
        self.value = value
        self.exec_callbacks()

    def exec_callbacks(self) -> None:
        for func in self.callbacks:
            func(self.value)

    def add_callback(self, callback_func: typing.Callable[[CallbackTypes], None]) -> None:
        if callback_func in self.callbacks: return
        self.callbacks.add(callback_func)


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
