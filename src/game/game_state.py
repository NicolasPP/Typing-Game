from random import randrange

from pygame import KEYDOWN
from pygame import K_BACKSPACE
from pygame.event import Event
from pygame.key import name
from pygame.math import Vector2

from config.game_config import SPAWN_DELAY
from game.components.board import Board
from game.components.level import LevelManager
from game.components.word import Word
from gui.gui_manager import GuiManager
from gui.gui_vars import GuiVars
from utils.accumulator import Accumulator
from utils.word_data_manager import WordDataManager


class GameState:

    def __init__(self, board_width: int, board_height: int) -> None:
        self.board: Board = Board(board_width, board_height)
        self.level_manager: LevelManager = LevelManager()
        self.gui_manager: GuiManager = GuiManager(self.board.rect)
        self.words: list[Word] = []
        self.played_words: list[str] = []
        self.spawn_accumulator: Accumulator = Accumulator(SPAWN_DELAY)
        self.stop_spawning: bool = False
        self.game_over: bool = False
        self.current_word: Word | None = None
        GuiVars.lives.add_callback(self.end_game)

    def render(self) -> None:
        self.board.clear()
        for word in self.words:
            word.render(self.board.surface)
        self.board.render()
        self.gui_manager.render()

    def update(self, delta_time: float) -> None:
        if self.game_over: return
        if self.spawn_accumulator.wait(delta_time):
            self.spawn_word()

        # update words
        for word in self.words:
            word.fall(delta_time, self.level_manager.get_speed())

        current_word: Word | None = self.get_current_word()
        if current_word is None: return
        if current_word.is_correct():
            self.level_manager.set_completed_words(self.level_manager.completed_words + 1)
            self.remove_first_word()

        if self.is_word_collided():
            GuiVars.lives.set(GuiVars.lives.get() - 1)

    def parse_player_input(self, game_event: Event):
        if game_event.type == KEYDOWN:
            self.process_key_name(game_event.key)

    def add_word(self, word_value: str) -> None:
        self.played_words.append(word_value)
        word: Word = Word(word_value)
        word.set_pos(Vector2(Vector2(randrange(0, self.board.rect.width - word.rect.width), -1 * word.rect.height)))
        if len(self.words) == 0: word.underline()
        self.words.append(word)

    def spawn_word(self) -> None:
        if self.stop_spawning: return
        word_val: str = WordDataManager.get_random_word(word_lengths=self.level_manager.get_word_lengths())
        self.add_word(word_val)

    def remove_first_word(self) -> None:
        self.words = self.words[1:]
        word: Word | None = self.get_current_word()
        if word is None: return
        word.underline()

    def is_word_collided(self) -> bool:
        current_word: Word | None = self.get_current_word()
        if current_word is None: return False
        is_collided: bool = self.words[0].rect.bottom > self.board.rect.height
        if is_collided: self.remove_first_word()
        return is_collided

    def get_current_word(self) -> Word | None:
        if len(self.words) == 0: return None
        return self.words[0]

    def process_key_name(self, key_code: int) -> None:
        current_word: Word | None = self.get_current_word()
        if current_word is None: return
        if key_code == K_BACKSPACE:
            current_word.process_backspace()
        key_name: str = name(key_code)
        if len(key_name) != 1 or not key_name.isalpha(): return
        current_word.add_pressed_key(key_name)

    def end_game(self, lives_count: int) -> None:
        if lives_count == 0:
            self.game_over = True
