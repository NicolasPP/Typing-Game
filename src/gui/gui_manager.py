from pygame import Rect

from gui.lives_gui import LivesGui
from gui.score_gui import ScoreGui


class GuiManager:
    def __init__(self, board_rect: Rect) -> None:
        self.lives: LivesGui = LivesGui(board_rect)
        self.score: ScoreGui = ScoreGui(board_rect)

    def render(self) -> None:
        self.lives.render()
        self.score.render()