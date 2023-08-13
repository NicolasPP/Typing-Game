from _thread import start_new_thread
from enum import Enum
from enum import auto
from typing import NamedTuple

from pygame.mixer import Sound

from config.game_config import ADD_CHAR_RIGHT_VOLUME_MULT
from config.game_config import ADD_CHAR_WRONG_VOLUME_MULT
from config.game_config import BACK_BUTTON_HOVER
from config.game_config import BUTTON_CLICK_VOLUME_MULT
from config.game_config import CHECK_ON
from config.game_config import COMPLETE_TEXT_VOLUME_MULT
from config.game_config import COUNT_2S
from config.game_config import DEFAULT_VOLUME
from config.game_config import DRUM_HIT_CLAP
from config.game_config import DRUM_HIT_FINISH
from config.game_config import DRUM_HIT_NORMAL
from config.game_config import GAIN_LIFE_VOLUME_MULT
from config.game_config import LOSE_LIFE_VOLUME_MULT


class AppSounds(Enum):
    ADD_CHAR_RIGHT = auto()
    ADD_CHAR_WRONG = auto()
    COMPLETE_WORD = auto()
    BUTTON_CLICK = auto()
    LOSE_LIFE = auto()
    GAIN_LIFE = auto()


class AppSound(NamedTuple):
    sound: Sound
    volume_mult: float


class SoundManager:
    sounds: dict[AppSounds, AppSound] = {}
    volume: float = DEFAULT_VOLUME

    @staticmethod
    def load_sounds() -> None:
        SoundManager.sounds[AppSounds.ADD_CHAR_RIGHT] = AppSound(Sound(DRUM_HIT_NORMAL), ADD_CHAR_RIGHT_VOLUME_MULT)
        SoundManager.sounds[AppSounds.ADD_CHAR_WRONG] = AppSound(Sound(DRUM_HIT_FINISH), ADD_CHAR_WRONG_VOLUME_MULT)
        SoundManager.sounds[AppSounds.COMPLETE_WORD] = AppSound(Sound(DRUM_HIT_CLAP), COMPLETE_TEXT_VOLUME_MULT)
        SoundManager.sounds[AppSounds.BUTTON_CLICK] = AppSound(Sound(BACK_BUTTON_HOVER), BUTTON_CLICK_VOLUME_MULT)
        SoundManager.sounds[AppSounds.LOSE_LIFE] = AppSound(Sound(COUNT_2S), LOSE_LIFE_VOLUME_MULT)
        SoundManager.sounds[AppSounds.GAIN_LIFE] = AppSound(Sound(CHECK_ON), GAIN_LIFE_VOLUME_MULT)

    @staticmethod
    def set_volume(volume: float) -> None:
        SoundManager.volume = volume

    @staticmethod
    def get(sound_name: AppSounds) -> AppSound:
        app_sound: AppSound | None = SoundManager.sounds.get(sound_name)
        assert app_sound is not None, f"sound name: {sound_name.name} has not been loaded"
        return app_sound

    @staticmethod
    def play(sound_name: AppSounds) -> None:
        app_sound: AppSound = SoundManager.get(sound_name)
        app_sound.sound.set_volume(SoundManager.volume * app_sound.volume_mult)
        start_new_thread(app_sound.sound.play, ())
