from dataclasses import dataclass

from pygame import Rect
from pygame import Surface
from pygame import display

from game.game_screen import GameScreen
from utils.themes import ThemeManager


@dataclass
class BoardConfig:
    background_color: tuple[int, int, int]


class Board:

    @staticmethod
    def get_config() -> BoardConfig:
        return BoardConfig(ThemeManager.get_theme().foreground_primary)

    def __init__(self, width: int, height: int) -> None:
        self.rect: Rect = Rect(0, 0, width, height)
        self.rect.center = GameScreen.get_surface().get_rect().center
        self.config: BoardConfig = Board.get_config()
        self.surface: Surface = Surface(self.rect.size)
        self.init_board_surface()
        ThemeManager.add_call_back(self.theme_call_back)

    def init_board_surface(self) -> None:
        self.surface.fill(self.config.background_color)

    def render(self) -> None:
        display.get_surface().blit(self.surface, self.rect)

    def theme_call_back(self) -> None:
        self.config.background_color = ThemeManager.get_theme().foreground_primary
        self.init_board_surface()
