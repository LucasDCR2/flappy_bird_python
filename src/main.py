"""
Ponto de entrada para o jogo Flappy Bird
Corresponde ao arquivo main.dart do projeto Flutter
"""

import glfw # type: ignore
from OpenGL.GL import * # type: ignore
from OpenGL.GL import GL_PROJECTION, GL_MODELVIEW, GL_COLOR_BUFFER_BIT # type: ignore
from OpenGL.GL import glViewport, glMatrixMode, glLoadIdentity, glOrtho, glClearColor, glClear # type: ignore
from OpenGL.GL import glEnable, glBlendFunc, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA # type: ignore
import time
import sys
import typing
import config # Importa o módulo config inteiro para modificar seus valores

# Importa módulos do jogo
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, MAX_LIVES
from config import SPEED_INCREASE_FREQUENCY, SPEED_INCREASE_MULTIPLIER, HEART_ITEM_FREQUENCY
from texture_manager import TextureManager
from components.background import Background
from components.ground import Ground
from components.bird import Bird
from components.pipe import PipeManager
from components.overlay import StartScreenOverlay, GameOverOverlay, HeartDisplay, ScoreDisplay
from components.heart_item import HeartItem

# Variáveis globais
lives: int = MAX_LIVES
texture_manager: typing.Optional[TextureManager] = None
background: typing.Optional[Background] = None
ground: typing.Optional[Ground] = None
bird: typing.Optional[Bird] = None
pipe_manager: typing.Optional[PipeManager] = None
start_screen: typing.Optional[StartScreenOverlay] = None
game_over_screen: typing.Optional[GameOverOverlay] = None
heart_display: typing.Optional[HeartDisplay] = None
score_display: typing.Optional[ScoreDisplay] = None
heart_item: typing.Optional[HeartItem] = None
last_time: float = 0
game_over: bool = False
score: int = 0
game_started: bool = False
last_speed_increase_score: int = 0 # Guarda a última pontuação que causou aumento de velocidade
last_heart_spawn_score: int = 0 # Guarda a última pontuação que gerou um item de vida

# Callback para teclas
def key_callback(window, key, scancode, action, mods) -> None:
    """
    Callback para eventos de teclado
    
    Args:
        window: Janela GLFW
        key: Tecla pressionada
        scancode: Código de varredura da tecla
        action: Ação (pressionar, soltar, etc.)
        mods: Modificadores (shift, ctrl, etc.)
    """
    global bird, game_over, game_started, start_screen
    
    # Tecla espaço para pular ou iniciar o jogo
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        if not game_started:
            # Inicia o jogo
            game_started = True
            if start_screen:
                start_screen.hide()
        elif not game_over and bird:
            bird.jump()
    
    # Tecla R para reiniciar o jogo
    if key == glfw.KEY_R and action == glfw.PRESS and game_over:
        restart_game()

def mouse_button_callback(window, button, action, mods) -> None:
    """
    Callback para eventos de mouse
    
    Args:
        window: Janela GLFW
        button: Botão do mouse
        action: Ação (pressionar, soltar)
        mods: Modificadores (shift, ctrl, etc.)
    """
    global bird, game_over, game_started, start_screen, game_over_screen
    
    # Obtém a posição do cursor
    x, y = glfw.get_cursor_pos(window)
    
    # Clique para pular ou iniciar o jogo
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        # Verifica se o botão de restart foi clicado
        if game_over and game_over_screen and game_over_screen.is_restart_button_clicked(x, y):
            restart_game()
        elif not game_started:
            # Inicia o jogo
            game_started = True
            if start_screen:
                start_screen.hide()
        elif not game_over and bird:
            bird.jump()

