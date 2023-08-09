from dataclasses import dataclass
from enum import Enum
from typing import Callable

from pygame import MOUSEBUTTONDOWN
from pygame import Rect
from pygame import Surface
from pygame import mouse
from pygame.event import Event
from pygame.font import Font

from config.game_config import DEFAULT_FONT_SIZE
from config.game_config import HOVER_ALPHA
from utils.fonts import FontManager
from utils.themes import Theme
from utils.themes import ThemeManager


@dataclass
class ButtonConfig:
    label_color: tuple[int, int, int]
    hover_color: tuple[int, int, int]
    hover_alpha: int
    font_size: int

# TODO rename to LEFT, MIDDLE, ...
class ButtonEvent(Enum):
    MOUSECLICK_LEFT = 1
    MOUSECLICK_MIDDLE = 2
    MOUSECLICK_RIGHT = 3
    MOUSECLICK_SCROLL_UP = 4
    MOUSECLICK_SCROLL_DOWN = 5


class ButtonGui:

    @staticmethod
    def get_default_config() -> ButtonConfig:
        theme: Theme = ThemeManager.get_theme()
        return ButtonConfig(theme.background_primary, theme.background_primary, HOVER_ALPHA, DEFAULT_FONT_SIZE)

    def __init__(self, label: str | None = None, size: tuple[int, int] = None) -> None:
        assert not (label is None and size is None), "must provide label or size"
        self.label: str | None = label
        self.size: tuple[int, int] | None = size
        self.cfg: ButtonConfig = ButtonGui.get_default_config()
        self.surface: Surface = self.create_surface()
        self.hover_surface: Surface = self.create_hover_surface()
        self.rect: Rect = self.surface.get_rect()
        self.call_backs: dict[int, list[Callable[[], None]]] = {}

    def configure(self, label_color: tuple[int, int, int] | None = None,
                  hover_color: tuple[int, int, int] | None = None, hover_alpha: int | None = None,
                  font_size: int | None = None) -> None:
        if label_color is not None:
            if self.label is not None and len(self.label) > 0:
                self.cfg.label_color = label_color

        if font_size is not None:
            if self.label is not None and len(self.label) > 0:
                self.cfg.font_size = font_size

        if hover_color is not None:
            self.cfg.hover_color = hover_color

        if hover_alpha is not None:
            self.cfg.hover_alpha = hover_alpha

        self.surface = self.create_surface()
        self.hover_surface = self.create_hover_surface()

    def create_hover_surface(self) -> Surface:
        hover_surface: Surface = Surface(self.surface.get_size())
        hover_surface.set_alpha(self.cfg.hover_alpha)
        hover_surface.fill(self.cfg.hover_color)
        return hover_surface

    def create_surface(self) -> Surface:
        if self.label is None:
            return Surface(self.size)

        font: Font = FontManager.get_font(self.cfg.font_size)
        return font.render(self.label, True, self.cfg.label_color)

    def render(self, parent_surface: Surface) -> None:
        parent_surface.blit(self.surface, self.rect)
        if self.is_collided((parent_surface.get_rect().x, parent_surface.get_rect().y)):
            parent_surface.blit(self.hover_surface, self.rect)

    def is_collided(self, offset: tuple[int, int]) -> bool:
        x, y = mouse.get_pos()
        off_x, off_y = offset
        return self.rect.collidepoint(x + off_x, y + off_y)

    def parse_event(self, event: Event, parent_offset: tuple[int, int]) -> None:
        if event.type != MOUSEBUTTONDOWN: return
        func_list: list[Callable[[], None]] | None = self.call_backs.get(event.button)
        if func_list is None: return
        if self.is_collided(parent_offset):
            for func in func_list:
                func()

    def add_call_back(self, button_event: ButtonEvent, func: Callable[[], None]) -> None:
        if button_event.value not in self.call_backs:
            self.call_backs[button_event.value] = [func]
        else:
            self.call_backs[button_event.value].append(func)
