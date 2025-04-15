"""
Componente pássaro para o jogo Flappy Bird
Corresponde ao arquivo bird.dart do projeto Flutter
"""

from OpenGL.GL import * # type: ignore
from OpenGL.GL import glPushMatrix, glLoadIdentity, glEnable, glBindTexture, glBegin, glEnd, glDisable, glPopMatrix # type: ignore
from OpenGL.GL import glTexCoord2f, glVertex2f, GL_TEXTURE_2D, GL_QUADS, glTranslatef, glRotatef # type: ignore
import numpy as np # type: ignore
import sys # type: ignore
import os # type: ignore
import typing # type: ignore
import math # type: ignore

# Adiciona o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets import BIRD_DOWN_FLAP, BIRD_MID_FLAP, BIRD_UP_FLAP
from config import BIRD_VELOCITY, GRAVITY
from texture_manager import TextureManager

# Enum para movimento do pássaro (similar ao BirdMovement do Flutter)
class BirdMovement:
    UP = 0    # Asas para cima - voando para cima
    MIDDLE = 1  # Asas no meio - transição
    DOWN = 2  # Asas para baixo - caindo

class Bird:
    """
    Classe para renderizar e controlar o pássaro do jogo.
    Implementa física e animações.
    Corresponde à classe Bird do projeto Flutter.
    """
    
    def __init__(self, texture_manager: TextureManager, window_width: float, window_height: float):
        """
        Inicializa o componente do pássaro
        
        Args:
            texture_manager: Gerenciador de texturas para carregar as imagens
            window_width: Largura da janela
            window_height: Altura da janela
        """
        # Posição e dimensões
        self.width: float = 40.0
        self.height: float = 28.0
        self.window_width: float = window_width
        self.window_height: float = window_height
        
        # Posição inicial do pássaro (centro da tela, um pouco mais ao topo)
        self.x: float = window_width / 3
        self.y: float = window_height / 2 + 50
        
        # Velocidade e aceleração
        self.velocity: float = 0.0
        self.rotation: float = 0.0
        
        # Estado do jogo
        self.is_dead: bool = False
        
        # Carrega as texturas do pássaro para animação
        self.texture_down: typing.Optional[int] = texture_manager.load_texture(BIRD_DOWN_FLAP, "bird_down")
        self.texture_up: typing.Optional[int] = texture_manager.load_texture(BIRD_UP_FLAP, "bird_up")
        self.texture_mid: typing.Optional[int] = texture_manager.load_texture(BIRD_MID_FLAP, "bird_mid")
        
        # Começa no estado médio
        self.current_movement: int = BirdMovement.MIDDLE
        
        # Temporizador para transição da animação
        self.animation_timer: float = 0.0
        self.animation_transition: float = 0.2  # segundos
        
        # Retângulo de colisão (hitbox menor que o sprite para melhor gameplay)
        self.collision_rect: dict[str, float] = {
            'x': self.x - self.width / 3,
            'y': self.y - self.height / 3,
            'width': self.width * 2/3,
            'height': self.height * 2/3
        }
    
    def jump(self) -> None:
        """
        Faz o pássaro pular/voar
        Corresponde ao método fly() no projeto Flutter
        """
        if not self.is_dead:
            self.velocity = BIRD_VELOCITY
            self.current_movement = BirdMovement.UP  # muda para sprite com asas para cima
            self.animation_timer = 0.0  # reinicia o temporizador
    
    def update(self, delta_time: float) -> None:
        """
        Atualiza a posição, velocidade e animação do pássaro
        
        Args:
            delta_time: Tempo desde o último quadro em segundos
        """
        if self.is_dead:
            # Se o pássaro está morto, apenas cai no chão
            self.velocity += GRAVITY * delta_time * 2  # Gravidade mais forte quando morto
            self.y += self.velocity * delta_time
            
            # Aumenta a rotação para simular queda
            self.rotation -= 350.0 * delta_time
            if self.rotation < -90.0:
                self.rotation = -90.0
                
            # Mantém o sprite com asas para baixo quando morto
            self.current_movement = BirdMovement.DOWN
        else:
            # Física normal
            self.velocity += GRAVITY * delta_time
            self.y += self.velocity * delta_time
            
            # Atualiza a rotação com base na velocidade
            # Inverte o sinal para que valores positivos de velocidade resultem em rotação positiva (para cima)
            # e valores negativos de velocidade resultem em rotação negativa (para baixo)
            target_rotation = math.degrees(math.atan2(self.velocity, BIRD_VELOCITY))
            # Limita a rotação (com ângulos menores)
            target_rotation = max(-20, min(20, target_rotation))
            # Suaviza a rotação
            self.rotation = self.rotation * 0.01 + target_rotation * 0.99
            
            # Controle de animação com base no estado atual e temporizador
            if self.current_movement == BirdMovement.UP:
                # Se estiver no estado "para cima", espera um pouco e muda para o meio
                self.animation_timer += delta_time
                if self.animation_timer >= self.animation_transition:
                    self.current_movement = BirdMovement.MIDDLE
                    self.animation_timer = 0.0
            elif self.current_movement == BirdMovement.MIDDLE and self.velocity < -50:
                # Se estiver no estado "meio" e caindo com certa velocidade, muda para baixo
                self.current_movement = BirdMovement.DOWN
        
        # Atualiza a hitbox
        self.collision_rect = {
            'x': self.x - self.width / 3,
            'y': self.y - self.height / 3,
            'width': self.width * 2/3,
            'height': self.height * 2/3
        }
    
    def render(self) -> None:
        """
        Renderiza o pássaro com animação e rotação
        """
        # Determina qual textura usar com base no movimento atual
        texture_id = None
        if self.current_movement == BirdMovement.UP:
            texture_id = self.texture_up
        elif self.current_movement == BirdMovement.MIDDLE:
            texture_id = self.texture_mid
        else:  # BirdMovement.DOWN
            texture_id = self.texture_down
            
        # Verifica se a textura foi carregada corretamente
        if texture_id is None:
            return
            
        # Salva o estado da matriz atual
        glPushMatrix()
        
        # Move para a posição do pássaro e aplica rotação
        glTranslatef(self.x, self.y, 0)
        glRotatef(self.rotation, 0, 0, 1)
        
        # Ativa o mapeamento de texturas 2D
        glEnable(GL_TEXTURE_2D)
        
        # Vincula a textura do pássaro
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        # Desenha o pássaro como um quadrilátero centrado
        half_width = self.width / 2
        half_height = self.height / 2
        
        glBegin(GL_QUADS)
        
        # Coordenadas de textura e vértices
        glTexCoord2f(0, 0)
        glVertex2f(-half_width, -half_height)
        
        glTexCoord2f(1, 0)
        glVertex2f(half_width, -half_height)
        
        glTexCoord2f(1, 1)
        glVertex2f(half_width, half_height)
        
        glTexCoord2f(0, 1)
        glVertex2f(-half_width, half_height)
        
        glEnd()
        
        # Desativa o mapeamento de texturas 2D
        glDisable(GL_TEXTURE_2D)
        
        # Restaura o estado da matriz anterior
        glPopMatrix()
    
    def check_collision(self, object_rect: dict[str, float]) -> bool:
        """
        Verifica se há colisão entre o pássaro e outro objeto
        
        Args:
            object_rect: Retângulo do objeto a verificar colisão (dict com x, y, width, height)
            
        Returns:
            bool: True se há colisão, False caso contrário
        """
        # Implementação de colisão AABB (Axis-Aligned Bounding Box)
        return (
            self.collision_rect['x'] < object_rect['x'] + object_rect['width'] and
            self.collision_rect['x'] + self.collision_rect['width'] > object_rect['x'] and
            self.collision_rect['y'] < object_rect['y'] + object_rect['height'] and
            self.collision_rect['y'] + self.collision_rect['height'] > object_rect['y']
        )
        
    def die(self) -> None:
        """
        Marca o pássaro como morto
        """
        self.is_dead = True 