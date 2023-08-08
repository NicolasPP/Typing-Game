from random import randint

from config.game_config import STARTING_SPEED
from gui.gui_vars import GuiVars


class LevelManager:

    @staticmethod
    def roll_text_length() -> int:
        # TODO change the percentage based on the users score
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

    def __init__(self) -> None:
        self.completed_words: int = 0
        self.speed: float = STARTING_SPEED

    def set_completed_words(self, completed_words: int) -> None:
        if completed_words < 0: return
        if completed_words < self.completed_words: return
        self.completed_words = completed_words
        GuiVars.score.set(completed_words)

    def get_speed(self) -> float:
        return self.speed + ((self.completed_words // 10) * 5)

    def get_word_lengths(self) -> list[int]:
        start: int = (self.completed_words // 10) + 2
        return list(range(start, start + 3))
