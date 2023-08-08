from utils.callback_vars import IntCB
from config.game_config import BASE_LIVES_COUNT

class GuiVars:

    score: IntCB = IntCB(0)
    lives: IntCB = IntCB(BASE_LIVES_COUNT)