from __future__ import annotations

from dataclasses import dataclass

from config.game_config import BASE_LIFE_POOL
from config.game_config import MAX_LIFE_POOL
from config.game_config import SPAWN_DELAY
from config.game_config import STARTING_SPEED
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
        lives: IntCB = IntCB(BASE_LIFE_POOL)
        spawn_delay: FloatCB = FloatCB(SPAWN_DELAY)
        fall_speed: FloatCB = FloatCB(STARTING_SPEED)
        word_length: IntCB = IntCB(2)
        text_length: IntCB = IntCB(1)
        game_over: BoolCB = BoolCB(False)

        life_pool.set_limit(MAX_LIFE_POOL)
        lives.set_limit(BASE_LIFE_POOL)
        life_pool.add_callback(lambda val: lives.set_limit(val))
        return Stats(words_right, words_wrong, life_pool, lives, spawn_delay, fall_speed, word_length, text_length,
                     game_over)

    @staticmethod
    def reset() -> None:
        GameStats.get().words_right.set(0)
        GameStats.get().words_wrong.set(0)
        GameStats.get().life_pool.set(BASE_LIFE_POOL)
        GameStats.get().lives.set(BASE_LIFE_POOL)
        GameStats.get().spawn_delay.set(SPAWN_DELAY)
        GameStats.get().fall_speed.set(STARTING_SPEED)
        GameStats.get().word_length.set(2)
        GameStats.get().text_length.set(1)
        GameStats.get().game_over.set(False)
