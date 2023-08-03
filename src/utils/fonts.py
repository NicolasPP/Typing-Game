from pygame.font import Font
from pygame.font import SysFont
from pygame.font import get_fonts


class FontManager:
    possible_fonts: list[str] = get_fonts()
    font_index: int = 0

    @staticmethod
    def get_font(font_size: int) -> Font:
        return SysFont(FontManager.get_font_name(), font_size)

    @staticmethod
    def get_font_name() -> str:
        return FontManager.possible_fonts[FontManager.font_index % len(FontManager.possible_fonts)]
