from abc import ABC
from abc import abstractmethod

from pygame import Rect
from pygame import Surface


class GuiComponent(ABC):

    def __init__(self, board_rect: Rect) -> None:
        self.board_rect: Rect = board_rect
        self.rect: Rect | None = None
        self.surface: Surface | None = None

    @abstractmethod
    def render(self) -> None: pass
