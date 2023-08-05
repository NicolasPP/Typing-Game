from enum import Enum
from enum import auto

from pygame import Rect
from pygame import Surface
from pygame.font import Font

from utils.fonts import FontManager
from utils.themes import ThemeManager
from config.game_config import DEFAULT_LETTER_SIZE

class LetterState(Enum):
    RIGHT = auto()
    WRONG = auto()
    EMPTY = auto()


class Letter:
    state_colors: dict[LetterState, tuple[int, int, int]] = {}

    @staticmethod
    def load_state_colors() -> None:
        Letter.state_colors[LetterState.RIGHT] = (0, 255, 0)
        Letter.state_colors[LetterState.WRONG] = (255, 0, 0)
        Letter.state_colors[LetterState.EMPTY] = ThemeManager.get_theme().background_primary

    def __init__(self, letter: str) -> None:
        assert len(letter) == 1, "letter cannot be longer than one char"
        self.val: str = letter
        self.state: LetterState = LetterState.EMPTY
        self.surface: Surface = self.create_surface()
        self.rect: Rect = Rect(0, 0, *self.surface.get_size())

    def create_surface(self) -> Surface:
        font: Font = FontManager.get_font(DEFAULT_LETTER_SIZE)
        anti_alias: bool = True
        color: tuple[int, int, int] | None = Letter.state_colors.get(self.state)
        assert color is not None, f"state's {self.state.name} color value has not been loaded"
        return font.render(self.val, anti_alias, color, ThemeManager.get_theme().foreground_primary)

    def set_state(self, state: LetterState) -> None:
        self.state = state
        self.surface = self.create_surface()

    def render(self, parent_surface: Surface) -> None:
        parent_surface.blit(self.surface, self.rect)
