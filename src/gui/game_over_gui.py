from pygame import Rect
from pygame import Surface

from config.game_config import GAME_OVER_ALPHA
from config.game_config import TRY_AGAIN_VALUE
from game.game_screen import GameScreen
from gui.button_gui import ButtonGui
from gui.gui_component import GuiComponent
from utils.themes import Theme
from utils.themes import ThemeManager


class GameOverGui(GuiComponent):

    def __init__(self, board_rect: Rect) -> None:
        super().__init__(board_rect)
        self.surface = Surface(board_rect.size)
        self.surface.set_alpha(GAME_OVER_ALPHA)
        theme: Theme = ThemeManager.get_theme()
        self.surface.fill(theme.background_primary)

        self.retry_button: ButtonGui = ButtonGui(TRY_AGAIN_VALUE)
        self.retry_button.rect.center = self.board_rect.center

    def render(self) -> None:
        self.retry_button.render(GameScreen.get_surface())
        GameScreen.get_surface().blit(self.surface, self.board_rect)
