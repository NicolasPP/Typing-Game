from pygame import Rect
from pygame import Surface
from pygame import draw
from pygame.math import Vector2

from config.game_config import OUTLINE_THICKNESS
from game.components.letter import Letter
from game.components.letter import LetterState
from game.game_stats import GameStats
from utils.themes import ThemeManager


class Word:
    def __init__(self, word: str) -> None:
        self.typed_value: str = ""
        self.letters: list[Letter] = [Letter(char) for char in word]
        self.surface: Surface = self.create_surface()
        self.rect: Rect = Rect(0, 0, *self.surface.get_size())
        self.pos: Vector2 = Vector2(0, 0)
        self.pressed_key_index: int = 0
        ThemeManager.add_call_back(self.update_word_theme)

    def update_word_theme(self) -> None:
        self.surface = self.create_surface()

    def add_char(self, key: str) -> bool:
        if self.pressed_key_index >= len(self.letters): return False
        result: bool = self.letters[self.pressed_key_index].val == key
        if result:
            self.set_letter_state(self.pressed_key_index, LetterState.RIGHT)
            self.pressed_key_index += 1
            self.typed_value += key
        else:
            self.set_letter_state(self.pressed_key_index, LetterState.WRONG)

        return result

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

    def fall(self, delta_time: float) -> None:
        distance: float = delta_time * GameStats.get().fall_speed.get()
        self.set_pos(self.pos + Vector2(0, distance))

    def underline(self, start_index: int = 0) -> None:
        if start_index >= len(self.letters) or start_index < 0: return
        start_rect: Rect = self.letters[start_index].rect
        draw.line(self.surface, ThemeManager.get_theme().background_primary, start_rect.bottomleft,
                  self.surface.get_rect().bottomright, OUTLINE_THICKNESS)

    def is_correct(self) -> bool:
        letters_size: int = len(self.letters)
        if letters_size != len(self.typed_value): return False
        for letter_index in range(letters_size):
            if self.typed_value[letter_index] != self.letters[letter_index].val: return False
        return True
