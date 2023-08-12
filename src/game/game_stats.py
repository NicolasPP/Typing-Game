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
from utils.callback_vars import BoolCB
from utils.callback_vars import FloatCB
from utils.callback_vars import IntCB


@dataclass
class Stats:
    words_right: IntCB
    words_wrong: IntCB
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
        words_right: IntCB = IntCB(0)
        words_wrong: IntCB = IntCB(0)
        life_pool: IntCB = IntCB(BASE_LIFE_POOL)
        lives: IntCB = IntCB(BASE_LIVES_COUNT)
        spawn_delay: FloatCB = FloatCB(SPAWN_DELAY)
        fall_speed: FloatCB = FloatCB(BASE_SPEED)
        word_length: IntCB = IntCB(2)
        text_length: IntCB = IntCB(1)
        game_over: BoolCB = BoolCB(False)
        combo_speed: FloatCB = FloatCB(BASE_COMBO_SPEED)
        combo_fill: FloatCB = FloatCB(0.0)
        combo_multiplier: FloatCB = FloatCB(BASE_COMBO_MULTIPLIER)

        life_pool.set_limit(MAX_LIFE_POOL)
        combo_multiplier.set_limit(MAX_COMBO_MULTIPLIER)
        lives.set_limit(BASE_LIFE_POOL)
        life_pool.add_callback(lambda val: lives.set_limit(val))
        return Stats(words_right, words_wrong, life_pool, lives, spawn_delay, fall_speed, word_length, text_length,
                     game_over, combo_speed, combo_fill, combo_multiplier)

    @staticmethod
    def reset(board_width: int) -> None:
        GameStats.get().words_right.set(0)
        GameStats.get().words_wrong.set(0)
        GameStats.get().life_pool.set(BASE_LIFE_POOL)
        GameStats.get().lives.set(BASE_LIVES_COUNT)
        GameStats.get().spawn_delay.set(SPAWN_DELAY)
        GameStats.get().fall_speed.set(BASE_SPEED)
        GameStats.get().word_length.set(2)
        GameStats.get().text_length.set(1)
        GameStats.get().game_over.set(False)
        GameStats.get().combo_speed.set(BASE_COMBO_SPEED)
        GameStats.get().combo_fill.set(float(board_width))
        GameStats.get().combo_multiplier.set(BASE_COMBO_MULTIPLIER)
