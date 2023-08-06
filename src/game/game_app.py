from time import time

from pygame import QUIT
from pygame import display
from pygame import event
from pygame import font

from config.game_config import BOARD_HEIGHT
from config.game_config import BOARD_WIDTH
from game.components.letter import Letter
from game.game_screen import GameScreen
from game.game_state import GameState
from utils.themes import ThemeManager
from utils.word_data_manager import WordDataManager


class GameApp:

    def __init__(self) -> None:
        ThemeManager.load_themes()
        Letter.load_state_colors()
        WordDataManager.load_words()
        font.init()

        self.state: GameState = GameState(BOARD_WIDTH, BOARD_HEIGHT)
        self.done: bool = False
        self.prev_time: float = time()
        self.delta_time: float = 0.0

    def run(self) -> None:

        while not self.done:

            now: float = time()
            self.delta_time = now - self.prev_time
            self.prev_time = now

            for game_event in event.get():
                if game_event.type == QUIT:
                    self.done = True
                else:
                    self.state.parse_player_input(game_event)

            GameScreen.get().clear()
            self.state.update(self.delta_time)
            self.state.render()
            display.flip()
