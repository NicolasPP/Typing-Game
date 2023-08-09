from pygame import Rect
from pygame import Surface
from pygame.font import Font
from pygame import mouse

from config.game_config import DEFAULT_FONT_SIZE
from config.game_config import GAME_OVER_ALPHA
from config.game_config import TRY_AGAIN_VALUE
from game.game_screen import GameScreen
from gui.gui_component import GuiComponent
from gui.gui_vars import GuiVars
from utils.callback_vars import CallbackTypes
from utils.fonts import FontManager
from utils.themes import Theme
from utils.themes import ThemeManager


class GameOverGui(GuiComponent):

    def __init__(self, board_rect: Rect) -> None:
        super().__init__(board_rect)
        self.surface = Surface(board_rect.size)
        self.surface.set_alpha(GAME_OVER_ALPHA)
        theme: Theme = ThemeManager.get_theme()
        self.surface.fill(theme.background_primary)
        font: Font = FontManager.get_font(DEFAULT_FONT_SIZE)

        self.is_try_again_collided: bool = False
        self.try_again: Surface = font.render(TRY_AGAIN_VALUE, True, theme.background_primary)
        self.try_again_rect: Rect = self.try_again.get_rect(center=self.board_rect.center)

    def render(self) -> None:
        if GuiVars.game_over.get():
            GameScreen.get_surface().blit(self.surface, self.board_rect)
            GameScreen.get_surface().blit(self.try_again, self.try_again_rect)

            if self.is_try_again_collided:
                hover: Surface = Surface(self.try_again.get_size())
                hover.set_alpha(GAME_OVER_ALPHA)
                hover.fill(ThemeManager.get_theme().background_primary)
                GameScreen.get_surface().blit(hover, self.try_again_rect)

    def try_again_collision(self) -> bool:
        return self.try_again_rect.collidepoint(mouse.get_pos())

    def update(self) -> None:
        self.is_try_again_collided = self.try_again_collision()

    def update_surface(self, value: CallbackTypes) -> None:
        pass
