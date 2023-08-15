from dataclasses import dataclass
from enum import Enum
from enum import auto
from random import choice

from pygame import Rect
from pygame import Surface
from pygame.font import Font

from config.game_config import BASE_WORDS_PER_LEVEL
from config.game_config import DEFAULT_FONT_SIZE
from config.game_config import FADE_SPEED
from config.game_config import REQUIRED_WORDS_ALPHA
from game.components.text import Text
from game.game_modifier import GameModifier
from game.game_modifier import StatModifier
from game.game_stats import GameStats
from game.game_stats import Stats
from utils.fonts import FontManager
from utils.themes import Theme
from utils.themes import ThemeManager
from utils.word_data_manager import WordDataManager


class LevelState(Enum):
    PLAYING = auto()
    HIDE_REQ_NUM = auto()
    SHOW_REQ_NUM = auto()
    SHOW_ROLL = auto()
    HIDE_ROLL = auto()


class Fade(Enum):
    IN = auto()
    OUT = auto()


@dataclass
class WordsReq:
    render: bool = False
    surface: Surface | None = None
    rect: Rect | None = None
    alpha: float = REQUIRED_WORDS_ALPHA


class LevelManager:
    def __init__(self, board_rect: Rect) -> None:
        self.board_rect: Rect = board_rect
        self.words_per_level: int = BASE_WORDS_PER_LEVEL
        self.played_words: list[str] = []
        self.words_req: WordsReq = WordsReq(render=True)
        self.state: LevelState = LevelState.PLAYING
        self.is_rolling: bool = False

        stats: Stats = GameStats.get()
        self.update_word_req(GameStats.get().words_required.get())
        stats.words_required.add_callback(self.update_word_req)
        ThemeManager.add_call_back(lambda: self.update_word_req(stats.words_required.get()), name="update "
                                                                                                  "words "
                                                                                                  "required theme")

    def reset(self) -> None:
        self.words_req.render = True
        self.words_per_level = BASE_WORDS_PER_LEVEL

    def update_word_req(self, words_req: int) -> None:
        if words_req == 0: self.set_is_rolling(True)
        font: Font = FontManager.get_font(DEFAULT_FONT_SIZE * 6)
        theme: Theme = ThemeManager.get_theme()
        surface: Surface = font.render(str(words_req), True, theme.background_primary, theme.foreground_primary)
        surface.set_alpha(int(self.words_req.alpha))

        self.words_req.surface = surface
        self.words_req.rect = surface.get_rect(center=(self.board_rect.width // 2, self.board_rect.height // 2))

    def set_is_rolling(self, is_rolling: bool) -> None:
        if is_rolling:
            self.state = LevelState.HIDE_REQ_NUM
        else:
            GameStats.get().level_num.increment(1)
        self.is_rolling = is_rolling
        GameStats.get().is_rolling.set(is_rolling)

    def get_text(self) -> Text:
        text_length: int = roll_text_length()
        word_lengths: list[int] = roll_word_lengths()
        word_values: list[str] = []
        while len(word_values) < text_length:
            word_val: str = WordDataManager.get_random_word(played_words=self.played_words, word_lengths=word_lengths)
            word_values.append(word_val)
            self.played_words.append(word_val)

        return Text(word_values)

    def update(self, delta_time: float) -> None:
        if self.state is LevelState.PLAYING:
            return

        elif self.state is LevelState.HIDE_REQ_NUM:
            is_fade_done: bool = self.fade_overtime(self.words_req.surface, delta_time, Fade.OUT)
            if is_fade_done:
                self.state = LevelState.SHOW_ROLL
                self.words_req.render = False
                self.words_per_level += BASE_WORDS_PER_LEVEL
                GameStats.get().words_required.set(self.words_per_level)

        elif self.state is LevelState.SHOW_REQ_NUM:

            is_fade_done: bool = self.fade_overtime(self.words_req.surface, delta_time, Fade.IN)
            if is_fade_done:
                self.state = LevelState.PLAYING
                self.set_is_rolling(False)

        elif self.state is LevelState.SHOW_ROLL:
            buff: StatModifier = choice(GameModifier.roll_buffs())
            buff.apply()
            print(f"buff: {buff.name}")
            debuffs: list[StatModifier] = GameModifier.roll_debuffs()
            for debuff in debuffs:
                debuff.apply()

            print("debuffs: ", end=' ')
            print(*[d.name for d in debuffs], sep=' ')

            self.state = LevelState.HIDE_ROLL

        elif self.state is LevelState.HIDE_ROLL:
            self.state = LevelState.SHOW_REQ_NUM
            self.words_req.render = True

    def render(self, board_surface: Surface) -> None:
        if self.words_req.surface is None or self.words_req.rect is None: return
        if self.words_req.render:
            board_surface.blit(self.words_req.surface, self.words_req.rect)

    def fade_overtime(self, surface: Surface, delta_time: float, fade: Fade) -> bool:
        if fade is Fade.IN:
            if self.words_req.alpha >= REQUIRED_WORDS_ALPHA:
                self.words_req.alpha = REQUIRED_WORDS_ALPHA
                return True
        else:
            if self.words_req.alpha <= 0.0:
                self.words_req.alpha = 0.0
                return True

        diff: float = FADE_SPEED * delta_time
        if fade is Fade.IN:
            self.words_req.alpha += diff
        else:
            self.words_req.alpha -= diff
        surface.set_alpha(int(self.words_req.alpha))

        return False


def roll_word_lengths() -> list[int]:
    max_len: int = max(WordDataManager.words_by_length.keys())
    start: int = GameStats.get().word_length.get()
    seg_length: int = 3

    if start + seg_length > max_len:
        diff: int = (start + seg_length) - max_len
        return list(range(start - diff + 1, max_len + 1))
    return list(range(start, start + seg_length))


def roll_text_length() -> int:
    possible_lengths: list = list(range(1, GameStats.get().text_length.get() + 1))
    choices: list[int] = []
    for length, freq in zip(possible_lengths, possible_lengths[::-1]):
        choices.extend([length] * freq)
    return choice(choices)
