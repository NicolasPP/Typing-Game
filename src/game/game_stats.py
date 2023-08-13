from __future__ import annotations

from dataclasses import dataclass

from config.game_config import BASE_LIFE_POOL
from config.game_config import BASE_LIVES_COUNT
from config.game_config import MAX_LIFE_POOL
from config.game_config import SPAWN_DELAY
from config.game_config import BASE_SPEED
from config.game_config import BASE_COMBO_SPEED
from config.game_config import BASE_COMBO_MULTIPLIER
from config.game_config import MAX_COMBO_MULTIPLIER
from config.game_config import BASE_WORDS_PER_LEVEL
from config.game_config import BASE_WORD_LENGTH
from config.game_config import BASE_TEXT_LENGTH
from config.game_config import MAX_TEXT_LENGTH
from utils.callback_vars import BoolCB
from utils.callback_vars import FloatCB
from utils.callback_vars import IntCB
from utils.word_data_manager import WordDataManager

@dataclass
class Stats:
    level_num: IntCB
    words_required: IntCB
    life_pool: IntCB
    lives: IntCB
    spawn_delay: FloatCB
    fall_speed: FloatCB
    word_length: IntCB
    text_length: IntCB
    game_over: BoolCB
    combo_speed: FloatCB
    combo_fill: FloatCB
    combo_multiplier: FloatCB


class GameStats:
    stats: Stats | None = None

    @staticmethod
    def get() -> Stats:
        if GameStats.stats is None:
            GameStats.stats = GameStats.get_base_stats()
        return GameStats.stats

    @staticmethod
    def get_base_stats() -> Stats:
        level_num: IntCB = IntCB(0)
        words_required: IntCB = IntCB(BASE_WORDS_PER_LEVEL)
        life_pool: IntCB = IntCB(BASE_LIFE_POOL)
        lives: IntCB = IntCB(BASE_LIVES_COUNT)
        spawn_delay: FloatCB = FloatCB(SPAWN_DELAY)
        fall_speed: FloatCB = FloatCB(BASE_SPEED)
        word_length: IntCB = IntCB(BASE_WORD_LENGTH)
        text_length: IntCB = IntCB(BASE_TEXT_LENGTH)
        game_over: BoolCB = BoolCB(False)
        combo_speed: FloatCB = FloatCB(BASE_COMBO_SPEED)
        combo_fill: FloatCB = FloatCB(0.0)
        combo_multiplier: FloatCB = FloatCB(BASE_COMBO_MULTIPLIER)

        word_length.set_limit(BASE_WORD_LENGTH, max(WordDataManager.words_by_length.keys()))
        text_length.set_limit(BASE_TEXT_LENGTH, MAX_TEXT_LENGTH)
        life_pool.set_limit(BASE_LIFE_POOL, MAX_LIFE_POOL)
        combo_multiplier.set_limit(BASE_COMBO_MULTIPLIER, MAX_COMBO_MULTIPLIER)
        lives.set_limit(None, BASE_LIFE_POOL)
        life_pool.add_callback(lambda val: lives.set_limit(None, val))
        return Stats(level_num, words_required, life_pool, lives, spawn_delay, fall_speed, word_length, text_length,
                     game_over, combo_speed, combo_fill, combo_multiplier)

    @staticmethod
    def reset(board_width: int) -> None:
        GameStats.get().level_num.set(0)
        GameStats.get().words_required.set(BASE_WORDS_PER_LEVEL)
        GameStats.get().life_pool.set(BASE_LIFE_POOL)
        GameStats.get().lives.set(BASE_LIVES_COUNT)
        GameStats.get().spawn_delay.set(SPAWN_DELAY)
        GameStats.get().fall_speed.set(BASE_SPEED)
        GameStats.get().word_length.set(BASE_WORD_LENGTH)
        GameStats.get().text_length.set(BASE_TEXT_LENGTH)
        GameStats.get().game_over.set(False)
        GameStats.get().combo_speed.set(BASE_COMBO_SPEED)
        GameStats.get().combo_fill.set(float(board_width))
        GameStats.get().combo_multiplier.set(BASE_COMBO_MULTIPLIER)
