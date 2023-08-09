from pygame import Rect
from pygame import Surface
from pygame.font import Font

from config.game_config import DEFAULT_FONT_SIZE
from game.game_screen import GameScreen
from game.game_stats import GameStats
from game.game_stats import Stats
from gui.gui_component import GuiComponent
from utils.callback_vars import CallbackTypes
from utils.fonts import FontManager
from utils.themes import Theme
from utils.themes import ThemeManager


class ScoreGui(GuiComponent):

    def __init__(self, board_rect: Rect) -> None:
        super().__init__(board_rect)
        stats: Stats = GameStats.get()
        self.update_surface(stats.words_right.get())
        stats.words_right.add_callback(self.update_surface)

    def update_surface(self, value: CallbackTypes) -> None:
        error_message: str = f"value should be {type(GameStats.get().words_right.get())} rather than {type(value)}"
        assert isinstance(value, int), error_message
        font: Font = FontManager.get_font(DEFAULT_FONT_SIZE)
        theme: Theme = ThemeManager.get_theme()
        surface: Surface = font.render(str(value), True, theme.foreground_primary, theme.background_primary)

        self.surface = surface
        self.rect = surface.get_rect(bottomleft=self.board_rect.topleft)

    def render(self) -> None:
        if self.surface is None or self.rect is None: return
        GameScreen.get_surface().blit(self.surface, self.rect)
