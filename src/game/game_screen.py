from __future__ import annotations

from dataclasses import dataclass

from pygame import Surface
from pygame import display

from config.game_config import GAME_SCREEN_HEIGHT
from config.game_config import GAME_SCREEN_WIDTH
from utils.themes import ThemeManager


@dataclass
class GameScreenConfig:
    background_color: tuple[int, int, int]


class GameScreen:
    screen: GameScreen | None = None

    @staticmethod
    def get() -> GameScreen:
        if GameScreen.screen is None:
            GameScreen.screen = GameScreen()

        return GameScreen.screen

    @staticmethod
    def get_surface() -> Surface:
        return GameScreen.get().surface

    @staticmethod
    def get_config() -> GameScreenConfig:
        return GameScreenConfig(ThemeManager.get_theme().background_primary)

    def __init__(self) -> None:
        self.surface: Surface = display.set_mode((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
        self.config: GameScreenConfig = GameScreen.get_config()
        ThemeManager.add_call_back(self.theme_call_back)

    def clear(self) -> None:
        self.surface.fill(self.config.background_color)

    def theme_call_back(self) -> None:
        self.config.background_color = ThemeManager.get_theme().background_primary
