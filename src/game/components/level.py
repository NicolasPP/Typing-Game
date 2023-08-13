from config.game_config import BASE_WORDS_PER_LEVEL
from game.components.text import Text
from game.game_modifier import roll_text_length
from game.game_modifier import roll_word_lengths
from game.game_stats import GameStats
from utils.word_data_manager import WordDataManager


class LevelManager:
    def __init__(self) -> None:
        self.words_per_level: int = BASE_WORDS_PER_LEVEL
        self.played_words: list[str] = []
        GameStats.get().words_required.add_callback(self.update_level_num)
        GameStats.get().level_num.add_callback(lambda val: GameStats.get().word_length.increment(1))
        GameStats.get().level_num.add_callback(lambda val: GameStats.get().text_length.increment(1))

    def update_level_num(self, words_required: int) -> None:
        if words_required <= 0:
            GameStats.get().level_num.increment(1)
            GameStats.get().words_required.set(self.words_per_level)

    def get_text(self) -> Text:
        text_length: int = roll_text_length()
        word_lengths: list[int] = roll_word_lengths()
        word_values: list[str] = []
        while len(word_values) < text_length:
            word_val: str = WordDataManager.get_random_word(played_words=self.played_words, word_lengths=word_lengths)
            word_values.append(word_val)
            self.played_words.append(word_val)

        return Text(word_values)
