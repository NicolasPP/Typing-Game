from abc import ABC
from abc import abstractmethod

from pygame.event import Event


class Page(ABC):

    @abstractmethod
    def parse_event(self, event: Event) -> None:
        pass

    @abstractmethod
    def render(self) -> None: pass

    @abstractmethod
    def update(self, delta_time: float) -> None: pass
