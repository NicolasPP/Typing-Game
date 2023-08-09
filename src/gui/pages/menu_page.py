from typing import Callable
from typing import NamedTuple

from pygame import Rect
from pygame.event import Event

from config.game_config import PLAY_LABEL_VALUE
from config.game_config import SCORE_LABEL_VALUE
from gui.button_gui import ButtonEvent
from gui.button_gui import ButtonGui
from gui.pages.page import Page
from utils.themes import Theme
from utils.themes import ThemeManager
from utils.window import Window


class MenuPageGui(NamedTuple):
    play: ButtonGui
    score: ButtonGui


class MenuPage(Page):

    @staticmethod
    def get_gui() -> MenuPageGui:
        return MenuPageGui(ButtonGui(PLAY_LABEL_VALUE), ButtonGui(SCORE_LABEL_VALUE))

    def __init__(self, change_page: Callable[[str], None]) -> None:
        super().__init__(change_page)
        self.gui: MenuPageGui = MenuPage.get_gui()

        theme: Theme = ThemeManager.get_theme()
        self.gui.play.configure(theme.foreground_primary)
        self.gui.score.configure(theme.foreground_primary)
        self.gui.play.rect.center = Window.get_surface().get_rect().center
        self.gui.score.rect.midtop = self.gui.play.rect.midbottom
        self.gui.score.rect.y += self.gui.score.rect.width // 2

        self.gui.play.add_call_back(ButtonEvent.MOUSECLICK_LEFT, lambda: self.change_page("GamePage"))
        self.gui.score.add_call_back(ButtonEvent.MOUSECLICK_LEFT, lambda: self.change_page("ScorePage"))

    def render(self) -> None:
        self.gui.play.render(Window.get_surface())
        self.gui.score.render(Window.get_surface())

    def parse_event(self, event: Event) -> None:
        window_rect: Rect = Window.get_surface().get_rect()
        offset: tuple[int, int] = window_rect.x, window_rect.y
        self.gui.play.parse_event(event, offset)
        self.gui.score.parse_event(event, offset)

    def update(self, delta_time: float) -> None:
        pass
