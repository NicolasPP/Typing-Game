from pygame import Rect

from game.game_stats import GameStats
from gui.game_over_gui import GameOverGui
from gui.lives_gui import LivesGui
from gui.score_gui import ScoreGui


class GuiManager:
    def __init__(self, board_rect: Rect) -> None:
        self.lives: LivesGui = LivesGui(board_rect)
        self.score: ScoreGui = ScoreGui(board_rect)
        self.game_over: GameOverGui = GameOverGui(board_rect)

    def render(self) -> None:
        self.lives.render()
        self.score.render()
        if GameStats.get().game_over.get():
            self.game_over.render()
