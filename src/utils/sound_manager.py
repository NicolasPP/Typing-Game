from _thread import start_new_thread
from enum import Enum
from enum import auto

from pygame.mixer import Sound

from config.game_config import DRUM_HIT_CLAP
from config.game_config import BACK_BUTTON_CLICK
from config.game_config import BACK_BUTTON_HOVER
from config.game_config import DRUM_HIT_FINISH
from config.game_config import COUNT_2S
from config.game_config import DRUM_HIT_NORMAL
from config.game_config import CHECK_ON


class AppSounds(Enum):
    ADD_CHAR_RIGHT = auto()
    ADD_CHAR_WRONG = auto()
    COMPLETE_TEXT = auto()
    BUTTON_CLICK = auto()
    LOSE_LIFE = auto()
    GAIN_LIFE = auto()
    BACKSPACE = auto()

class SoundManager:
    sounds: dict[AppSounds, Sound] = {}

    @staticmethod
    def load_sounds() -> None:
        SoundManager.sounds[AppSounds.ADD_CHAR_RIGHT] = Sound(DRUM_HIT_NORMAL)
        SoundManager.sounds[AppSounds.ADD_CHAR_WRONG] = Sound(DRUM_HIT_FINISH)
        SoundManager.sounds[AppSounds.COMPLETE_TEXT] = Sound(DRUM_HIT_CLAP)
        SoundManager.sounds[AppSounds.BUTTON_CLICK] = Sound(BACK_BUTTON_HOVER)
        SoundManager.sounds[AppSounds.LOSE_LIFE] = Sound(COUNT_2S)
        SoundManager.sounds[AppSounds.GAIN_LIFE] = Sound(CHECK_ON)
        SoundManager.sounds[AppSounds.BACKSPACE] = Sound(BACK_BUTTON_CLICK)

    @staticmethod
    def get(sound_name: AppSounds) -> Sound:
        sound: Sound = SoundManager.sounds.get(sound_name)
        assert sound is not None, f"sound name: {sound_name.name} has not been loaded"
        return sound

    @staticmethod
    def play(sound_name: AppSounds) -> None:
        sound: Sound = SoundManager.get(sound_name)
        start_new_thread(sound.play, ())
