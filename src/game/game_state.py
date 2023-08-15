from pygame.event import Event
from pygame.key import name

from game.components.board import Board
from game.components.letter import Letter
from game.components.level import LevelManager
from game.components.text import Text
from game.game_stats import GameStats
from game.game_stats import Stats
from utils.accumulator import Accumulator
from utils.sound_manager import AppSounds
from utils.sound_manager import SoundManager
from utils.themes import ThemeManager


class GameState:

    def __init__(self, board_width: int, board_height: int) -> None:
        self.board: Board = Board(board_width, board_height)
        self.spawn_accumulator: Accumulator = Accumulator(GameStats.get().spawn_delay.get())
        self.level_manager: LevelManager = LevelManager(self.board.rect)

        self.texts: list[Text] = []
        self.stop_spawning: bool = False
        self.game_over: bool = False
        self.current_text: Text | None = None

        GameStats.get().lives.add_callback(self.end_game)
        ThemeManager.add_call_back(Letter.load_state_colors)
        ThemeManager.add_call_back(self.update_state_theme, 1)

    def update_state_theme(self) -> None:
        current_text: Text | None = self.get_current_text()
        if current_text is None: return
        current_text.get_current_word().underline()

    def render(self) -> None:
        self.board.clear()
        for text in self.texts:
            text.render(self.board.surface)
        self.level_manager.render(self.board.surface)
        self.board.render()

    def parse_event(self, event: Event) -> None:
        self.level_manager.parse_event(event)

    def update(self, delta_time: float) -> None:
        stats: Stats = GameStats.get()
        if stats.game_over.get(): return
        is_rolling: bool = self.level_manager.is_rolling
        self.level_manager.update(delta_time)

        if is_rolling and len(self.texts) > 0:
            self.texts.clear()

        if self.spawn_accumulator.wait(delta_time) and not is_rolling:
            self.spawn_text()

        # update words
        for text in self.texts:
            text.fall(delta_time)

        current_text: Text | None = self.get_current_text()
        if current_text is None: return
        if current_text.is_done():
            self.remove_fist_text()

        if self.is_text_collided():
            stats.lives.increment(len(current_text.words) * -1)
            stats.combo_fill.set(0.0)
            SoundManager.play(AppSounds.LOSE_LIFE)

    def reset(self) -> None:
        self.texts.clear()
        self.level_manager.reset()
        GameStats.reset(self.board.rect.width)

    def add_text(self, text: Text) -> None:
        text.set_random_pos(self.board.rect.width)
        if len(self.texts) == 0: text.underline_current_word()
        self.texts.append(text)

    def spawn_text(self) -> None:
        if self.stop_spawning: return
        text: Text = self.level_manager.get_text()
        self.add_text(text)

    def remove_fist_text(self) -> None:
        self.texts = self.texts[1:]
        text: Text | None = self.get_current_text()
        if text is None: return
        text.underline_current_word()

    def is_text_collided(self) -> bool:
        current_text: Text | None = self.get_current_text()
        if current_text is None: return False
        is_collided: bool = current_text.get_current_word().rect.bottom > self.board.rect.height
        if is_collided: self.remove_fist_text()
        return is_collided

    def get_current_text(self) -> Text | None:
        if len(self.texts) == 0: return None
        return self.texts[0]

    def process_key_code(self, key_code: int) -> None:
        current_text: Text | None = self.get_current_text()
        stats: Stats = GameStats.get()
        if stats.game_over.get(): return
        if current_text is None: return
        key_name: str = name(key_code)
        if len(key_name) != 1: return
        if current_text.is_done(): return
        if current_text.add_pressed_key(key_name):
            stats.combo_fill.increment(stats.combo_multiplier.get())
            SoundManager.play(AppSounds.ADD_CHAR_RIGHT)
        else:
            stats.combo_fill.increment(stats.combo_multiplier.get() * -1)
            SoundManager.play(AppSounds.ADD_CHAR_WRONG)

        if current_text.get_current_word().is_correct():
            word_length: int = len(current_text.get_current_word().letters)
            stats.combo_fill.increment(float(word_length) * stats.combo_multiplier.get())
            current_text.remove_word()
            current_text.update_counter_surface()
            stats.words_required.increment(-1)
            SoundManager.play(AppSounds.COMPLETE_WORD)

    def end_game(self, lives_count: int) -> None:
        if lives_count <= 0:
            GameStats.get().game_over.set(True)
            self.texts.clear()
            self.level_manager.words_req.render = False
