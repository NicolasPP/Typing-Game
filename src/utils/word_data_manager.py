from random import choice

from config.game_config import WORDS_FILE
from config.game_config import WORDS_FILE_MODE


class WordDataManager:
    words_by_length: dict[int, set[str]] = {}

    @staticmethod
    def load_words() -> None:
        with open(WORDS_FILE, WORDS_FILE_MODE) as word_file:

            for word in word_file.read().split():
                word_length: int = len(word)
                if word_length in WordDataManager.words_by_length:
                    WordDataManager.words_by_length[word_length].add(word)
                else:
                    WordDataManager.words_by_length[word_length] = {word}

    @staticmethod
    def get_random_word(word_length: int | None = None, played_words: set[str] | None = None) -> str:
        if word_length is None or word_length not in WordDataManager.words_by_length:
            possible_words = WordDataManager.get_all_words()

        else:
            possible_words = WordDataManager.words_by_length[word_length]

        if played_words is not None:
            possible_words -= played_words

        if len(possible_words) == 0:
            # FIXME this is no good, icky. maybe get another word
            raise Exception(f"no words with length {word_length} available")

        return choice(list(possible_words))

    @staticmethod
    def get_all_words() -> set[str]:
        all_words: set[str] = set()
        for words in WordDataManager.words_by_length.values():
            all_words = all_words.union(words)
        return all_words
