from abc import ABC
from abc import abstractmethod
from enum import Enum
from enum import auto
from random import choice
from random import uniform
from typing import TypeAlias

from config.game_config import MAX_STAT_MULT
from config.game_config import MIN_STAT_MULT
from config.game_config import STAT_MOD_AMOUNT
from config.game_config import STAT_MULT_SEG_SIZE
from game.game_stats import GameStats
from game.game_stats import Stats
from utils.callback_vars import BoolCB
from utils.callback_vars import FloatCB
from utils.callback_vars import IntCB

PossibleStats: TypeAlias = IntCB | BoolCB | FloatCB


class StatModifierType(Enum):
    INCREASE = auto()
    DECREASE = auto()


class StatModifier(ABC):
    def __init__(self, stat: PossibleStats, name: str, description: str, stat_type: StatModifierType) -> None:
        self.name: str = name
        self.description: str = description
        self.stat: PossibleStats = stat
        self.type: StatModifierType = stat_type

    @abstractmethod
    def apply(self) -> None:
        pass


class MultiplierModifier(StatModifier):
    def __init__(self, stat: PossibleStats, name: str, description: str, stat_type: StatModifierType) -> None:
        super().__init__(stat, name, description, stat_type)
        self.min_mult: float = MIN_STAT_MULT
        self.max_mult: float = MAX_STAT_MULT
        self.seg_size: float = STAT_MULT_SEG_SIZE
        self.start_point: float = MIN_STAT_MULT

    def set_starting_point(self, starting_point: float) -> None:
        if starting_point + self.seg_size > self.max_mult:
            self.start_point = self.max_mult - self.seg_size

        elif starting_point < 0:
            self.start_point = 0

        else:
            self.start_point = starting_point

    def roll_multiplier(self) -> float:
        return uniform(self.start_point, self.start_point + self.seg_size)

    def apply(self) -> None:
        multiplier: float = self.roll_multiplier()
        if self.type is StatModifierType.INCREASE:
            self.stat.set(self.stat.get() * multiplier)

        if self.type is StatModifierType.DECREASE:
            self.stat.set(self.stat.get() / multiplier)


class FixedModifier(StatModifier):

    def __init__(self, stat: PossibleStats, name: str, description: str, stat_type: StatModifierType,
                 amount: int | float) -> None:
        super().__init__(stat, name, description, stat_type)
        self.amount: int | float = amount

    def apply(self) -> None:
        assert not isinstance(self.stat, BoolCB), "stat can not be a boolean"
        if self.type is StatModifierType.INCREASE:
            self.stat.increment(self.amount)

        if self.type is StatModifierType.DECREASE:
            self.stat.increment(self.amount * -1)


class GameModifier:
    buffs: list[StatModifier] = []
    debuffs: list[StatModifier] = []

    @staticmethod
    def load_modifiers() -> None:
        GameModifier.load_debuffs()
        GameModifier.load_buffs()

    @staticmethod
    def load_debuffs() -> None:
        stats: Stats = GameStats.get()
        increase_word_length: FixedModifier = FixedModifier(stats.word_length, "WordLength+",
                                                            "increase word length range by 1",
                                                            StatModifierType.INCREASE, 1)
        increase_text_length: FixedModifier = FixedModifier(stats.text_length, "TextLength+",
                                                            "increase the possible text length by 1",
                                                            StatModifierType.INCREASE, 1)
        increase_fall_speed: MultiplierModifier = MultiplierModifier(stats.fall_speed, "FallSpeed+",
                                                                     "increase fall speed", StatModifierType.INCREASE)
        decrease_spawn_delay: MultiplierModifier = MultiplierModifier(stats.spawn_delay, "SpawnDelay-",
                                                                      "decrease the spawn delay",
                                                                      StatModifierType.DECREASE)
        GameModifier.debuffs.extend(
            [increase_text_length, increase_word_length, increase_fall_speed, decrease_spawn_delay])

    @staticmethod
    def load_buffs() -> None:
        stats: Stats = GameStats.get()
        increase_life_pool: FixedModifier = FixedModifier(stats.life_pool, "LifePool+", "Increase life pool by 1",
                                                          StatModifierType.INCREASE, 1)
        decrease_fall_speed: MultiplierModifier = MultiplierModifier(stats.fall_speed, "FallSpeed-",
                                                                     "increase fall speed", StatModifierType.DECREASE)
        increase_spawn_delay: MultiplierModifier = MultiplierModifier(stats.spawn_delay, "SpawnDelay-",
                                                                      "decrease the spawn delay",
                                                                      StatModifierType.INCREASE)
        GameModifier.buffs.extend([increase_life_pool, decrease_fall_speed, increase_spawn_delay])

    @staticmethod
    def roll_buffs() -> list[StatModifier]:
        buffs: list[StatModifier] = []
        while len(buffs) < STAT_MOD_AMOUNT:
            debuff: StatModifier = choice(GameModifier.buffs)
            if debuff not in buffs:
                buffs.append(debuff)
        return buffs

    @staticmethod
    def roll_debuffs() -> list[StatModifier]:
        debuffs: list[StatModifier] = []
        while len(debuffs) < STAT_MOD_AMOUNT:
            debuff: StatModifier = choice(GameModifier.debuffs)
            if debuff not in debuffs:
                debuffs.append(debuff)
        return debuffs
