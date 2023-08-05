from pygame import Rect
from pygame import Surface

from game.components.letter import Letter
from game.components.letter import LetterState
from utils.accumulator import Accumulator
from utils.word_data_manager import WordDataManager
from config.game_config import SPAWN_DELAY


class Word:
    def __init__(self, word: str) -> None:
        self.value: str = word
        self.letters: list[Letter] = [Letter(char) for char in word]
        self.surface: Surface = self.create_surface()
        self.rect: Rect = Rect(0, 0, *self.surface.get_size())

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


class WordManager:
    def __init__(self) -> None:
        self.words: list[Word] = []
        self.played_words: set[str] = set()
        self.spawn_accumulator: Accumulator = Accumulator(SPAWN_DELAY)
        self.stop_spawning: bool = False

    def spawn_word(self, delta_time: float) -> None:
        if self.stop_spawning: return
        if not self.spawn_accumulator.wait(delta_time): return
        word: str = WordDataManager.get_random_word()
        self.played_words.add(word)
        self.words.append(Word(word))
