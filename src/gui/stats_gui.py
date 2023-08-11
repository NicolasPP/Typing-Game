from pygame import Rect
from pygame import Surface
from pygame.font import Font

from config.game_config import DEFAULT_FONT_SIZE
from config.game_config import GUI_GAP
from game.game_stats import GameStats
from game.game_stats import Stats
from gui.gui_component import GuiComponent
from utils.fonts import FontManager
from utils.themes import Theme
from utils.themes import ThemeManager
from utils.window import Window


class StatsGui(GuiComponent):

    def __init__(self, board_rect: Rect) -> None:
        super().__init__(board_rect)
        stats: Stats = GameStats.get()
        self.font: Font = FontManager.get_font(DEFAULT_FONT_SIZE)

        self.score_surface: Surface | None = None
        self.score_rect: Rect | None = None
        self.speed_surface: Surface | None = None
        self.speed_rect: Rect | None = None
        self.spawn_delay_surface: Surface | None = None
        self.spawn_rect: Rect | None = None

        self.update_score_surface(stats.words_right.get())
        stats.words_right.add_callback(self.update_score_surface)

        self.update_speed_surface(stats.fall_speed.get())
        stats.fall_speed.add_callback(self.update_speed_surface)

        self.update_spawn_delay_surface(stats.spawn_delay.get())
        stats.spawn_delay.add_callback(self.update_spawn_delay_surface)

    def update_score_surface(self, score: int) -> None:
        theme: Theme = ThemeManager.get_theme()
        surface: Surface = self.font.render(str(score), True, theme.foreground_primary, theme.background_primary)

        self.score_surface = surface
        self.score_rect = surface.get_rect(midtop=self.board_rect.midbottom)
        self.score_rect.y += (GUI_GAP * 2)

    def update_speed_surface(self, speed: float) -> None:
        theme: Theme = ThemeManager.get_theme()
        font: Font = FontManager.get_font(int(DEFAULT_FONT_SIZE * 0.7))
        text: str = f"{round(speed, 2)} p/s"
        surface: Surface = font.render(text, True, theme.foreground_primary, theme.background_primary)

        self.speed_surface = surface
        self.speed_rect = surface.get_rect(topleft=self.board_rect.bottomleft)
        self.speed_rect.y += (GUI_GAP * 2)

    def update_spawn_delay_surface(self, spawn_delay: float) -> None:
        theme: Theme = ThemeManager.get_theme()
        font: Font = FontManager.get_font(int(DEFAULT_FONT_SIZE * 0.7))
        text: str = f"{round(spawn_delay, 2)} s/w"
        surface: Surface = font.render(text, True, theme.foreground_primary, theme.background_primary)

        self.spawn_delay_surface = surface
        self.spawn_rect = surface.get_rect(topright=self.board_rect.bottomright)
        self.spawn_rect.y += (GUI_GAP * 2)

    def render(self) -> None:
        def render_stat(surf: Surface | None, rect: Rect | None) -> None:
            if surf is None or rect is None: return
            Window.get_surface().blit(surf, rect)

        render_stat(self.score_surface, self.score_rect)
        render_stat(self.speed_surface, self.speed_rect)
        render_stat(self.spawn_delay_surface, self.spawn_rect)
