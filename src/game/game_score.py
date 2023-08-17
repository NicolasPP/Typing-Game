from dataclasses import dataclass
from pickle import dump
from pickle import load

from config.game_config import MAX_STORED_SCORES
from config.game_config import SCORE_FILE
from game.game_modifier import get_words_completed


@dataclass
class Score:
    level: int
    words_left: int


class GameScores:
    scores: list[Score] = []

    @staticmethod
    def load_scores() -> None:
        with open(SCORE_FILE, "rb") as score_file:
            if not score_file.read():
                GameScores.scores = []
            else:
                GameScores.scores = load(score_file)
        GameScores.sort()

    @staticmethod
    def add_score(score: Score) -> None:
        GameScores.get().append(score)
        GameScores.sort()

        if len(GameScores.get()) > MAX_STORED_SCORES:
            GameScores.scores = GameScores.get()[:MAX_STORED_SCORES]

        GameScores.write_scores()

    @staticmethod
    def get() -> list[Score]:
        return GameScores.scores

    @staticmethod
    def write_scores() -> None:
        with open(SCORE_FILE, "wb") as score_file:
            dump(GameScores.get(), score_file)

    @staticmethod
    def sort() -> None:
        GameScores.get().sort(key=lambda score: get_words_completed(score.level, score.words_left))
