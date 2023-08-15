from pygame import Rect
from pygame import Surface

from config.game_config import BACK_LABEL_VALUE
from config.game_config import GAME_OVER_ALPHA
from config.game_config import GUI_GAP
from config.game_config import TRY_AGAIN_VALUE
from gui.button_gui import ButtonGui
from gui.gui_component import GuiComponent
from utils.themes import ThemeManager
from utils.window import Window


class GameOverGui(GuiComponent):

    def __init__(self, board_rect: Rect) -> None:
        super().__init__(board_rect)
        self.surface = Surface(board_rect.size)
        self.surface.set_alpha(GAME_OVER_ALPHA)

        ThemeManager.add_call_back(self.update_game_over_theme)

        self.back_button: ButtonGui = ButtonGui(BACK_LABEL_VALUE)
        self.retry_button: ButtonGui = ButtonGui(TRY_AGAIN_VALUE)

        self.update_game_over_theme()

        self.retry_button.rect.midbottom = self.board_rect.center
        self.back_button.rect.midtop = self.board_rect.center

        self.back_button.rect.y += + (GUI_GAP * 10)
        self.retry_button.rect.y -= + (GUI_GAP * 10)

    def update_game_over_theme(self) -> None:
        self.surface.fill(ThemeManager.get_theme().background_primary)

    def render(self) -> None:
        if self.surface is None: return
        Window.get_surface().blit(self.surface, self.board_rect)
        self.retry_button.render(Window.get_surface())
        self.back_button.render(Window.get_surface())
