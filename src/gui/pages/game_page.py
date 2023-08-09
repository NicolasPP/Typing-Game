from pygame import KEYDOWN
from pygame.event import Event

from config.game_config import BOARD_HEIGHT
from config.game_config import BOARD_WIDTH
from game.game_state import GameState
from gui.button_gui import ButtonEvent
from gui.gui_manager import GuiManager
from gui.pages.page import Page


class GamePage(Page):
    def __init__(self) -> None:
        self.state: GameState = GameState(BOARD_WIDTH, BOARD_HEIGHT)
        self.gui_manager: GuiManager = GuiManager(self.state.board.rect)
        self.gui_manager.game_over.retry_button.add_call_back(ButtonEvent.MOUSECLICK_LEFT, self.state.reset)

    def render(self) -> None:
        self.state.render()
        self.gui_manager.render()

    def parse_event(self, event: Event) -> None:
        if event.type == KEYDOWN:
            self.state.process_key_name(event.key)

        self.gui_manager.game_over.retry_button.parse_event(event)

    def update(self, delta_time: float) -> None:
        self.state.update(delta_time)
