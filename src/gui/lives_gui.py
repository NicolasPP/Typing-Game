from math import ceil

from pygame import Rect
from pygame import Surface
from pygame import draw

from config.game_config import BASE_LIFE_POOL
from config.game_config import GUI_GAP
from config.game_config import LIFE_SURF_SIZE
from config.game_config import MAX_LIFE_POOL
from game.game_stats import GameStats
from game.game_stats import Stats
from gui.gui_component import GuiComponent
from utils.themes import Theme
from utils.themes import ThemeManager
from utils.window import Window


class LivesGui(GuiComponent):

    @staticmethod
    def get_life_surface(add_heart: bool = True) -> Surface:
        surface: Surface = Surface((LIFE_SURF_SIZE, LIFE_SURF_SIZE))
        surface.fill(ThemeManager.get_theme().background_primary)
        theme: Theme = ThemeManager.get_theme()
        draw.circle(surface, theme.foreground_primary, surface.get_rect().center, ((LIFE_SURF_SIZE - GUI_GAP) // 2))
        if add_heart: draw_heart(surface, theme)
        return surface

    def __init__(self, board_rect: Rect) -> None:
        super().__init__(board_rect)
        stats: Stats = GameStats.get()
        self.update_surface()
        stats.life_pool.add_callback(lambda val: self.update_surface())
        stats.lives.add_callback(lambda val: self.update_surface())

    def update_surface(self) -> None:
        stats: Stats = GameStats.get()
        if not BASE_LIFE_POOL <= stats.life_pool.get() <= MAX_LIFE_POOL: return
        life_spot_surface: Surface = LivesGui.get_life_surface(add_heart=False)
        life_heart_surface: Surface = LivesGui.get_life_surface()
        life_pool_surface: Surface = Surface(
            (life_spot_surface.get_width() * stats.life_pool.get(), life_spot_surface.get_height()))
        prev_rect: Rect | None = None
        hearts_placed: int = 0
        heart_surface: Surface = life_heart_surface
        for _ in range(stats.life_pool.get()):

            if hearts_placed >= stats.lives.get():
                heart_surface = life_spot_surface

            if prev_rect is None:
                life_rect = heart_surface.get_rect(bottomright=life_pool_surface.get_rect().bottomright)
            else:
                life_rect = heart_surface.get_rect(bottomright=prev_rect.bottomleft)

            life_pool_surface.blit(heart_surface, life_rect)
            prev_rect = life_rect

            hearts_placed += 1

        self.surface = life_pool_surface
        self.rect = life_pool_surface.get_rect(midbottom=self.board_rect.midtop)
        self.rect.y -= (GUI_GAP * 2)

    def render(self) -> None:
        if self.surface is None or self.rect is None: return
        Window.get_surface().blit(self.surface, self.rect)


def draw_heart(surface: Surface, theme: Theme) -> None:
    scale: float = min(surface.get_width(), surface.get_height()) * 0.4
    width: int = int(scale)
    height: int = int(scale * 1.45)

    # Calculate heart position
    x, y = surface.get_rect().center
    y += ceil(LIFE_SURF_SIZE / 10) - 1

    draw.polygon(surface, theme.background_primary,
                 [(x, y + height // 4), (x - width // 2, y - height // 4), (x + width // 2, y - height // 4)])
    draw.circle(surface, theme.background_primary, (x - width // 4, y - height // 4), width // 4)
    draw.circle(surface, theme.background_primary, (x + width // 4, y - height // 4), width // 4)
