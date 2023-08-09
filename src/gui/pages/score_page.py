from typing import Callable

from pygame.event import Event

from gui.pages.page import Page


class ScorePage(Page):
    def __init__(self, change_page: Callable[[str], None]) -> None:
        super().__init__(change_page)

    def render(self) -> None:
        pass

    def parse_event(self, event: Event) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass
