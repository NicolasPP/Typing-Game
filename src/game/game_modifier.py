from random import choice

from game.game_stats import GameStats
from utils.word_data_manager import WordDataManager


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
    print(choices)
    return choice(choices)
