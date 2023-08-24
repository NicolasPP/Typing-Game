from dataclasses import dataclass
from pickle import dump
from pickle import load

from config.game_config import MAX_STORED_SCORES
from config.game_config import SCORE_FILE
from game.game_modifier import get_words_completed
from game.game_stats import GameStats


@dataclass
class Score:
    level: int
    words_left: int


class GameScores:
    scores: list[Score] = []

    @staticmethod
    def load_scores() -> None:
        with open(SCORE_FILE, "rb") as score_file:
            try:
                GameScores.set(load(score_file))
            except EOFError:
                GameScores.set([])
        GameScores.sort()

    @staticmethod
    def set(scores: list[Score]) -> None:
        GameScores.scores = scores
        GameStats.get().is_scores_empty.set(len(scores) == 0)

    @staticmethod
    def add_score(score: Score) -> None:
        scores: list[Score] = GameScores.get()
        scores.append(score)
        GameScores.set(scores)
        GameScores.sort()

        if len(GameScores.get()) > MAX_STORED_SCORES:
            GameScores.set(GameScores.get()[:MAX_STORED_SCORES])

        GameScores.write_scores()

    @staticmethod
    def get() -> list[Score]:
        return GameScores.scores

    @staticmethod
    def get_top_score() -> Score | None:
        if len(GameScores.get()) == 0: return None
        return GameScores.get()[-1]

    @staticmethod
    def write_scores() -> None:
        with open(SCORE_FILE, "wb") as score_file:
            dump(GameScores.get(), score_file)

    @staticmethod
    def sort() -> None:
        GameScores.get().sort(key=lambda score: get_words_completed(score.level, score.words_left))
