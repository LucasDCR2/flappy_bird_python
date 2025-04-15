"""
Componente de canos (pipes) para o jogo Flappy Bird
Corresponde ao arquivo pipe.dart do projeto Flutter
"""

from OpenGL.GL import * # type: ignore
from OpenGL.GL import glPushMatrix, glLoadIdentity, glEnable, glBindTexture, glBegin, glEnd, glDisable, glPopMatrix # type: ignore
from OpenGL.GL import glTexCoord2f, glVertex2f, GL_TEXTURE_2D, GL_QUADS, glTranslatef # type: ignore
import numpy as np # type: ignore
import sys # type: ignore
import os # type: ignore
import typing # type: ignore
import random # type: ignore

# Adiciona o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets import PIPE, PIPE_ROTATED
from config import GAME_SPEED, PIPE_INTERVAL
from texture_manager import TextureManager

class Pipe:
    """
    Classe para renderizar e gerenciar um par de canos (superior e inferior)
    """
    
    def __init__(self, texture_manager: TextureManager, window_width: float, window_height: float, x_position: float):
        """
        Inicializa um par de canos
        
        Args:
            texture_manager: Gerenciador de texturas para carregar as imagens
            window_width: Largura da janela
            window_height: Altura da janela
            x_position: Posição x inicial do cano
        """
        self.width: float = 52.0
        self.height: float = 320.0
        self.window_width: float = window_width
        self.window_height: float = window_height
        
        # Posição x inicial (geralmente fora da tela à direita)
        self.x: float = x_position
        
        # Tamanho do espaço entre os canos (abertura para o pássaro passar)
        # Varia entre 140 e 180 para ter níveis diferentes de dificuldade
        self.gap_size: float = random.uniform(100.0, 180.0)
        
        # Posição y do espaço (aleatória, mas mantendo os canos visíveis na tela)
        # Usamos três zonas possíveis para o gap: inferior, média e superior
        zone = random.randint(0, 2)  # 0 = inferior, 1 = média, 2 = superior
        
        # Altura mínima para evitar que os canos fiquem muito perto da borda
        min_height = 60
        
        if zone == 0:  # Zona inferior - gap mais perto do chão
            min_gap_y = min_height + 80
            max_gap_y = self.window_height * 0.35
        elif zone == 1:  # Zona média - gap no meio da tela
            min_gap_y = self.window_height * 0.35
            max_gap_y = self.window_height * 0.65
        else:  # Zona superior - gap mais perto do topo
            min_gap_y = self.window_height * 0.65
            max_gap_y = self.window_height - min_height - self.gap_size
        
        self.gap_y: float = random.uniform(min_gap_y, max_gap_y)
        
        # Carrega as texturas dos canos
        self.texture_pipe: typing.Optional[int] = texture_manager.load_texture(PIPE, "pipe")
        self.texture_pipe_rotated: typing.Optional[int] = texture_manager.load_texture(PIPE_ROTATED, "pipe_rotated")
        
        # Retângulos de colisão para ambos os canos
        self.update_collision_rects()
        
        # Flag para controlar se o pássaro já passou por este cano
        self.passed: bool = False
        
    def update_collision_rects(self) -> None:
        """
        Atualiza os retângulos de colisão dos canos
        """
        # Cano superior (invertido)
        self.upper_rect: dict[str, float] = {
            'x': self.x - self.width / 2,
            'y': self.gap_y + self.gap_size / 2,
            'width': self.width,
            'height': self.window_height
        }
        
        # Cano inferior
        self.lower_rect: dict[str, float] = {
            'x': self.x - self.width / 2,
            'y': 0,
            'width': self.width,
            'height': self.gap_y - self.gap_size / 2
        }
        
    def update(self, delta_time: float) -> None:
        """
        Atualiza a posição dos canos
        
        Args:
            delta_time: Tempo desde o último quadro em segundos
        """
        # Move os canos para a esquerda
        self.x -= GAME_SPEED * delta_time
        
        # Atualiza os retângulos de colisão
        self.update_collision_rects()
        
    def render(self) -> None:
        """
        Renderiza o par de canos
        """
        # Verifica se as texturas foram carregadas corretamente
        if self.texture_pipe is None or self.texture_pipe_rotated is None:
            return
            
        # Salva o estado da matriz atual
        glPushMatrix()
        
        # Ativa o mapeamento de texturas 2D
        glEnable(GL_TEXTURE_2D)
        
        # --- Renderiza o cano inferior ---
        # Reseta a matriz para identidade e move para a posição do cano
        glLoadIdentity()
        glTranslatef(self.x, 0, 0)
        
        # Vincula a textura do cano
        glBindTexture(GL_TEXTURE_2D, self.texture_pipe)
        
        # Define a altura do cano inferior (de 0 até a parte inferior do espaço)
        lower_pipe_height = self.gap_y - self.gap_size / 2
        
        glBegin(GL_QUADS)
        
        # Coordenadas de textura e vértices
        # Define as coordenadas para cano inferior centralizado na posição x
        half_width = self.width / 2
        
        glTexCoord2f(0, 0)
        glVertex2f(-half_width, 0)
        
        glTexCoord2f(1, 0)
        glVertex2f(half_width, 0)
        
        glTexCoord2f(1, lower_pipe_height / self.height)
        glVertex2f(half_width, lower_pipe_height)
        
        glTexCoord2f(0, lower_pipe_height / self.height)
        glVertex2f(-half_width, lower_pipe_height)
        
        glEnd()
        
        # --- Renderiza o cano superior (invertido) ---
        # Reseta a matriz para identidade e move para a posição do cano superior
        glLoadIdentity()
        glTranslatef(self.x, self.gap_y + self.gap_size / 2, 0)
        
        # Vincula a textura do cano invertido
        glBindTexture(GL_TEXTURE_2D, self.texture_pipe_rotated)
        
        # Altura do cano superior (da parte superior do espaço até o topo da tela)
        upper_pipe_height = self.window_height - (self.gap_y + self.gap_size / 2)
        
        glBegin(GL_QUADS)
        
        glTexCoord2f(0, 0)
        glVertex2f(-half_width, 0)
        
        glTexCoord2f(1, 0)
        glVertex2f(half_width, 0)
        
        glTexCoord2f(1, upper_pipe_height / self.height)
        glVertex2f(half_width, upper_pipe_height)
        
        glTexCoord2f(0, upper_pipe_height / self.height)
        glVertex2f(-half_width, upper_pipe_height)
        
        glEnd()
        
        # Desativa o mapeamento de texturas 2D
        glDisable(GL_TEXTURE_2D)
        
        # Restaura o estado da matriz anterior
        glPopMatrix()
        
    def is_visible(self) -> bool:
        """
        Verifica se o cano ainda está visível na tela
        
        Returns:
            bool: True se o cano ainda está visível, False caso contrário
        """
        return self.x + self.width / 2 > 0
        
    def check_collision(self, object_rect: dict[str, float]) -> bool:
        """
        Verifica se há colisão entre o objeto e qualquer um dos canos
        
        Args:
            object_rect: Retângulo do objeto a verificar colisão (dict com x, y, width, height)
            
        Returns:
            bool: True se há colisão, False caso contrário
        """
        # Verifica colisão com o cano superior
        if (object_rect['x'] < self.upper_rect['x'] + self.upper_rect['width'] and
            object_rect['x'] + object_rect['width'] > self.upper_rect['x'] and
            object_rect['y'] < self.upper_rect['y'] + self.upper_rect['height'] and
            object_rect['y'] + object_rect['height'] > self.upper_rect['y']):
            return True
            
        # Verifica colisão com o cano inferior
        if (object_rect['x'] < self.lower_rect['x'] + self.lower_rect['width'] and
            object_rect['x'] + object_rect['width'] > self.lower_rect['x'] and
            object_rect['y'] < self.lower_rect['y'] + self.lower_rect['height'] and
            object_rect['y'] + object_rect['height'] > self.lower_rect['y']):
            return True
            
        return False
        
    def check_passed(self, bird_x: float) -> bool:
        """
        Verifica se o pássaro passou por este cano
        
        Args:
            bird_x: Posição x do pássaro
            
        Returns:
            bool: True se o pássaro passou pelo cano e isso ainda não havia sido registrado
        """
        if not self.passed and bird_x > self.x:
            self.passed = True
            return True
        return False

