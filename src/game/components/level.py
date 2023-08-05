from config.game_config import STARTING_SPEED

class LevelManager:
    def __init__(self) -> None:
        self.completed_words: int = 0
        self.speed: float = STARTING_SPEED

    def get_speed(self) -> float:
        return self.speed + (self.completed_words * 2)

    def get_word_lengths(self) -> list[int]:
        start: int = (self.completed_words // 10) + 2
        return list(range(start, start + 3))

