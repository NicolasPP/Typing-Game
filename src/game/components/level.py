from random import randint

from game.game_stats import GameStats


class LevelManager:

    @staticmethod
    def roll_text_length() -> int:
        """
        length
            = 1 - 65 %
            = 2 - 20 %
            = 3 - 10 %
            = 4 - 5 %
        """
        roll: int = randint(0, 100)
        if roll <= 65:
            return 1

        elif 65 < roll <= 85:
            return 2

        elif 85 < roll <= 95:
            return 3

        else:
            return 4

    @staticmethod
    def roll_word_lengths() -> list[int]:
        start: int = (GameStats.get().words_right.get() // 10) + 2
        return list(range(start, start + 3))
