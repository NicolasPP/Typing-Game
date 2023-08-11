from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import Callable

from config.theme_config import DARK_BACKGROUND_PRIMARY
from config.theme_config import DARK_BACKGROUND_SECONDARY
from config.theme_config import DARK_FOREGROUND_PRIMARY
from config.theme_config import DARK_FOREGROUND_SECONDARY
from config.theme_config import LIGHT_BACKGROUND_PRIMARY
from config.theme_config import LIGHT_BACKGROUND_SECONDARY
from config.theme_config import LIGHT_FOREGROUND_PRIMARY
from config.theme_config import LIGHT_FOREGROUND_SECONDARY


class ThemeType(Enum):
    DARK = auto()
    LIGHT = auto()


@dataclass
class Theme:
    name: str
    foreground_primary: tuple[int, int, int]
    foreground_secondary: tuple[int, int, int]
    background_primary: tuple[int, int, int]
    background_secondary: tuple[int, int, int]


class ThemeManager:
    current_theme: Theme | None = None
    themes: dict[ThemeType, Theme] = {}
    call_backs: list[Callable[[], None]] = []

    @staticmethod
    def get_theme() -> Theme:
        if ThemeManager.current_theme is None:
            ThemeManager.set_current_theme(ThemeType.DARK)

        assert ThemeManager.current_theme is not None
        return ThemeManager.current_theme

    @staticmethod
    def set_current_theme(theme_type: ThemeType) -> None:
        ThemeManager.current_theme = ThemeManager.get(theme_type)
        for call_back in ThemeManager.call_backs:
            call_back()

    @staticmethod
    def get(theme_type: ThemeType) -> Theme:
        theme: Theme | None = ThemeManager.themes.get(theme_type)
        assert theme is not None, f"theme: {theme_type.name} has not been loaded"
        return theme

    @staticmethod
    def add_call_back(call_back: Callable[[], None]) -> None:
        ThemeManager.call_backs.append(call_back)

    @staticmethod
    def load_themes() -> None:
        ThemeManager.themes[ThemeType.LIGHT] = Theme(ThemeType.LIGHT.name, LIGHT_FOREGROUND_PRIMARY,
                                                     LIGHT_FOREGROUND_SECONDARY, LIGHT_BACKGROUND_PRIMARY,
                                                     LIGHT_BACKGROUND_SECONDARY)
        ThemeManager.themes[ThemeType.DARK] = Theme(ThemeType.DARK.name, DARK_FOREGROUND_PRIMARY,
                                                    DARK_FOREGROUND_SECONDARY, DARK_BACKGROUND_PRIMARY,
                                                    DARK_BACKGROUND_SECONDARY)
