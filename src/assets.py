"""
Constantes para os assets do jogo Flappy Bird
Compatível com qualquer sistema operacional usando pathlib
"""

from pathlib import Path

# Caminho base relativo ao local deste arquivo
BASE_PATH = Path(__file__).resolve().parent / "assets"
IMAGES_PATH = BASE_PATH / "images"
AUDIO_PATH = BASE_PATH / "audio"
SCORE_PATH = BASE_PATH / "score"

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
HEART = IMAGES_PATH / "heart.png"  # Imagem do coração para representar vidas

# Números para exibição de pontuação (0-9)
NUMBER_0 = SCORE_PATH / "0.png"
NUMBER_1 = SCORE_PATH / "1.png"
NUMBER_2 = SCORE_PATH / "2.png"
NUMBER_3 = SCORE_PATH / "3.png"
NUMBER_4 = SCORE_PATH / "4.png"
NUMBER_5 = SCORE_PATH / "5.png"
NUMBER_6 = SCORE_PATH / "6.png"
NUMBER_7 = SCORE_PATH / "7.png"
NUMBER_8 = SCORE_PATH / "8.png"
NUMBER_9 = SCORE_PATH / "9.png"

# Áudio
FLYING = AUDIO_PATH / "fly.wav"
COLLISION = AUDIO_PATH / "collision.wav"
POINT = AUDIO_PATH / "point.wav"
