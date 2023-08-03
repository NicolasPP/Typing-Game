from game.components.board import Board


class GameState:

    def __init__(self, board_width: int, board_height: int) -> None:
        self.board: Board = Board(board_width, board_height)

    def render(self) -> None:
        self.board.render()

    def update(self) -> None:
        pass
