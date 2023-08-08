from pygame import KEYDOWN
from pygame.event import Event

from game.components.board import Board
from game.components.level import LevelManager
from game.components.word import Word
from game.components.word import WordManager
from gui.gui_manager import GuiManager
from gui.gui_vars import GuiVars


class GameState:

    def __init__(self, board_width: int, board_height: int) -> None:
        self.board: Board = Board(board_width, board_height)
        self.level_manager: LevelManager = LevelManager()
        self.word_manager: WordManager = WordManager()
        self.gui_manager: GuiManager = GuiManager(self.board.rect)
        self.game_over: bool = False
        GuiVars.lives.add_callback(self.end_game)

    def render(self) -> None:
        self.board.clear()
        self.word_manager.render(self.board.surface)
        self.board.render()
        self.gui_manager.render()

    def update(self, delta_time: float) -> None:
        if self.game_over: return
        if self.word_manager.spawn_accumulator.wait(delta_time):
            self.word_manager.spawn_word(self.level_manager.get_word_lengths(), self.board.rect.width)

        # update words
        for word in self.word_manager.words:
            word.fall(delta_time, self.level_manager.get_speed())

        current_word: Word | None = self.word_manager.get_current_word()
        if current_word is None: return
        if current_word.is_correct():
            self.level_manager.set_completed_words(self.level_manager.completed_words + 1)
            self.word_manager.remove_first_word()

        if self.word_manager.is_collided(self.board.rect.height):
            GuiVars.lives.set(GuiVars.lives.get() - 1)

    def parse_player_input(self, game_event: Event):
        if game_event.type == KEYDOWN:
            self.word_manager.process_key_name(game_event.key)

    def end_game(self, lives_count: int) -> None:
        if lives_count == 0:
            self.game_over = True
