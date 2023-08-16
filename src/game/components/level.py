from dataclasses import dataclass
from enum import Enum
from enum import auto
from functools import partial
from random import choice

from pygame import Rect
from pygame import Surface
from pygame.event import Event
from pygame.font import Font

from config.game_config import BACKGROUND_ALPHA
from config.game_config import BASE_WORDS_PER_LEVEL
from config.game_config import BG_FADE_SPEED
from config.game_config import DEBUFF_FONT_SIZE
from config.game_config import DEFAULT_FONT_SIZE
from config.game_config import GUI_GAP
from config.game_config import REQUIRED_WORDS_ALPHA
from config.game_config import ROLL_FADE_SPEED
from config.game_config import ROLL_GAP
from config.game_config import WORDS_REQ_FADE_SPEED
from config.theme_config import DEBUFF_COLOR
from game.components.text import Text
from game.game_modifier import GameModifier
from game.game_modifier import StatModifier
from game.game_stats import GameStats
from game.game_stats import Stats
from gui.button_gui import ButtonEvent
from gui.button_gui import ButtonGui
from utils.fonts import FontManager
from utils.themes import Theme
from utils.themes import ThemeManager
from utils.word_data_manager import WordDataManager


class LevelState(Enum):
    PLAYING = auto()
    HIDE_REQ_NUM = auto()
    SHOW_BUFF_ROLL = auto()
    SHOW_DEBUFF_ROLL = auto()
    HIDE_ALL_ROLLS = auto()
    SHOW_REQ_NUM = auto()


class FadeDirection(Enum):
    IN = auto()
    OUT = auto()


@dataclass
class FadeInfo:
    direction: FadeDirection
    min_alpha: int
    max_alpha: int
    speed: float


@dataclass
class LevelEntity:
    fade_info: FadeInfo
    req_render: bool = True
    surface: Surface | None = None
    rect: Rect | None = None
    alpha: float = float(REQUIRED_WORDS_ALPHA)

    def render(self, board_surface: Surface) -> None:
        if self.surface is None: return
        if self.rect is None: return
        if not self.req_render: return
        board_surface.blit(self.surface, self.rect)

    def fade_overtime(self, delta_time: float) -> bool:
        diff: float = self.fade_info.speed * delta_time
        if self.fade_info.direction is FadeDirection.IN:
            self.alpha += diff
        else:
            self.alpha -= diff

        if self.fade_info.direction is FadeDirection.IN:
            if self.alpha >= self.fade_info.max_alpha:
                self.alpha = self.fade_info.max_alpha
                return True
        else:
            if self.alpha <= self.fade_info.min_alpha:
                self.alpha = self.fade_info.min_alpha
                return True

        assert self.surface is not None
        self.surface.set_alpha(int(self.alpha))
        return False


@dataclass
class Roll:
    buttons: list[ButtonGui]
    mods: list[StatModifier]
    entity: LevelEntity

    def render(self, board_surface: Surface, board_rect: Rect) -> None:
        if self.entity.surface is None: return
        self.entity.surface.fill(ThemeManager.get_theme().foreground_primary)
        for button in self.buttons:
            button.render(self.entity.surface, self.get_offset(board_rect))
        self.entity.render(board_surface)

    def get_offset(self, board_rect: Rect) -> tuple[int, int]:
        assert self.entity.rect is not None, "missing entity rect"
        return board_rect.x + self.entity.rect.x, board_rect.y + self.entity.rect.y