class PipeManager:
    """
    Classe para gerenciar múltiplos canos no jogo
    """
    
    def __init__(self, texture_manager: TextureManager, window_width: float, window_height: float):
        """
        Inicializa o gerenciador de canos
        
        Args:
            texture_manager: Gerenciador de texturas
            window_width: Largura da janela
            window_height: Altura da janela
        """
        self.texture_manager: TextureManager = texture_manager
        self.window_width: float = window_width
        self.window_height: float = window_height
        
        # Lista de canos ativos
        self.pipes: list[Pipe] = []
        
        # Temporizador para criação de novos canos
        self.timer: float = 0.0
        
        # Ponto de partida dos canos (fora da tela à direita)
        self.spawn_x: float = window_width + 100
        
    def update(self, delta_time: float) -> int:
        """
        Atualiza todos os canos e cria novos canos quando necessário
        
        Args:
            delta_time: Tempo desde o último quadro em segundos
            
        Returns:
            int: Número de pontos obtidos neste frame (por passar por canos)
        """
        points = 0
        
        # Atualiza o temporizador
        self.timer += delta_time
        
        # Cria um novo cano quando o temporizador atingir o intervalo
        if self.timer >= PIPE_INTERVAL:
            self.pipes.append(Pipe(self.texture_manager, self.window_width, self.window_height, self.spawn_x))
            self.timer = 0.0
            
        # Atualiza cada cano e verifica se ele saiu da tela
        pipes_to_remove = []
        for pipe in self.pipes:
            pipe.update(delta_time)
            
            # Se o cano não estiver mais visível, marca para remoção
            if not pipe.is_visible():
                pipes_to_remove.append(pipe)
                
        # Remove canos que saíram da tela
        for pipe in pipes_to_remove:
            self.pipes.remove(pipe)
            
        return points
        
    def render(self) -> None:
        """
        Renderiza todos os canos
        """
        for pipe in self.pipes:
            pipe.render()
            
    def check_collision(self, object_rect: dict[str, float]) -> bool:
        """
        Verifica se há colisão entre o objeto e qualquer um dos canos
        
        Args:
            object_rect: Retângulo do objeto a verificar colisão
            
        Returns:
            bool: True se há colisão, False caso contrário
        """
        for pipe in self.pipes:
            if pipe.check_collision(object_rect):
                return True
        return False
        
    def check_score(self, bird_x: float) -> int:
        """
        Verifica se o pássaro passou por algum cano e adiciona pontos
        
        Args:
            bird_x: Posição x do pássaro
            
        Returns:
            int: Número de pontos obtidos neste frame
        """
        points = 0
        for pipe in self.pipes:
            if pipe.check_passed(bird_x):
                points += 1
        return points
        
    def reset(self) -> None:
        """
        Reinicia o gerenciador de canos
        """
        self.pipes.clear()
        self.timer = 0.0 