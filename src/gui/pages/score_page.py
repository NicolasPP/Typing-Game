from typing import Callable

from pygame.event import Event

from config.game_config import BACK_LABEL_VALUE
from gui.button_gui import ButtonEvent
from gui.button_gui import ButtonGui
from gui.pages.page import Page
from utils.themes import ThemeManager
from utils.window import Window


class ScorePage(Page):
    def __init__(self, change_page: Callable[[str], None]) -> None:
        super().__init__(change_page)
        self.back_button: ButtonGui = ButtonGui(BACK_LABEL_VALUE)
        self.back_button.rect.center = Window.get_surface().get_rect().center
        self.back_button.add_call_back(ButtonEvent.LEFT_CLICK, lambda: self.change_page("MenuPage"))
        self.update_score_page_theme()
        ThemeManager.add_call_back(self.update_score_page_theme)

    def update_score_page_theme(self) -> None:
        self.back_button.configure(label_color=ThemeManager.get_theme().foreground_primary)

    def render(self) -> None:
        self.back_button.render(Window.get_surface())

    def parse_event(self, event: Event) -> None:
        self.back_button.parse_event(event)

    def update(self, delta_time: float) -> None:
        pass
