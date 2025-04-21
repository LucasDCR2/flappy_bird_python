"""
Constantes para os assets do jogo Flappy Bird
Compatível com qualquer sistema operacional usando pathlib
"""

from pathlib import Path

# Caminho base relativo ao local deste arquivo
BASE_PATH = Path(__file__).resolve().parent / "assets"
IMAGES_PATH = BASE_PATH / "images"
AUDIO_PATH = BASE_PATH / "audio"

# Imagens
BACKGROUND = IMAGES_PATH / "background.png"
GROUND = IMAGES_PATH / "ground.png"
CLOUDS = IMAGES_PATH / "clouds.png"
PIPE = IMAGES_PATH / "pipe.png"
PIPE_ROTATED = IMAGES_PATH / "pipe_rotated.png"

BIRD_MID_FLAP = IMAGES_PATH / "bird_midflap.png"
BIRD_UP_FLAP = IMAGES_PATH / "bird_upflap.png"
BIRD_DOWN_FLAP = IMAGES_PATH / "bird_downflap.png"

GAME_OVER = IMAGES_PATH / "gameover.png"
MENU = IMAGES_PATH / "menu.jpg"
MESSAGE = IMAGES_PATH / "message.png"

# Áudio
FLYING = AUDIO_PATH / "fly.wav"
COLLISION = AUDIO_PATH / "collision.wav"
POINT = AUDIO_PATH / "point.wav"
