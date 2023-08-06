from pygame import KEYDOWN
from pygame.event import Event
from pygame.key import name

from game.components.board import Board
from game.components.level import LevelManager
from game.components.word import WordManager


class GameState:

    def __init__(self, board_width: int, board_height: int) -> None:
        self.lives: int = 5
        self.board: Board = Board(board_width, board_height)
        self.level_manager: LevelManager = LevelManager()
        self.word_manager: WordManager = WordManager()

    def render(self) -> None:
        self.board.clear()
        self.word_manager.render(self.board.surface)
        self.board.render()

    def update(self, delta_time: float) -> None:
        if self.word_manager.spawn_accumulator.wait(delta_time):
            self.word_manager.spawn_word(self.level_manager.get_word_lengths(), self.board.rect.width)

        self.word_manager.update(delta_time, self.level_manager.get_speed(),
                                 self.level_manager.increment_completed_words)

        if self.word_manager.is_collided(self.board.rect.height):
            self.lives -= 1

    def parse_player_input(self, game_event: Event):
        if game_event.type == KEYDOWN:
            self.word_manager.process_key_name(game_event.key)
