"""
Componente de item de vida extra (coração) para o jogo Flappy Bird
"""

from OpenGL.GL import * # type: ignore
from OpenGL.GL import glPushMatrix, glEnable, glBindTexture, glBegin, glEnd, glDisable, glPopMatrix # type: ignore
from OpenGL.GL import glTexCoord2f, glVertex2f, GL_TEXTURE_2D, GL_QUADS, glTranslatef # type: ignore
import sys # type: ignore
import os # type: ignore
import typing # type: ignore
import random # type: ignore
import math  # Para a função sin usada na flutuação

# Adiciona o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets import HEART
from texture_manager import TextureManager
import config
from config import HEART_ITEM_WIDTH, HEART_ITEM_HEIGHT, HEART_ITEM_FLOAT_AMPLITUDE, HEART_ITEM_FLOAT_SPEED

class HeartItem:
    """
    Classe para representar um item de vida extra (coração) que o jogador pode coletar
    """
    
    def __init__(self, texture_manager: TextureManager, window_width: float, window_height: float):
        """
        Inicializa o item de coração
        
        Args:
            texture_manager: Gerenciador de texturas
            window_width: Largura da janela
            window_height: Altura da janela
        """
        self.window_width = window_width
        self.window_height = window_height
        
        # Carrega a textura do coração
        self.texture = texture_manager.load_texture(HEART, "heart_item")
        
        # Dimensões do item (usando valores do config)
        self.width = HEART_ITEM_WIDTH
        self.height = HEART_ITEM_HEIGHT
        
        # Posição inicial (fora da tela à direita)
        self.x = window_width + 100.0
        
        # Altura aleatória (entre 25% e 75% da altura total da tela)
        min_y = window_height * 0.25
        max_y = window_height * 0.75 - self.height
        self.y = random.uniform(min_y, max_y)
        
        # Velocidade do item (igual à dos canos)
        self.speed = config.PIPE_SPEED
        
        # Controla se o item está ativo (visível na tela)
        self.active = False
        
        # Adiciona um efeito de flutuação (usando valores do config)
        self.float_amplitude = HEART_ITEM_FLOAT_AMPLITUDE
        self.float_speed = HEART_ITEM_FLOAT_SPEED
        self.float_offset = random.uniform(0.0, 6.28)  # Valor aleatório entre 0 e 2*PI
        self.base_y = self.y
        self.time = 0.0
    
    def update(self, delta_time: float) -> None:
        """
        Atualiza a posição do item
        
        Args:
            delta_time: Tempo desde o último quadro em segundos
        """
        if not self.active:
            return
            
        # Atualiza a velocidade para acompanhar a dos canos
        self.speed = config.PIPE_SPEED
        
        # Move o item para a esquerda
        self.x -= self.speed * delta_time
        
        # Atualiza o efeito de flutuação
        self.time += delta_time
        self.y = self.base_y + self.float_amplitude * (
            math.sin(self.time * self.float_speed + self.float_offset)
        )
        
        # Verifica se o item saiu da tela
        if self.x + self.width < 0:
            self.active = False
    
    def render(self) -> None:
        """
        Renderiza o item na tela
        """
        if not self.active or self.texture is None:
            return
            
        # Salva o estado da matriz atual
        glPushMatrix()
        
        # Ativa o mapeamento de texturas 2D
        glEnable(GL_TEXTURE_2D)
        
        # Move para a posição do item
        glTranslatef(self.x, self.y, 0)
        
        # Vincula a textura do coração
        glBindTexture(GL_TEXTURE_2D, self.texture)
        
        # Desenha o quadrilátero com a textura
        glBegin(GL_QUADS)
        
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        
        glTexCoord2f(1, 0)
        glVertex2f(self.width, 0)
        
        glTexCoord2f(1, 1)
        glVertex2f(self.width, self.height)
        
        glTexCoord2f(0, 1)
        glVertex2f(0, self.height)
        
        glEnd()
        
        # Desativa o mapeamento de texturas 2D
        glDisable(GL_TEXTURE_2D)
        
        # Restaura o estado da matriz anterior
        glPopMatrix()
    
    def spawn(self) -> None:
        """
        Ativa o item e posiciona-o fora da tela à direita
        """
        self.active = True
        self.x = self.window_width + 100.0
        
        # Nova altura aleatória
        min_y = self.window_height * 0.25
        max_y = self.window_height * 0.75 - self.height
        self.base_y = random.uniform(min_y, max_y)
        self.y = self.base_y
        
        # Reinicia o tempo de flutuação com offset aleatório
        self.time = 0.0
        self.float_offset = random.uniform(0.0, 6.28)
    
    def is_colliding(self, bird_rect: typing.Dict[str, float]) -> bool:
        """
        Verifica se o pássaro está colidindo com o item
        
        Args:
            bird_rect: Retângulo de colisão do pássaro (dict com x, y, width, height)
            
        Returns:
            bool: True se há colisão, False caso contrário
        """
        if not self.active:
            return False
            
        # Verificação simples de colisão AABB (Axis-Aligned Bounding Box)
        return (
            bird_rect['x'] < self.x + self.width and
            bird_rect['x'] + bird_rect['width'] > self.x and
            bird_rect['y'] < self.y + self.height and
            bird_rect['y'] + bird_rect['height'] > self.y
        )
    
    def reset(self) -> None:
        """
        Reinicia o estado do item (desativa-o)
        """
        self.active = False
        
import math  # Adicionado para a função sin usada na flutuação 