class LevelManager:
    def __init__(self, board_rect: Rect) -> None:
        self.board_rect: Rect = board_rect
        self.words_per_level: int = BASE_WORDS_PER_LEVEL
        self.played_words: list[str] = []
        self.parse_button_events = False
        self.buff_roll: Roll | None = None
        self.debuff_roll: Roll | None = None
        self.words_req: LevelEntity = LevelEntity(
            FadeInfo(FadeDirection.OUT, 0, REQUIRED_WORDS_ALPHA, WORDS_REQ_FADE_SPEED))
        self.background: LevelEntity = LevelEntity(FadeInfo(FadeDirection.IN, 0, BACKGROUND_ALPHA, BG_FADE_SPEED),
                                                   req_render=False)
        self.state: LevelState = LevelState.PLAYING
        self.is_rolling: bool = False

        stats: Stats = GameStats.get()
        self.update_word_req(GameStats.get().words_required.get())
        self.update_background()
        stats.words_required.add_callback(self.update_word_req)
        ThemeManager.add_call_back(self.update_level_theme)

    def update_level_theme(self) -> None:
        stats: Stats = GameStats.get()
        self.update_word_req(stats.words_required.get())
        self.update_background()

    def update_background(self) -> None:
        surface: Surface = Surface(self.board_rect.size)
        surface.fill(ThemeManager.get_theme().foreground_primary)
        surface.set_alpha(self.background.fade_info.max_alpha)
        self.background.surface = surface
        self.background.rect = surface.get_rect()

    def reset(self) -> None:
        self.words_req.req_render = True
        self.words_per_level = BASE_WORDS_PER_LEVEL

    def parse_event(self, event: Event) -> None:
        if not self.parse_button_events: return
        if self.buff_roll is not None:
            for button in self.buff_roll.buttons:
                button.parse_event(event, self.buff_roll.get_offset(self.board_rect))

    def update_word_req(self, words_req: int) -> None:
        if words_req == 0: self.set_is_rolling(True)
        font: Font = FontManager.get_font(DEFAULT_FONT_SIZE * 6)
        theme: Theme = ThemeManager.get_theme()
        surface: Surface = font.render(str(words_req), True, theme.background_primary, theme.foreground_primary)
        surface.set_alpha(int(self.words_req.alpha))
        self.words_req.surface = surface
        self.words_req.rect = surface.get_rect(center=(self.board_rect.w // 2, self.board_rect.h // 2))

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
            if self.words_req.fade_overtime(delta_time):
                self.words_req.fade_info.direction = FadeDirection.IN
                GameStats.get().words_required.set(self.words_per_level)
                self.state = LevelState.SHOW_BUFF_ROLL
                self.words_per_level += BASE_WORDS_PER_LEVEL
                self.words_req.req_render = False
                self.parse_button_events = True
                self.background.req_render = True

        elif self.state is LevelState.SHOW_BUFF_ROLL:
            if self.buff_roll is None: self.set_buff_roll()
            assert self.buff_roll is not None, "buff roll object is missing"
            self.buff_roll.entity.fade_overtime(delta_time)
            self.background.fade_overtime(delta_time)

        elif self.state is LevelState.SHOW_DEBUFF_ROLL:
            if self.debuff_roll is None: self.set_debuff_roll()
            assert self.debuff_roll is not None, "debuff roll object is missing"
            assert self.buff_roll is not None, "debuff roll object is missing"
            if self.debuff_roll.entity.fade_overtime(delta_time):
                self.state = LevelState.HIDE_ALL_ROLLS
                self.background.fade_info.direction = FadeDirection.OUT
                self.debuff_roll.entity.fade_info.direction = FadeDirection.OUT
                self.buff_roll.entity.fade_info.direction = FadeDirection.OUT
                for mod in self.debuff_roll.mods: mod.apply()

        elif self.state is LevelState.HIDE_ALL_ROLLS:
            assert self.buff_roll is not None, "buff roll object is missing"
            assert self.debuff_roll is not None, "debuff roll object is missing"
            self.background.fade_overtime(delta_time)
            is_buff_fade_done: bool = self.buff_roll.entity.fade_overtime(delta_time)
            is_debuff_fade_done: bool = self.debuff_roll.entity.fade_overtime(delta_time)
            if is_buff_fade_done and is_debuff_fade_done:
                self.state = LevelState.SHOW_REQ_NUM
                self.background.fade_info.direction = FadeDirection.IN
                self.buff_roll = None
                self.debuff_roll = None
                self.words_req.req_render = True
                self.background.req_render = False

        elif self.state is LevelState.SHOW_REQ_NUM:
            if self.words_req.fade_overtime(delta_time):
                self.words_req.fade_info.direction = FadeDirection.OUT
                self.state = LevelState.PLAYING
                self.set_is_rolling(False)

    def set_debuff_roll(self) -> None:
        debuffs: list[StatModifier] = GameModifier.roll_debuffs()
        assert len(debuffs) == 3, "must roll 3 debuffs"

        buttons: list[ButtonGui] = []
        for debuff in debuffs:
            button: ButtonGui = ButtonGui(debuff.name)
            button.configure(is_hover_enabled=False, label_color=DEBUFF_COLOR, font_size=DEBUFF_FONT_SIZE)
            buttons.append(button)

        fade_info: FadeInfo = FadeInfo(FadeDirection.IN, 0, 255, ROLL_FADE_SPEED)

        max_width_button: ButtonGui = max(buttons, key=lambda b: b.rect.width)
        width: int = max_width_button.rect.width + (ROLL_GAP * 2)
        height: int = (ROLL_GAP * 4) + sum([b.rect.h for b in buttons])
        surface: Surface = Surface((width, height))

        rect: Rect = surface.get_rect(midtop=(self.board_rect.w // 2, self.board_rect.h // 2))
        rect.y += GUI_GAP
        surface.set_alpha(fade_info.min_alpha)

        max_width_button.rect.topleft = ROLL_GAP, ROLL_GAP

        prev_rect = None
        for button in buttons:
            if button == max_width_button: continue
            if prev_rect is None:
                button.rect.midtop = max_width_button.rect.midbottom
            else:
                button.rect.midtop = prev_rect.midbottom

            button.rect.y += ROLL_GAP
            prev_rect = button.rect

        surface.fill(ThemeManager.get_theme().foreground_primary)

        entity: LevelEntity = LevelEntity(fade_info, surface=surface, rect=rect, alpha=0.0)
        self.debuff_roll = Roll(buttons, debuffs, entity)

    def set_buff_roll(self) -> None:
        buffs: list[StatModifier] = GameModifier.roll_buffs()
        assert len(buffs) == 3, "must roll 3 buffs"

        buttons: list[ButtonGui] = []
        for buff in buffs:
            button: ButtonGui = ButtonGui(buff.name)
            button.configure(label_color=ThemeManager.get_theme().background_primary)
            button.add_call_back(ButtonEvent.LEFT_CLICK, partial(self.buff_button_click, buff))
            buttons.append(button)
        fade_info: FadeInfo = FadeInfo(FadeDirection.IN, 0, 255, ROLL_FADE_SPEED)

        height: int = (ROLL_GAP * 3) + (max([b.rect.h for b in buttons]) * 2)
        width: int = (ROLL_GAP * 3) + (sum([b.rect.w for b in buttons]) - max([b.rect.w for b in buttons]))
        surface: Surface = Surface((width, height))

        rect: Rect = surface.get_rect(midbottom=(self.board_rect.w // 2, self.board_rect.h // 2))
        rect.y -= GUI_GAP
        surface.set_alpha(fade_info.min_alpha)

        max_width_button: ButtonGui = max(buttons, key=lambda b: b.rect.w)
        prev_rect: Rect | None = None
        for button in buttons:
            if button == max_width_button: continue
            if prev_rect is None:
                button.rect.topleft = (ROLL_GAP, ROLL_GAP)
            else:
                button.rect.midleft = prev_rect.midright
                button.rect.x += ROLL_GAP
            prev_rect = button.rect

        assert prev_rect is not None
        max_width_button.rect.center = rect.w // 2, rect.h // 2
        max_width_button.rect.top = prev_rect.bottom
        max_width_button.rect.y += ROLL_GAP

        surface.fill(ThemeManager.get_theme().foreground_primary)

        entity: LevelEntity = LevelEntity(fade_info, surface=surface, rect=rect, alpha=0.0)
        self.buff_roll = Roll(buttons, buffs, entity)

    def render(self, board_surface: Surface) -> None:

        self.background.render(board_surface)
        self.words_req.render(board_surface)

        if self.buff_roll is not None:
            self.buff_roll.render(board_surface, self.board_rect)

        if self.debuff_roll is not None:
            self.debuff_roll.render(board_surface, self.board_rect)

    def buff_button_click(self, mod: StatModifier) -> None:
        assert self.buff_roll is not None, "buff roll obj missing"
        assert self.buff_roll.entity.surface is not None, "buff roll obj surface missing"
        self.state = LevelState.SHOW_DEBUFF_ROLL
        self.buff_roll.entity.alpha = self.buff_roll.entity.fade_info.max_alpha
        self.buff_roll.entity.surface.set_alpha(self.buff_roll.entity.fade_info.max_alpha)
        self.parse_button_events = False
        mod.apply()


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