def restart_game() -> None:
    global bird, game_over, texture_manager, pipe_manager, score, game_started, game_over_screen
    global last_speed_increase_score, lives, heart_display, score_display, heart_item, last_heart_spawn_score

    # Se o jogo acabou de verdade, reseta vidas e score
    if lives <= 0:
        lives = MAX_LIVES
        score = 0
        last_speed_increase_score = 0
        last_heart_spawn_score = 0
        config.GAME_SPEED = config.INITIAL_GAME_SPEED
        config.PIPE_SPEED = config.INITIAL_PIPE_SPEED
        config.PIPE_SPAWN_INTERVAL = config.INITIAL_PIPE_SPAWN_INTERVAL
        print(f"Velocidade/Intervalo resetados: Chão={config.GAME_SPEED}, Canos={config.PIPE_SPEED}, Intervalo={config.PIPE_SPAWN_INTERVAL:.2f}")

    game_over = False

    if game_over_screen:
        game_over_screen.hide()

    if texture_manager:
        bird = Bird(texture_manager, WINDOW_WIDTH, WINDOW_HEIGHT)

    if pipe_manager:
        pipe_manager.reset()
        
    # Reseta o item de vida
    if heart_item:
        heart_item.reset()
        
    # Atualiza os displays
    if heart_display:
        heart_display.update_lives(lives)
    if score_display:
        score_display.update_score(score)

def check_collisions() -> bool:
    global bird, ground, pipe_manager, game_over, game_over_screen, score, lives, heart_display, heart_item

    if not bird or not ground or not pipe_manager:
        return False

    hit = False

    if ground.check_collision(bird.collision_rect):
        hit = True

    bird_hitbox = (bird.collision_rect['x'], bird.collision_rect['y'], bird.collision_rect['width'], bird.collision_rect['height'])
    if pipe_manager.check_collision(bird_hitbox):
        hit = True

    if bird.y + bird.height / 2 > WINDOW_HEIGHT:
        hit = True

    # Verifica colisão com o item de vida
    if heart_item and heart_item.active and heart_item.is_colliding(bird.collision_rect):
        # Adiciona uma vida e atualiza o display
        lives = min(lives + 1, MAX_LIVES)  # Limita ao máximo de vidas
        if heart_display:
            heart_display.update_lives(lives)
        
        # Toca um som de coleta (opcional)
        # se tiver um som de coleta, tocar aqui
        
        # Desativa o item após coletado
        heart_item.reset()
        
        print(f"Vida extra coletada! Vidas: {lives}")

    if hit:
        bird.die()
        lives -= 1
        print(f"Colidiu! Vidas restantes: {lives}")
        
        # Atualiza o display de corações
        if heart_display:
            heart_display.update_lives(lives)
            
        if lives <= 0:
            game_over = True
            if game_over_screen:
                game_over_screen.show_with_score(score)
        else:
            # Reinicia automaticamente para próxima vida
            restart_game()
        return True

    return False

