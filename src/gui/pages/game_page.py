from typing import NamedTuple

from pygame import KEYDOWN
from pygame import Rect
from pygame.event import Event

from config.game_config import BOARD_HEIGHT
from config.game_config import BOARD_WIDTH
from game.game_state import GameState
from game.game_stats import GameStats
from gui.button_gui import ButtonEvent
from gui.game_over_gui import GameOverGui
from gui.lives_gui import LivesGui
from gui.pages.page import Page
from gui.score_gui import ScoreGui


class GamePageGui(NamedTuple):
    lives: LivesGui
    score: ScoreGui
    game_over: GameOverGui


class GamePage(Page):

    @staticmethod
    def get_gui(board_rect: Rect) -> GamePageGui:
        return GamePageGui(LivesGui(board_rect), ScoreGui(board_rect), GameOverGui(board_rect))

    def __init__(self) -> None:
        self.state: GameState = GameState(BOARD_WIDTH, BOARD_HEIGHT)
        self.gui: GamePageGui = GamePage.get_gui(self.state.board.rect)
        self.gui.game_over.retry_button.add_call_back(ButtonEvent.MOUSECLICK_LEFT, self.state.reset)

    def render(self) -> None:
        self.state.render()
        self.gui.lives.render()
        self.gui.score.render()
        if GameStats.get().game_over.get():
            self.gui.game_over.render()

    def parse_event(self, event: Event) -> None:
        if event.type == KEYDOWN:
            self.state.process_key_name(event.key)

        self.gui.game_over.retry_button.parse_event(event)

    def update(self, delta_time: float) -> None:
        self.state.update(delta_time)
