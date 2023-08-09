from pygame import Rect

from gui.lives_gui import LivesGui
from gui.score_gui import ScoreGui
from gui.game_over_gui import GameOverGui


class GuiManager:
    def __init__(self, board_rect: Rect) -> None:
        self.lives: LivesGui = LivesGui(board_rect)
        self.score: ScoreGui = ScoreGui(board_rect)
        self.game_over: GameOverGui = GameOverGui(board_rect)

    def render(self) -> None:
        self.lives.render()
        self.score.render()
        self.game_over.render()

    def update(self) -> None:
        self.game_over.update()