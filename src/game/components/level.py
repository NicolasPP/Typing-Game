from config.game_config import STARTING_SPEED
from gui.gui_vars import GuiVars

class LevelManager:
    def __init__(self) -> None:
        self.completed_words: int = 0
        self.speed: float = STARTING_SPEED

    def set_completed_words(self, completed_words: int) -> None:
        if completed_words < 0: return
        if completed_words < self.completed_words: return
        self.completed_words = completed_words
        GuiVars.score.set(completed_words)

    def get_speed(self) -> float:
        return self.speed + (self.completed_words * 2)

    def get_word_lengths(self) -> list[int]:
        start: int = (self.completed_words // 10) + 2
        return list(range(start, start + 3))

