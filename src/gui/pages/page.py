from abc import ABC
from abc import abstractmethod
from typing import Callable

from pygame.event import Event


class Page(ABC):

    def __init__(self, change_page: Callable[[str], None]) -> None:
        self.change_page: Callable[[str], None] = change_page

    @abstractmethod
    def parse_event(self, event: Event) -> None:
        pass

    @abstractmethod
    def render(self) -> None: pass

    @abstractmethod
    def update(self, delta_time: float) -> None: pass
