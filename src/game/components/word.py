from pygame import Rect
from pygame import Surface

from game.components.letter import Letter
from game.components.letter import LetterState


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
