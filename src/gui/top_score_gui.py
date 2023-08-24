from pygame import Rect
from pygame import Surface
from pygame.font import Font

from config.game_config import DEFAULT_FONT_SIZE
from config.game_config import GUI_GAP
from game.game_modifier import get_words_completed
from game.game_score import GameScores
from game.game_score import Score
from utils.fonts import FontManager
from utils.themes import Theme
from utils.themes import ThemeManager


class TopScoreGui:
    def __init__(self) -> None:
        self.surface: Surface | None = None
        self.rect: Rect | None = None
        self.update_surface()

    def update_surface(self) -> None:
        top_score: Score | None = GameScores.get_top_score()
        if top_score is None: return
        font: Font = FontManager.get_font(DEFAULT_FONT_SIZE)
        theme: Theme = ThemeManager.get_theme()
        level_surface: Surface = font.render(str(top_score.level), True, theme.foreground_primary,
                                             theme.background_primary)
        total_words: str = f"words: {get_words_completed(top_score.level, top_score.words_left)}"
        font = FontManager.get_font(DEFAULT_FONT_SIZE)
        total_words_surface: Surface = font.render(total_words, True, theme.foreground_primary,
                                                   theme.background_primary)
        width: int = max([total_words_surface.get_width(), level_surface.get_width()])
        height: int = total_words_surface.get_height() + level_surface.get_height() + GUI_GAP
        surface: Surface = Surface((width, height))
        surface.fill(theme.background_primary)
        surface.blit(level_surface, level_surface.get_rect(midtop=surface.get_rect().midtop))
        surface.blit(total_words_surface, (0, level_surface.get_height() + GUI_GAP))

        self.surface = surface
        rect: Rect = surface.get_rect()

        if self.rect is not None:
            rect.topleft = self.rect.topleft

        self.rect = rect

    def render(self, parent_surface: Surface) -> None:
        if self.surface is None: return
        if self.rect is None: return
        parent_surface.blit(self.surface, self.rect)
