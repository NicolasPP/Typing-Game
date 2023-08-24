from time import time

from pygame import QUIT
from pygame import display
from pygame import event
from pygame import font
from pygame import mixer

from game.components.letter import Letter
from game.game_modifier import GameModifier
from game.game_score import GameScores
from gui.pages.game_page import GamePage
from gui.pages.menu_page import MenuPage
from gui.pages.page import Page
from gui.pages.page_manager import PageManager
from utils.sound_manager import SoundManager
from utils.themes import ThemeManager
from utils.window import Window
from utils.word_data_manager import WordDataManager


class GameApp:

    def __init__(self) -> None:
        font.init()
        mixer.init()
        ThemeManager.load_themes()
        Letter.load_state_colors()
        WordDataManager.load_words()
        SoundManager.load_sounds()
        GameModifier.load_modifiers()
        GameScores.load_scores()

        self.page_manager: PageManager = PageManager()
        self.done: bool = False
        self.prev_time: float = time()
        self.delta_time: float = 0.0

        self.page_manager.add_page(MenuPage)
        self.page_manager.add_page(GamePage)
        self.page_manager.set_page("MenuPage")

    def set_delta_time(self) -> None:
        now: float = time()
        self.delta_time = now - self.prev_time
        self.prev_time = now

    def run(self) -> None:

        while not self.done:

            page: Page = self.page_manager.get_page()
            self.set_delta_time()

            for game_event in event.get():
                if game_event.type == QUIT:
                    self.done = True
                else:
                    page.parse_event(game_event)

            Window.get().clear()
            page.update(self.delta_time)
            page.render()
            display.flip()
