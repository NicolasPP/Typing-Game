from pygame import Rect
from pygame import Surface
from pygame.font import Font

from config.game_config import DEFAULT_FONT_SIZE
from config.game_config import REQUIRED_WORDS_ALPHA
from config.game_config import GUI_GAP
from game.game_stats import GameStats
from game.game_stats import Stats
from gui.gui_component import GuiComponent
from utils.fonts import FontManager
from utils.themes import Theme
from utils.themes import ThemeManager
from utils.window import Window


class LevelGui(GuiComponent):

    def __init__(self, board_rect: Rect) -> None:
        super().__init__(board_rect)
        stats: Stats = GameStats.get()
        self.update_surface(stats.words_required.get())
        stats.words_required.add_callback(self.update_surface)

    def update_surface(self, level_num: int) -> None:
        font: Font = FontManager.get_font(DEFAULT_FONT_SIZE * 6)
        theme: Theme = ThemeManager.get_theme()
        surface: Surface = font.render(str(level_num), True, theme.background_primary, theme.foreground_primary)
        surface.set_alpha(REQUIRED_WORDS_ALPHA)

        self.surface = surface
        self.rect = surface.get_rect(center=self.board_rect.center)
        self.rect.y += (GUI_GAP * 2)

    def render(self) -> None:
        if self.surface is None or self.rect is None: return
        Window.get_surface().blit(self.surface, self.rect)
