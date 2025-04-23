"""
Configurações do jogo Flappy Bird
Arquivo central de configurações para todo o jogo
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
PIPE_INTERVAL: float = 1.5 # Intervalo mantido por compatibilidade
BIRD_VELOCITY: float = 300.0 
GRAVITY: float = -700.0 
CLOUDS_HEIGHT: float = 70.0 

# Configurações dos Canos
PIPE_SPEED: float = INITIAL_PIPE_SPEED # Velocidade atual de movimento dos canos
PIPE_GAP: float = 150.0 
PIPE_SPAWN_INTERVAL: float = INITIAL_PIPE_SPAWN_INTERVAL # Intervalo atual para spawn dos canos
PIPE_WIDTH: float = 70.0 
PIPE_HEIGHT: float = 400.0 

# Configurações do Player
MAX_LIVES: int = 3  # Número máximo de vidas do jogador

# Configurações de UI
HEART_WIDTH: float = 35.0  # Largura do coração no display de vidas
HEART_HEIGHT: float = 35.0  # Altura do coração no display de vidas
HEART_SPACING: float = 7.0  # Espaçamento entre os corações no display

SCORE_NUMBER_WIDTH: float = 36.0  # Largura dos números do score
SCORE_NUMBER_HEIGHT: float = 56.0  # Altura dos números do score
SCORE_NUMBER_SPACING: float = 2.0  # Espaçamento entre os números do score

# Configurações de Itens
HEART_ITEM_FREQUENCY: int = 20  # A cada quantos pontos aparece um item de vida
HEART_ITEM_WIDTH: float = 40.0  # Largura do item de coração
HEART_ITEM_HEIGHT: float = 40.0  # Altura do item de coração
HEART_ITEM_FLOAT_AMPLITUDE: float = 10.0  # Amplitude da flutuação do item
HEART_ITEM_FLOAT_SPEED: float = 2.0  # Velocidade da flutuação do item

# Configurações de Dificuldade
SPEED_INCREASE_FREQUENCY: int = 5  # A cada quantos pontos a velocidade aumenta
SPEED_INCREASE_MULTIPLIER: float = 1.10  # Fator de aumento da velocidade (10%)
