from random import randrange

from pygame import Surface
from pygame.font import Font
from pygame.math import Vector2

from config.game_config import DEFAULT_FONT_SIZE
from game.components.word import Word
from utils.fonts import FontManager
from utils.themes import Theme
from utils.themes import ThemeManager


class Text:

    def __init__(self, word_values: list[str]) -> None:
        self.words: list[Word] = [Word(value) for value in word_values]
        self.counter_surface: Surface | None = None
        self.update_counter_surface()
        self.score_worth: int = len(word_values)

    def update_counter_surface(self) -> None:
        font: Font = FontManager.get_font(DEFAULT_FONT_SIZE // 2)
        theme: Theme = ThemeManager.get_theme()
        counter_render: Surface = font.render(str(len(self.words)), True, theme.background_primary)
        self.counter_surface = counter_render

    def get_current_word(self) -> Word:
        assert len(self.words) != 0, "no more words left !"
        return self.words[-1]

    def set_pos(self, pos: Vector2) -> None:
        for word in self.words:
            word.set_pos(pos)

    def fall(self, delta_time: float) -> None:
        for word in self.words:
            word.fall(delta_time)

    def render(self, parent_surface: Surface) -> None:
        if self.counter_surface is None: return
        current_word: Word = self.get_current_word()
        current_word.render(parent_surface)
        if len(self.words) == 1: return
        parent_surface.blit(self.counter_surface, self.counter_surface.get_rect(midtop=current_word.rect.midbottom))

    def is_done(self) -> bool:
        return len(self.words) == 0

    def set_random_pos(self, board_width) -> None:
        current_word: Word = self.get_current_word()
        random_pos: Vector2 = Vector2(randrange(0, board_width - current_word.rect.width),
                                      -1 * current_word.rect.height)
        self.set_pos(random_pos)

    def underline_current_word(self) -> None:
        self.get_current_word().underline()

    def process_backspace(self) -> None:
        self.get_current_word().delete_char()

    def add_pressed_key(self, key_name: str) -> None:
        self.get_current_word().add_char(key_name)

    def remove_word(self) -> None:
        self.words = self.words[:len(self.words) - 1]
        if len(self.words) == 0: return
        self.underline_current_word()
