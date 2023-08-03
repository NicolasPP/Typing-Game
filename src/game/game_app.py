from pygame import QUIT
from pygame import display
from pygame import event
from pygame import font

from game.game_screen import GameScreen
from utils.themes import ThemeManager
from game.game_state import GameState
from game.components.letter import Letter


class GameApp:

    def __init__(self) -> None:
        ThemeManager.load_themes()
        Letter.load_state_colors()
        font.init()

        self.state: GameState = GameState(600, 600)
        self.done: bool = False

    def run(self) -> None:

        while not self.done:

            for game_event in event.get():
                if game_event.type == QUIT:
                    self.done = True

            GameScreen.get().clear()
            self.state.update()
            self.state.render()
            display.flip()
