from math import ceil

from pygame import Rect
from pygame import Surface
from pygame import draw

from config.game_config import GUI_GAP
from config.game_config import LIFE_SURF_SIZE
from game.game_screen import GameScreen
from gui.gui_component import GuiComponent
from gui.gui_vars import GuiVars
from utils.callback_vars import CallbackTypes
from utils.themes import Theme
from utils.themes import ThemeManager


class LivesGui(GuiComponent):

    @staticmethod
    def get_life_surface() -> Surface:
        surface: Surface = Surface((LIFE_SURF_SIZE, LIFE_SURF_SIZE))
        surface.fill(ThemeManager.get_theme().background_primary)
        theme: Theme = ThemeManager.get_theme()
        draw.circle(surface, theme.foreground_primary, surface.get_rect().center, ((LIFE_SURF_SIZE - GUI_GAP) // 2))
        # drawing heart
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

        return surface

    def __init__(self, board_rect: Rect) -> None:
        super().__init__(board_rect)
        self.update_surface(GuiVars.lives.get())
        GuiVars.lives.add_callback(self.update_surface)

    def update_surface(self, value: CallbackTypes) -> None:
        assert isinstance(value, int), f"value should be {type(GuiVars.lives.get())} rather than {type(value)}"
        if value < 0: value = 0
        lives_surface: Surface = Surface((LIFE_SURF_SIZE * value, LIFE_SURF_SIZE))
        prev_rect: Rect | None = None
        for _ in range(value):
            life_surface: Surface = LivesGui.get_life_surface()

            if prev_rect is None:
                life_rect = life_surface.get_rect(bottomright=lives_surface.get_rect().bottomright)
            else:
                life_rect = life_surface.get_rect(bottomright=prev_rect.bottomleft)

            lives_surface.blit(life_surface, life_rect)
            prev_rect = life_rect

        self.surface = lives_surface
        self.rect = lives_surface.get_rect()
        self.rect.bottomright = self.board_rect.topright
        self.rect.y -= GUI_GAP

    def render(self) -> None:
        if self.surface is None or self.rect is None: return
        GameScreen.get_surface().blit(self.surface, self.rect)
