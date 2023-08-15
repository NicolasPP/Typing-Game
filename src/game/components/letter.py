from enum import Enum
from enum import auto

from pygame import Rect
from pygame import Surface
from pygame.font import Font

from config.game_config import LETTER_FONT_SIZE
from config.theme_config import CORRECT_COLOR
from config.theme_config import WRONG_COLOR
from utils.fonts import FontManager
from utils.themes import ThemeManager


class LetterState(Enum):
    RIGHT = auto()
    WRONG = auto()
    EMPTY = auto()


class Letter:
    state_colors: dict[LetterState, tuple[int, int, int]] = {}

    @staticmethod
    def load_state_colors() -> None:
        Letter.state_colors[LetterState.RIGHT] = CORRECT_COLOR
        Letter.state_colors[LetterState.WRONG] = WRONG_COLOR
        Letter.state_colors[LetterState.EMPTY] = ThemeManager.get_theme().background_primary

    def __init__(self, letter: str) -> None:
        assert len(letter) == 1, "letter cannot be longer than one char"
        self.val: str = letter
        self.state: LetterState = LetterState.EMPTY
        self.surface: Surface = self.create_surface()
        self.rect: Rect = Rect(0, 0, *self.surface.get_size())
        ThemeManager.add_call_back(self.update_letter_theme)

    def update_letter_theme(self) -> None:
        self.surface = self.create_surface()

    def create_surface(self) -> Surface:
        font: Font = FontManager.get_font(LETTER_FONT_SIZE)
        anti_alias: bool = True
        color: tuple[int, int, int] | None = Letter.state_colors.get(self.state)
        assert color is not None, f"state's {self.state.name} color value has not been loaded"
        return font.render(self.val, anti_alias, color, ThemeManager.get_theme().foreground_primary)

    def set_state(self, state: LetterState) -> None:
        self.state = state
        self.surface = self.create_surface()

    def render(self, parent_surface: Surface) -> None:
        parent_surface.blit(self.surface, self.rect)
