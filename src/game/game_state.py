from game.components.board import Board
from game.components.word import WordManager


class GameState:

    def __init__(self, board_width: int, board_height: int) -> None:
        self.board: Board = Board(board_width, board_height)
        self.word_manager: WordManager = WordManager()

    def render(self) -> None:
        self.board.render()

    def update(self, delta_time: float) -> None:
        self.word_manager.spawn_word(delta_time)
