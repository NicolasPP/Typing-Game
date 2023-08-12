# -- Gui --
GAME_SCREEN_WIDTH: int = 540
GAME_SCREEN_HEIGHT: int = 800
BOARD_WIDTH: int = 480
BOARD_HEIGHT: int = 650
LIFE_SURF_SIZE: int = 40
OUTLINE_THICKNESS: int = 5
LIFE_COMBO_HEIGHT: int = 3
GUI_GAP: int = 5
GAME_OVER_ALPHA: int = 70
HOVER_ALPHA: int = 70

# -- Sounds --
BACK_BUTTON_CLICK: str = "assets/sounds/back-button-click.wav"
BACK_BUTTON_HOVER: str = "assets/sounds/back-button-hover.wav"
CHECK_OFF: str = "assets/sounds/check-off.wav"
CHECK_ON: str = "assets/sounds/check-on.wav"
COMBO_BREAK: str = "assets/sounds/combobreak.wav"
COUNT_1S: str = "assets/sounds/count1s.wav"
COUNT_2S: str = "assets/sounds/count2s.wav"
DRUM_HIT_CLAP: str = "assets/sounds/drum-hitclap.wav"
DRUM_HIT_FINISH: str = "assets/sounds/drum-hitfinish.wav"
DRUM_HIT_NORMAL: str = "assets/sounds/drum-hitnormal.wav"

# -- Font --
DEFAULT_FONT_SIZE: int = 37
LETTER_FONT_SIZE: int = 33

# -- Base Values --
SPAWN_DELAY: float = 3.0  # Seconds
BASE_SPEED: float = 30.0
BASE_COMBO_SPEED: float = 20.0
BASE_COMBO_MULTIPLIER: float = 7.0
MAX_COMBO_MULTIPLIER: float = 15.0
BASE_LIVES_COUNT: int = 3
BASE_LIFE_POOL: int = 3
MAX_LIFE_POOL: int = 12
DEFAULT_VOLUME: float = 0.3
TRY_AGAIN_VALUE: str = "Try Again!"
PLAY_LABEL_VALUE: str = "Play"
SCORE_LABEL_VALUE: str = "Scores"
BACK_LABEL_VALUE: str = "Back"

# -- files --
WORDS_FILE: str = "data/words/words_frequency.txt"
WORDS_FILE_MODE: str = "r"