def initialize() -> typing.Optional[typing.Any]:
    """
    Inicializa o jogo, configurações do GLFW e OpenGL
    Corresponde ao método main() do Flutter/Dart
    
    Returns:
        window: Objeto janela GLFW ou False em caso de erro
    """
    global texture_manager, background, ground, bird, pipe_manager
    global last_time, start_screen, game_over_screen, heart_display, score_display, heart_item
    
    # Inicializa GLFW
    if not glfw.init():
        print("Não foi possível inicializar o GLFW")
        return False
        
    # Cria uma janela em modo janela
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, None, None)
    
    if not window:
        print("Não foi possível criar a janela GLFW")
        glfw.terminate()
        return False
        
    # Torna o contexto da janela atual
    glfw.make_context_current(window)
    
    # Configura callbacks
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    
    # Configura o viewport
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # Configura a projeção ortográfica 2D
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    
    # Habilita blend para transparência
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Inicializa o gerenciador de texturas
    texture_manager = TextureManager()
    
    # Inicializa os componentes do jogo
    background = Background(texture_manager, WINDOW_WIDTH, WINDOW_HEIGHT)
    ground = Ground(texture_manager, WINDOW_WIDTH, WINDOW_HEIGHT)
    bird = Bird(texture_manager, WINDOW_WIDTH, WINDOW_HEIGHT)
    pipe_manager = PipeManager(texture_manager, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # Inicializa os overlays
    start_screen = StartScreenOverlay(texture_manager, WINDOW_WIDTH, WINDOW_HEIGHT)
    game_over_screen = GameOverOverlay(texture_manager, WINDOW_WIDTH, WINDOW_HEIGHT)
    heart_display = HeartDisplay(texture_manager, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_LIVES)
    score_display = ScoreDisplay(texture_manager, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # Inicializa o item de vida
    heart_item = HeartItem(texture_manager, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # Inicializa o tempo
    last_time = glfw.get_time()
    
    return window

def update(delta_time: float) -> None:
    """
    Atualiza o estado do jogo
    
    Args:
        delta_time: Tempo desde o último quadro em segundos
    """
    global ground, bird, pipe_manager, game_over, score, game_started
    global last_speed_increase_score, score_display, heart_item, last_heart_spawn_score
    
    # Atualiza o chão apenas se o jogo não terminou
    if ground and not game_over:
        ground.update(delta_time)
    
    # Se o jogo ainda não começou, aguarda ação do usuário
    if not game_started:
        return
        
    if not game_over:
        # Atualiza o pássaro
        if bird:
            bird.update(delta_time)
            
        # Atualiza o item de vida
        if heart_item:
            heart_item.update(delta_time)
            
        # Atualiza os canos e verifica pontuação
        if pipe_manager:
            pipe_manager.update(delta_time)
            if bird:
                points = pipe_manager.check_score(bird.x)
                if points > 0:
                    score += points
                    print(f"Pontuação: {score}")
                    
                    # Atualiza o display de pontuação
                    if score_display:
                        score_display.update_score(score)
                    
                    # Verifica se deve aumentar a velocidade (a cada SPEED_INCREASE_FREQUENCY pontos)
                    if score > 0 and score % SPEED_INCREASE_FREQUENCY == 0 and score > last_speed_increase_score:
                        speed_multiplier = SPEED_INCREASE_MULTIPLIER
                        config.GAME_SPEED *= speed_multiplier
                        config.PIPE_SPEED *= speed_multiplier
                        config.PIPE_SPAWN_INTERVAL /= speed_multiplier # Diminui o intervalo
                        print(f"Score {score}: Aumentando velocidade! Nova: Chão={config.GAME_SPEED:.2f}, Canos={config.PIPE_SPEED:.2f}, Intervalo={config.PIPE_SPAWN_INTERVAL:.2f}")
                        last_speed_increase_score = score # Atualiza a última pontuação que aumentou a velocidade
                    
                    # Verifica se deve spawnar um item de vida extra (a cada HEART_ITEM_FREQUENCY pontos)
                    if (score > 0 and score % HEART_ITEM_FREQUENCY == 0 and 
                        score > last_heart_spawn_score and heart_item and not heart_item.active):
                        heart_item.spawn()
                        last_heart_spawn_score = score
                        print(f"Score {score}: Spawning vida extra!")
            
        # Verifica colisões
        check_collisions()
    else:
        # Mesmo quando o jogo acabar, o pássaro continua atualizando para cair
        if bird:
            bird.update(delta_time)
    
def render() -> None:
    """
    Renderiza um quadro do jogo
    """
    # Limpa o buffer com uma cor de fundo
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Renderiza componentes na ordem correta (de trás para frente)
    if background:
        background.render()
    
    # Renderiza os canos apenas se o jogo já começou
    if game_started and pipe_manager:
        pipe_manager.render()
    
    # Renderiza o item de vida, se estiver ativo
    if game_started and heart_item and heart_item.active:
        heart_item.render()
    
    if ground:
        ground.render()
    
    if bird:
        bird.render()
    
    # Renderiza os overlays se estiverem visíveis
    if start_screen:
        start_screen.render()
        
    if game_over_screen:
        game_over_screen.render()
        
    # Renderiza o display de corações sempre que o jogo estiver em andamento
    if heart_display and game_started:
        heart_display.render()
        
    # Renderiza o display de pontuação se o jogo estiver em andamento
    if score_display and game_started:
        score_display.render()

def main() -> None:
    """
    Função principal do jogo
    """
    global last_time
    
    # Inicializa o jogo
    window = initialize()
    if not window:
        return
    
    # Loop principal
    while not glfw.window_should_close(window):
        # Calcula o delta time
        current_time = glfw.get_time()
        delta_time = current_time - last_time
        last_time = current_time
        
        # Limita o delta time para evitar problemas com pausas ou debugger
        delta_time = min(delta_time, 0.05)
        
        # Atualiza o estado do jogo
        update(delta_time)
        
        # Renderiza o quadro atual
        render()
        
        # Troca os buffers de front e back
        glfw.swap_buffers(window)
        
        # Processa eventos
        glfw.poll_events()
        
        # Escape para sair
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)
    
    # Limpa os recursos
    if texture_manager:
        texture_manager.cleanup()
        
    # Termina GLFW
    glfw.terminate()

if __name__ == "__main__":
    main() 