from typing import Callable
from typing import NamedTuple

from pygame.event import Event

from config.game_config import GUI_GAP
from config.game_config import PLAY_LABEL_VALUE
from config.game_config import SCORE_LABEL_VALUE
from gui.button_gui import ButtonEvent
from gui.button_gui import ButtonGui
from gui.pages.page import Page
from utils.themes import Theme
from utils.themes import ThemeManager
from utils.themes import ThemeType
from utils.window import Window


class MenuPageGui(NamedTuple):
    play: ButtonGui
    score: ButtonGui
    theme: ButtonGui


class MenuPage(Page):

    @staticmethod
    def get_gui() -> MenuPageGui:
        return MenuPageGui(ButtonGui(PLAY_LABEL_VALUE), ButtonGui(SCORE_LABEL_VALUE), ButtonGui(size=(50, 50)))

    def __init__(self, change_page: Callable[[str], None]) -> None:
        super().__init__(change_page)
        self.gui: MenuPageGui = MenuPage.get_gui()

        self.update_menu_theme()
        self.gui.play.rect.midbottom = Window.get_surface().get_rect().center
        self.gui.score.rect.midtop = self.gui.play.rect.center
        self.gui.theme.rect.midbottom = Window.get_surface().get_rect().midbottom

        self.gui.play.rect.y -= GUI_GAP * 10
        self.gui.score.rect.y += GUI_GAP * 10
        self.gui.theme.rect.y -= GUI_GAP * 10

        self.gui.play.add_call_back(ButtonEvent.LEFT_CLICK, lambda: self.change_page("GamePage"))
        self.gui.score.add_call_back(ButtonEvent.LEFT_CLICK, lambda: self.change_page("ScorePage"))
        self.gui.theme.add_call_back(ButtonEvent.LEFT_CLICK, switch_theme)

        ThemeManager.add_call_back(self.update_menu_theme)

    def update_menu_theme(self) -> None:
        theme: Theme = ThemeManager.get_theme()
        self.gui.play.configure(label_color=theme.foreground_primary)
        self.gui.score.configure(label_color=theme.foreground_primary)
        self.gui.theme.configure(label_color=theme.foreground_primary)

    def render(self) -> None:
        self.gui.play.render(Window.get_surface())
        self.gui.score.render(Window.get_surface())
        self.gui.theme.render(Window.get_surface())

    def parse_event(self, event: Event) -> None:
        self.gui.play.parse_event(event)
        self.gui.score.parse_event(event)
        self.gui.theme.parse_event(event)

    def update(self, delta_time: float) -> None:
        pass


def switch_theme() -> None:
    if ThemeManager.get_theme().name == ThemeType.LIGHT.name:
        ThemeManager.set_current_theme(ThemeType.DARK)
    else:
        ThemeManager.set_current_theme(ThemeType.LIGHT)
