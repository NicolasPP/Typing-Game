from random import choice
from typing import Type
from typing import TypeAlias

from config.game_config import WORDS_FILE
from config.game_config import WORDS_FILE_MODE

DataTypes: TypeAlias = str | float | int


class WordDataManager:
    words_by_length: dict[int, list[str]] = {}
    words: list[str] = []

    @staticmethod
    def load_words() -> None:
        # https://www.wordfrequency.info/samples.asp
        # freq_data: list[dict[str, DataTypes]] = []  # ordered by freq
        common_words: list[str] = []
        with open(WORDS_FILE, WORDS_FILE_MODE) as file:
            fields: list[str] = file.readline().split()
            row: str = file.readline()
            while row:

                row_data: list[str] = row.split()
                assert len(row_data) == len(fields)
                # row_dict: dict[str, DataTypes] = {}

                for field, data in zip(fields, row_data):
                    # data_type: Type[DataTypes] = get_data_type(data)
                    # row_dict[field] = data_type(data)
                    if field == "lemma":
                        common_words.append(data)
                        break

                # freq_data.append(row_dict)
                row = file.readline()
        WordDataManager.words = common_words
        WordDataManager.process_words(common_words)

    @staticmethod
    def process_words(words: list[str]) -> None:
        for word in words:
            word_length: int = len(word)
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


def get_data_type(data: str) -> Type[DataTypes]:
    if data.isalnum():
        return int

    elif data.isalpha():
        return str

    return float
