from math import ceil

from pygame import Rect
from pygame import Surface
from pygame import draw

from config.game_config import BASE_LIFE_POOL
from config.game_config import LIFE_COMBO_HEIGHT
from config.game_config import GUI_GAP
from config.game_config import LIFE_SURF_SIZE
from config.game_config import MAX_LIFE_POOL
from game.game_stats import GameStats
from game.game_stats import Stats
from gui.gui_component import GuiComponent
from utils.themes import Theme
from utils.themes import ThemeManager
from utils.window import Window


class LifeCombo:

    def __init__(self, board_rect: Rect) -> None:
        self.surface: Surface = Surface((board_rect.width, LIFE_COMBO_HEIGHT))
        self.surface.fill(ThemeManager.get_theme().foreground_primary)
        self.rect: Rect = self.surface.get_rect(midbottom=board_rect.midtop)
        self.rect.y -= (GUI_GAP * 2)
        stats: Stats = GameStats.get()
        self.full_lives: bool = stats.lives.get() == stats.life_pool.get()
        if self.full_lives:
            stats.combo_fill.set(float(self.rect.width))
        else:
            stats.combo_fill.set(0.0)
        stats.lives.add_callback(self.update_full_lives)

    def update_full_lives(self, lives: int) -> None:
        self.full_lives = lives == GameStats.get().life_pool.get()

    def render(self) -> None:
        if GameStats.get().combo_fill.get() == 0.0: return
        Window.get_surface().blit(self.surface, self.rect)

    def set_fill_width(self, fill_width: float) -> None:
        stats: Stats = GameStats.get()
        if fill_width <= 0:
            stats.combo_fill.set(0.0)
        elif fill_width >= self.rect.width:
            stats.combo_fill.set(float(self.rect.width))

            if not self.full_lives:
                GameStats.get().lives.increment(1)
                stats.combo_fill.set(0.0)

            if self.full_lives:
                stats.combo_fill.set(float(self.rect.width))
        else:
            stats.combo_fill.set(fill_width)

        self.surface = Surface((ceil(stats.combo_fill.get()), self.rect.height))
        self.surface.fill(ThemeManager.get_theme().foreground_primary)

    def update(self, delta_time: float) -> None:
        stats: Stats = GameStats.get()
        if stats.lives.get() == stats.life_pool.get(): return
        self.set_fill_width(stats.combo_fill.get() - (stats.combo_speed.get() * delta_time))
        self.surface = Surface((ceil(stats.combo_fill.get()), self.rect.height))
        self.surface.fill(ThemeManager.get_theme().foreground_primary)


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
        self.life_combo: LifeCombo = LifeCombo(board_rect)
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
        self.rect = life_pool_surface.get_rect(midbottom=self.life_combo.rect.midtop)
        self.rect.y -= (GUI_GAP * 2)

    def render(self) -> None:
        if self.surface is None or self.rect is None: return
        self.life_combo.render()
        Window.get_surface().blit(self.surface, self.rect)

    def update(self, delta_time: float) -> None:
        self.life_combo.update(delta_time)


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
