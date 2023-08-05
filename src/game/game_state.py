from game.components.board import Board
from game.components.level import LevelManager
from game.components.word import Word
from game.components.word import WordManager


class GameState:

    def __init__(self, board_width: int, board_height: int) -> None:
        self.board: Board = Board(board_width, board_height)
        self.level_manager: LevelManager = LevelManager()
        self.word_manager: WordManager = WordManager()

    def render(self) -> None:
        self.board.clear()
        self.word_manager.render(self.board.surface)
        self.board.render()

    def update(self, delta_time: float) -> None:
        if self.word_manager.spawn_accumulator.wait(delta_time):
            self.word_manager.spawn_word(self.level_manager.get_word_lengths())

        self.word_manager.update(delta_time, self.level_manager.get_speed())

        collided_words: list[Word] = self.word_manager.get_collided_words(self.board.rect)
