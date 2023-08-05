from random import randrange

from pygame import Rect
from pygame import Surface
from pygame.math import Vector2

from config.game_config import SPAWN_DELAY
from game.components.letter import Letter
from game.components.letter import LetterState
from utils.accumulator import Accumulator
from utils.word_data_manager import WordDataManager


class Word:
    def __init__(self, word: str) -> None:
        self.value: str = word
        self.letters: list[Letter] = [Letter(char) for char in word]
        self.surface: Surface = self.create_surface()
        self.rect: Rect = Rect(0, 0, *self.surface.get_size())
        self.pos: Vector2 = Vector2(0, 0)

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


class WordManager:
    def __init__(self) -> None:
        self.words: list[Word] = []
        self.played_words: list[str] = []
        self.spawn_accumulator: Accumulator = Accumulator(SPAWN_DELAY)
        self.stop_spawning: bool = False

    def spawn_word(self, word_lengths: list[int], board_width: int) -> None:
        if self.stop_spawning: return
        word: str = WordDataManager.get_random_word(word_lengths=word_lengths)
        self.played_words.append(word)
        word_obj: Word = Word(word)
        word_pos: Vector2 = Vector2(Vector2(randrange(0, board_width - word_obj.rect.width), -1 * word_obj.rect.height))
        word_obj.set_pos(word_pos)
        self.words.append(word_obj)

    def render(self, parent_surface: Surface) -> None:
        for word in self.words:
            word.render(parent_surface)

    def update(self, delta_time: float, speed: float) -> None:
        for word in self.words:
            word.fall(delta_time, speed)

    def is_collided(self, board_height: int) -> bool:
        if len(self.words) == 0: return False
        is_collided: bool = self.words[0].rect.bottom > board_height
        if is_collided:
            self.words = self.words[1:]
        return is_collided
