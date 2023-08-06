from random import randrange
from typing import Callable

from pygame import K_BACKSPACE
from pygame import Rect
from pygame import Surface
from pygame.draw import line
from pygame.key import name
from pygame.math import Vector2

from config.game_config import OUTLINE_THICKNESS
from config.game_config import SPAWN_DELAY
from game.components.letter import Letter
from game.components.letter import LetterState
from utils.accumulator import Accumulator
from utils.themes import ThemeManager
from utils.word_data_manager import WordDataManager


class Word:
    def __init__(self, word: str) -> None:
        self.typed_value: str = ""
        self.letters: list[Letter] = [Letter(char) for char in word]
        self.surface: Surface = self.create_surface()
        self.rect: Rect = Rect(0, 0, *self.surface.get_size())
        self.pos: Vector2 = Vector2(0, 0)
        self.pressed_key_index: int = -1

    def process_backspace(self) -> None:
        if self.pressed_key_index == -1: return
        self.set_letter_state(self.pressed_key_index, LetterState.EMPTY)
        self.pressed_key_index -= 1
        typed_value_size: int = len(self.typed_value)
        if typed_value_size == 0: return
        self.typed_value = self.typed_value[:typed_value_size - 1]
        self.underline(len(self.typed_value))

    def add_pressed_key(self, key: str) -> None:
        if self.pressed_key_index + 1 >= len(self.letters): return
        self.pressed_key_index += 1
        self.typed_value += key
        letter: Letter = self.letters[self.pressed_key_index]
        if key == letter.val:
            self.set_letter_state(self.pressed_key_index, LetterState.RIGHT)
        else:
            self.set_letter_state(self.pressed_key_index, LetterState.WRONG)

    def set_pos(self, pos: Vector2) -> None:
        self.rect.x, self.rect.y = round(pos.x), round(pos.y)
        self.pos = pos

    def set_letter_state(self, index: int, state: LetterState):
        assert len(self.letters) > index >= 0, f"index: {index} out of bounds"
        letter: Letter = self.letters[index]
        letter.set_state(state)
        letter.render(self.surface)

    def create_surface(self) -> Surface:
        width: int = sum([letter.rect.width for letter in self.letters])
        height: int = max([letter.rect.height for letter in self.letters])
        surface: Surface = Surface((width, height))
        prev_rect: Rect | None = None
        for letter in self.letters:

            if prev_rect is None:
                prev_rect = letter.rect

            else:
                letter.rect.topleft = prev_rect.topright
                prev_rect = letter.rect

            letter.render(surface)

        return surface

    def render(self, parent_surface: Surface) -> None:
        parent_surface.blit(self.surface, self.rect)

    def fall(self, delta_time: float, speed: float) -> None:
        distance: float = delta_time * speed
        self.set_pos(self.pos + Vector2(0, distance))

    def underline(self, start_index: int = 0) -> None:
        if start_index >= len(self.letters) or start_index < 0: return
        start_rect: Rect = self.letters[start_index].rect
        line(self.surface, ThemeManager.get_theme().background_primary, start_rect.bottomleft,
             self.surface.get_rect().bottomright, OUTLINE_THICKNESS)

    def is_correct(self) -> bool:
        letters_size: int = len(self.letters)
        if letters_size != len(self.typed_value): return False
        for letter_index in range(letters_size):
            if self.typed_value[letter_index] != self.letters[letter_index].val: return False
        return True


class WordManager:
    def __init__(self) -> None:
        self.words: list[Word] = []
        self.played_words: list[str] = []
        self.spawn_accumulator: Accumulator = Accumulator(SPAWN_DELAY)
        self.stop_spawning: bool = False
        self.current_word: Word | None = None

    def add_word(self, word_value: str, board_width: int) -> None:
        self.played_words.append(word_value)
        word: Word = Word(word_value)
        word.set_pos(Vector2(Vector2(randrange(0, board_width - word.rect.width), -1 * word.rect.height)))
        if len(self.words) == 0: word.underline()
        self.words.append(word)

    def spawn_word(self, word_lengths: list[int], board_width: int) -> None:
        if self.stop_spawning: return
        word_val: str = WordDataManager.get_random_word(word_lengths=word_lengths)
        self.add_word(word_val, board_width)

    def render(self, parent_surface: Surface) -> None:
        for word in self.words:
            word.render(parent_surface)

    def update(self, delta_time: float, speed: float, inc_completed_words: Callable[[], None]) -> None:
        for word in self.words:
            word.fall(delta_time, speed)
        current_word: Word | None = self.get_current_word()
        if current_word is None: return
        if current_word.is_correct():
            inc_completed_words()
            self.remove_first_word()

    def remove_first_word(self) -> None:
        self.words = self.words[1:]
        word: Word | None = self.get_current_word()
        if word is None: return
        word.underline()

    def is_collided(self, board_height: int) -> bool:
        current_word: Word | None = self.get_current_word()
        if current_word is None: return False
        is_collided: bool = self.words[0].rect.bottom > board_height
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
