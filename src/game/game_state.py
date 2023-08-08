from pygame import KEYDOWN
from pygame import K_BACKSPACE
from pygame.event import Event
from pygame.key import name

from config.game_config import SPAWN_DELAY
from game.components.board import Board
from game.components.level import LevelManager
from game.components.text import Text
from gui.gui_manager import GuiManager
from gui.gui_vars import GuiVars
from utils.accumulator import Accumulator
from utils.word_data_manager import WordDataManager


class GameState:

    def __init__(self, board_width: int, board_height: int) -> None:
        self.board: Board = Board(board_width, board_height)
        self.level_manager: LevelManager = LevelManager()
        self.gui_manager: GuiManager = GuiManager(self.board.rect)
        self.spawn_accumulator: Accumulator = Accumulator(SPAWN_DELAY)

        self.texts: list[Text] = []
        self.played_words: list[str] = []

        self.stop_spawning: bool = False
        self.game_over: bool = False
        self.current_text: Text | None = None

        GuiVars.lives.add_callback(self.end_game)

    def render(self) -> None:
        self.board.clear()
        for text in self.texts:
            text.render(self.board.surface)
        self.board.render()
        self.gui_manager.render()

    def update(self, delta_time: float) -> None:
        if self.game_over: return
        if self.spawn_accumulator.wait(delta_time):
            self.spawn_text()

        # update words
        for text in self.texts:
            text.fall(delta_time, self.level_manager.get_speed())

        current_text: Text | None = self.get_current_text()
        if current_text is None: return
        if current_text.is_done():
            self.remove_fist_text()

        if self.is_text_collided():
            GuiVars.lives.set(GuiVars.lives.get() - 1)

    def parse_player_input(self, game_event: Event):
        if game_event.type == KEYDOWN:
            self.process_key_name(game_event.key)

    def add_text(self, word_values: list[str]) -> None:
        text: Text = Text(word_values)
        text.set_random_pos(self.board.rect.width)
        if len(self.texts) == 0: text.underline_current_word()
        self.texts.append(text)

    def spawn_text(self) -> None:
        if self.stop_spawning: return
        word_values: list[str] = []
        target_length: int = LevelManager.roll_text_length()

        while len(word_values) < target_length:
            word_val: str = WordDataManager.get_random_word(played_words=self.played_words,
                                                            word_lengths=self.level_manager.get_word_lengths())
            word_values.append(word_val)
            self.played_words.append(word_val)

        self.add_text(word_values)

    def remove_fist_text(self) -> None:
        self.texts = self.texts[1:]
        text: Text | None = self.get_current_text()
        if text is None: return
        text.underline_current_word()

    def is_text_collided(self) -> bool:
        current_text: Text | None = self.get_current_text()
        if current_text is None: return False
        is_collided: bool = current_text.get_current_word().rect.bottom > self.board.rect.height
        if is_collided: self.remove_fist_text()
        return is_collided

    def get_current_text(self) -> Text | None:
        if len(self.texts) == 0: return None
        return self.texts[0]

    def process_key_name(self, key_code: int) -> None:
        current_text: Text | None = self.get_current_text()
        if current_text is None: return
        if key_code == K_BACKSPACE:
            current_text.process_backspace()
        key_name: str = name(key_code)
        if len(key_name) != 1 or not key_name.isalpha(): return
        current_text.add_pressed_key(key_name)
        if current_text.get_current_word().is_correct():
            current_text.remove_word()
            current_text.update_counter_surface()
            self.level_manager.set_completed_words(self.level_manager.completed_words + 1)

    def end_game(self, lives_count: int) -> None:
        if lives_count == 0:
            self.game_over = True
