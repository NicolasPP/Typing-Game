from dataclasses import dataclass
from enum import Enum
from enum import auto
from math import ceil
from random import choice

from pygame import Rect
from pygame import Surface
from pygame.event import Event
from pygame.font import Font

from config.game_config import BASE_WORDS_PER_LEVEL
from config.game_config import DEFAULT_FONT_SIZE
from config.game_config import FADE_SPEED
from config.game_config import GUI_GAP
from config.game_config import REQUIRED_WORDS_ALPHA
from config.game_config import ROLL_SIZE_RATIO
from game.components.text import Text
from game.game_modifier import GameModifier
from game.game_modifier import StatModifier
from game.game_stats import GameStats
from game.game_stats import Stats
from gui.button_gui import ButtonGui
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


class FadeDirection(Enum):
    IN = auto()
    OUT = auto()


@dataclass
class FadeInfo:
    direction: FadeDirection
    min_alpha: int
    max_alpha: float
    speed: float


@dataclass
class WordsReq:
    fade_info: FadeInfo
    render: bool = True
    surface: Surface | None = None
    alpha: float = float(REQUIRED_WORDS_ALPHA)


@dataclass
class Roll:
    surface: Surface
    buffs: list[ButtonGui]
    debuffs: list[ButtonGui]
    fade_info: FadeInfo
    rect: Rect
    alpha: float = 0.0


class LevelManager:
    def __init__(self, board_rect: Rect) -> None:
        self.board_rect: Rect = board_rect
        self.words_per_level: int = BASE_WORDS_PER_LEVEL
        self.played_words: list[str] = []
        self.roll: Roll | None = None
        self.words_req: WordsReq = WordsReq(FadeInfo(FadeDirection.OUT, 0, REQUIRED_WORDS_ALPHA, FADE_SPEED))
        self.state: LevelState = LevelState.PLAYING
        self.is_rolling: bool = False

        stats: Stats = GameStats.get()
        self.update_word_req(GameStats.get().words_required.get())
        stats.words_required.add_callback(self.update_word_req)

        word_req_name: str = "update words required theme"
        ThemeManager.add_call_back(lambda: self.update_word_req(stats.words_required.get()), name=word_req_name)

    def reset(self) -> None:
        self.words_req.render = True
        self.words_per_level = BASE_WORDS_PER_LEVEL

    def parse_event(self, event: Event) -> None:
        if self.roll is not None:
            for button in self.roll.buffs + self.roll.debuffs:
                button.parse_event(event, self.get_roll_surface_offset())

    def update_word_req(self, words_req: int) -> None:
        if words_req == 0: self.set_is_rolling(True)
        font: Font = FontManager.get_font(DEFAULT_FONT_SIZE * 6)
        theme: Theme = ThemeManager.get_theme()
        surface: Surface = font.render(str(words_req), True, theme.background_primary, theme.foreground_primary)
        surface.set_alpha(int(self.words_req.alpha))
        self.words_req.surface = surface

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
            is_fade_done: bool = fade_overtime(self.words_req, delta_time)
            if is_fade_done:
                self.words_req.fade_info.direction = FadeDirection.IN
                self.state = LevelState.SHOW_ROLL
                self.words_req.render = False
                self.words_per_level += BASE_WORDS_PER_LEVEL
                GameStats.get().words_required.set(self.words_per_level)

        elif self.state is LevelState.SHOW_ROLL:
            if self.roll is None: self.set_roll()
            assert self.roll is not None, "roll object is missing"
            is_fade_done: bool = fade_overtime(self.roll, delta_time)
            # if is_fade_done:
                # self.state = LevelState.HIDE_ROLL
                # self.roll.fade_info.direction = FadeDirection.OUT

        elif self.state is LevelState.HIDE_ROLL:
            assert self.roll is not None, "roll object is missing"
            is_fade_done: bool = fade_overtime(self.roll, delta_time)
            if is_fade_done:
                self.state = LevelState.SHOW_REQ_NUM
                self.roll = None
                self.words_req.render = True

        elif self.state is LevelState.SHOW_REQ_NUM:
            is_fade_done: bool = fade_overtime(self.words_req, delta_time)
            if is_fade_done:
                self.state = LevelState.PLAYING
                self.set_is_rolling(False)

    def set_roll(self) -> None:
        buffs: list[StatModifier] = GameModifier.roll_buffs()
        debuffs: list[StatModifier] = GameModifier.roll_debuffs()
        debuff_buttons: list[ButtonGui] = [ButtonGui(debuff.name) for debuff in debuffs]
        buff_buttons: list[ButtonGui] = [ButtonGui(buff.name) for buff in buffs]
        fade_info: FadeInfo = FadeInfo(FadeDirection.IN, 0, 255, FADE_SPEED * 2)
        width, height = ceil(self.board_rect.width * ROLL_SIZE_RATIO), ceil(self.board_rect.height * ROLL_SIZE_RATIO)
        surface: Surface = Surface((width, height))
        rect: Rect = surface.get_rect(center=(self.board_rect.w // 2, self.board_rect.h // 2))
        surface.set_alpha(fade_info.min_alpha)

        prev_rect: Rect | None = None
        for button in buff_buttons + debuff_buttons:
            button.configure(font_size=20)
            if prev_rect is None:
                button.rect.midtop = rect.w // 2, 0
            else:
                button.rect.midtop = prev_rect.midbottom

            button.rect.y += (GUI_GAP * 2)
            prev_rect = button.rect

        surface.fill('red')
        self.roll = Roll(surface, buff_buttons, debuff_buttons, fade_info, rect)

    def render(self, board_surface: Surface) -> None:
        if self.words_req.surface is None: return
        if self.words_req.render:
            pos: Rect = self.words_req.surface.get_rect(center=(self.board_rect.w // 2, self.board_rect.h // 2))
            board_surface.blit(self.words_req.surface, pos)

        if self.roll is not None:
            self.roll.surface.fill('red')
            for button in self.roll.buffs + self.roll.debuffs:
                button.render(self.roll.surface, self.get_roll_surface_offset())
            board_surface.blit(self.roll.surface, self.roll.rect)

    def get_roll_surface_offset(self) -> tuple[int, int]:
        assert self.roll is not None, "roll object missing"
        return self.board_rect.x + self.roll.rect.x, self.board_rect.y + self.roll.rect.y


def fade_overtime(fade_obj: WordsReq | Roll, delta_time: float) -> bool:
    if fade_obj.fade_info.direction is FadeDirection.IN:
        if fade_obj.alpha >= fade_obj.fade_info.max_alpha:
            fade_obj.alpha = fade_obj.fade_info.max_alpha
            return True
    else:
        if fade_obj.alpha <= fade_obj.fade_info.min_alpha:
            fade_obj.alpha = fade_obj.fade_info.min_alpha
            return True

    diff: float = fade_obj.fade_info.speed * delta_time
    if fade_obj.fade_info.direction is FadeDirection.IN:
        fade_obj.alpha += diff
    else:
        fade_obj.alpha -= diff

    fade_obj.surface.set_alpha(int(fade_obj.alpha))
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
