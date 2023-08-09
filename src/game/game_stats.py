from __future__ import annotations

from dataclasses import dataclass

from config.game_config import BASE_LIVES_COUNT
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
        return Stats(IntCB(0), IntCB(0), IntCB(BASE_LIVES_COUNT), IntCB(BASE_LIVES_COUNT), FloatCB(SPAWN_DELAY),
                     FloatCB(STARTING_SPEED), IntCB(2), IntCB(1), BoolCB(False))

    @staticmethod
    def reset() -> None:
        GameStats.get().words_right.set(0)
        GameStats.get().words_wrong.set(0)
        GameStats.get().life_pool.set(BASE_LIVES_COUNT)
        GameStats.get().lives.set(BASE_LIVES_COUNT)
        GameStats.get().spawn_delay.set(SPAWN_DELAY)
        GameStats.get().fall_speed.set(STARTING_SPEED)
        GameStats.get().word_length.set(2)
        GameStats.get().text_length.set(1)
        GameStats.get().game_over.set(False)
