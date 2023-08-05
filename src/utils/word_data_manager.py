from random import choice

from config.game_config import WORDS_FILE
from config.game_config import WORDS_FILE_MODE


class WordDataManager:
    words_by_length: dict[int, list[str]] = {}
    words: list[str] = []

    @staticmethod
    def load_words() -> None:
        with open(WORDS_FILE, WORDS_FILE_MODE) as word_file:

            for word in word_file.read().split():
                word_length: int = len(word)
                WordDataManager.words.append(word)
                if word_length in WordDataManager.words_by_length:
                    WordDataManager.words_by_length[word_length].append(word)
                else:
                    WordDataManager.words_by_length[word_length] = [word]

    @staticmethod
    def get_random_word(word_lengths: list[int] | None = None, played_words: list[str] | None = None) -> str:
        possible_words: list[str] = []
        if word_lengths is None:
            possible_words = WordDataManager.words

        else:
            for length in word_lengths:
                if length not in WordDataManager.words_by_length: continue
                possible_words.extend(WordDataManager.words_by_length[length])

            if len(possible_words) == 0:
                possible_words = WordDataManager.words

        if possible_words == played_words:
            # assuming a player wont use all the words in the dictionary in one game
            possible_words = WordDataManager.words

        word: str = choice(possible_words)

        if played_words is None:
            return word

        while word in played_words:
            word = choice(possible_words)

        return word
