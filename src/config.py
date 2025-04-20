"""
Configurações do jogo Flappy Bird
Corresponde ao arquivo configuration.dart do projeto Flutter
"""

# Configurações da janela
WINDOW_WIDTH: int = 400
WINDOW_HEIGHT: int = 600
WINDOW_TITLE: str = "Flappy Bird"

# --- Configurações Iniciais ---
INITIAL_GAME_SPEED: float = 200.0 
INITIAL_PIPE_SPEED: float = INITIAL_GAME_SPEED

# --- Configurações Atuais (Podem mudar durante o jogo) ---
GROUND_HEIGHT: float = 110.0
GAME_SPEED: float = INITIAL_GAME_SPEED  # Velocidade atual do chão
INITIAL_PIPE_SPAWN_INTERVAL: float = 1.5 # Intervalo inicial para spawn dos canos
PIPE_INTERVAL: float = 1.5 # Mantido? (Se não for usado, pode remover)
BIRD_VELOCITY: float = 300.0 
GRAVITY: float = -700.0 
CLOUDS_HEIGHT: float = 70.0 

# Configurações dos Canos (Velocidade atual)
PIPE_SPEED: float = INITIAL_PIPE_SPEED # Velocidade atual de movimento dos canos
PIPE_GAP: float = 150.0 
PIPE_SPAWN_INTERVAL: float = INITIAL_PIPE_SPAWN_INTERVAL # Intervalo atual para spawn dos canos
PIPE_WIDTH: float = 70.0 
PIPE_HEIGHT: float = 400.0 
