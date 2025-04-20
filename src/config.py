"""
Configurações do jogo Flappy Bird
Corresponde ao arquivo configuration.dart do projeto Flutter
"""

# Configurações da janela
WINDOW_WIDTH: int = 400
WINDOW_HEIGHT: int = 600
WINDOW_TITLE: str = "Flappy Bird"

# Configurações do jogo
GROUND_HEIGHT: float = 110.0
GAME_SPEED: float = 200.0
PIPE_INTERVAL: float = 1.5
BIRD_VELOCITY: float = 300.0
GRAVITY: float = -700.0
CLOUDS_HEIGHT: float = 70.0

# Configurações dos Canos
PIPE_SPEED: float = GAME_SPEED # Velocidade de movimento dos canos
PIPE_GAP: float = 150.0 # Tamanho do vão vertical entre os canos
PIPE_SPAWN_INTERVAL: float = 1.5 # Intervalo de tempo (segundos) para gerar novos canos
PIPE_WIDTH: float = 70.0 # Largura da textura do cano 
PIPE_HEIGHT: float = 400.0 # Altura da textura do cano 

# Corresponde aos valores em Config do projeto Flutter:
# static const groundHeight = 110.0;
# static const gameSpeed = 200.0;
# static const pipeInterval = 1.5;
# static const birdVelocity = 210;
# static const gravity = -100.0;
# static const cloudsHeight = 70.0;