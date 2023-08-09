from pygame import KEYDOWN
from pygame import K_BACKSPACE
from pygame import MOUSEBUTTONDOWN
from pygame.event import Event
from pygame.key import name

from game.components.board import Board
from game.components.level import LevelManager
from game.components.text import Text
from game.game_stats import GameStats
from game.game_stats import Stats
from gui.gui_manager import GuiManager
from utils.accumulator import Accumulator
from utils.word_data_manager import WordDataManager


class GameState:

    def __init__(self, board_width: int, board_height: int) -> None:
        self.board: Board = Board(board_width, board_height)
        self.gui_manager: GuiManager = GuiManager(self.board.rect)
        self.spawn_accumulator: Accumulator = Accumulator(GameStats.get().spawn_delay.get())

        self.texts: list[Text] = []
        self.played_words: list[str] = []

        self.stop_spawning: bool = False
        self.game_over: bool = False
        self.current_text: Text | None = None

        GameStats.get().lives.add_callback(self.end_game)

    def render(self) -> None:
        self.board.clear()
        if not GameStats.get().game_over.get():
            for text in self.texts:
                text.render(self.board.surface)
        self.board.render()
        self.gui_manager.render()

    def update(self, delta_time: float) -> None:
        stats: Stats = GameStats.get()
        if stats.game_over.get():
            self.gui_manager.update()
            return

        if self.spawn_accumulator.wait(delta_time):
            self.spawn_text()

        # update words
        for text in self.texts:
            text.fall(delta_time)

        current_text: Text | None = self.get_current_text()
        if current_text is None: return
        if current_text.is_done():
            self.remove_fist_text()

        if self.is_text_collided():
            stats.lives.set(stats.lives.get() - len(current_text.words))

    def parse_player_input(self, game_event: Event):
        if game_event.type == KEYDOWN:
            self.process_key_name(game_event.key)

        if game_event.type == MOUSEBUTTONDOWN:
            if self.gui_manager.game_over.is_try_again_collided:
                self.texts.clear()
                GameStats.reset()

    def add_text(self, word_values: list[str]) -> None:
        text: Text = Text(word_values)
        text.set_random_pos(self.board.rect.width)
        if len(self.texts) == 0: text.underline_current_word()
        self.texts.append(text)

    def spawn_text(self) -> None:
        if self.stop_spawning: return
        word_values: list[str] = []

        text_length: int = LevelManager.roll_text_length()
        word_lengths: list[int] = LevelManager.roll_word_lengths()

        while len(word_values) < text_length:
            word_val: str = WordDataManager.get_random_word(played_words=self.played_words, word_lengths=word_lengths)
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
            GameStats.get().words_right.set(GameStats.get().words_right.get() + 1)

    def end_game(self, lives_count: int) -> None:
        if lives_count <= 0:
            GameStats.get().game_over.set(True)
            self.board.clear()
