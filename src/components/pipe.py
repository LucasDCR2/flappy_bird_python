"""
Define as classes Pipe e PipeManager para o jogo Flappy Bird
"""

import random
import typing
import sys
import os
from OpenGL.GL import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from texture_manager import TextureManager
from config import PIPE_SPEED, PIPE_GAP, PIPE_SPAWN_INTERVAL, PIPE_HEIGHT, PIPE_WIDTH
import assets

# Assume um tipo simples para retângulo de colisão (x, y, width, height)
CollisionRect = typing.Tuple[float, float, float, float]

class Pipe:
    """
    Representa um único cano (superior ou inferior)
    """
    def __init__(self, texture_manager: TextureManager, x: float, y: float, is_top_pipe: bool):
        """
        Inicializa um cano
        
        Args:
            texture_manager: Gerenciador de texturas para carregar a imagem do cano
            x: Posição X inicial do cano
            y: Posição Y inicial do cano
            is_top_pipe: True se for o cano superior, False se for o inferior
        """
        self.texture_manager = texture_manager
        self.x = x
        self.y = y
        self.is_top_pipe = is_top_pipe
        
        # Carrega a textura apropriada
        texture_path = assets.PIPE_ROTATED if is_top_pipe else assets.PIPE
        self.texture_id = self.texture_manager.load_texture(texture_path)
        
        # Dimensões definidas em config.py
        self.width = PIPE_WIDTH 
        self.height = PIPE_HEIGHT 
        
        self.scored = False # Flag para indicar se o pássaro passou por este cano

    def update(self, delta_time: float) -> None:
        """
        Atualiza a posição do cano
        
        Args:
            delta_time: Tempo desde o último quadro
        """
        self.x -= PIPE_SPEED * delta_time

    def render(self) -> None:
        """
        Renderiza o cano na tela
        """
        if self.texture_id is not None:
            # O 'y' do cano já representa a borda inferior.
            # glTranslatef deve mover para a canto inferior esquerdo onde o quad será desenhado.
            render_y = self.y 
            
            # Salva o estado da matriz atual
            glPushMatrix()
            
            # Move para a posição do cano
            glTranslatef(self.x, render_y, 0)
            
            # Ativa o mapeamento de texturas 2D e blend (se necessário)
            glEnable(GL_TEXTURE_2D)
            # glEnable(GL_BLEND) # Blend já deve estar habilitado globalmente em main.py
            # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # Blend já deve estar habilitado globalmente em main.py
            
            # Vincula a textura do cano
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            
            # Desenha o cano como um quadrilátero
            glBegin(GL_QUADS)
            
            # Coordenadas de textura (0,0) a (1,1) e vértices (0,0) a (width, height)
            glTexCoord2f(0, 0); glVertex2f(0, 0)
            glTexCoord2f(1, 0); glVertex2f(self.width, 0)
            glTexCoord2f(1, 1); glVertex2f(self.width, self.height)
            glTexCoord2f(0, 1); glVertex2f(0, self.height)
            
            glEnd()
            
            # Desativa o mapeamento de texturas 2D
            glDisable(GL_TEXTURE_2D)
            # glDisable(GL_BLEND) # Não desabilitar o blend globalmente aqui
            
            # Restaura o estado da matriz anterior
            glPopMatrix()

    @property
    def collision_rect(self) -> CollisionRect:
        """
        Retorna o retângulo de colisão para este cano (x, y, width, height)
        Onde y é a borda inferior.
        """
        # self.y já representa a borda inferior.
        rect_y = self.y
        return (self.x, rect_y, self.width, self.height)
        
    def is_offscreen(self, window_width: int) -> bool:
        """
        Verifica se o cano está fora da tela (à esquerda)
        """
        return self.x + self.width < 0


class PipeManager:
    """
    Gerencia a criação, atualização e renderização dos pares de canos
    """
    def __init__(self, texture_manager: TextureManager, window_width: int, window_height: int):
        """
        Inicializa o gerenciador de canos
        
        Args:
            texture_manager: Gerenciador de texturas
            window_width: Largura da janela
            window_height: Altura da janela
        """
        self.texture_manager = texture_manager
        self.window_width = window_width
        self.window_height = window_height
        self._pipes: typing.List[Pipe] = []
        self._spawn_timer: float = 0.0
        self._last_scored_pipe: typing.Optional[Pipe] = None # Para evitar pontuação múltipla

        # Define os limites para a altura do vão dos canos
        # Ajustado para garantir que o cano não saia completamente da tela
        self._min_pipe_height = 100 # Mínimo de espaço visível do cano
        self._max_pipe_height = self.window_height - PIPE_GAP - self._min_pipe_height

    def _spawn_pipe(self) -> None:
        """
        Cria um novo par de canos (superior e inferior) com um vão aleatório
        """
        # Altura aleatória para o cano inferior (ou a base do vão)
        gap_y = random.uniform(self._min_pipe_height, self._max_pipe_height)
        
        # Posição inicial X (fora da tela à direita)
        initial_x = float(self.window_width)
        
        # Cria o cano inferior
        bottom_pipe = Pipe(self.texture_manager, initial_x, gap_y - PIPE_HEIGHT, False) # y é o topo do cano inferior
        
        # Cria o cano superior
        top_pipe_y = gap_y + PIPE_GAP # y é a base do cano superior
        top_pipe = Pipe(self.texture_manager, initial_x, top_pipe_y, True)
        
        self._pipes.append(bottom_pipe)
        self._pipes.append(top_pipe)
        
        # Reseta o timer de spawn, adicionando uma pequena variação
        self._spawn_timer = random.uniform(-0.2, 0.2) # Pequena variação no próximo spawn

    def update(self, delta_time: float) -> None:
        """
        Atualiza todos os canos, remove os que saíram da tela e gera novos canos
        
        Args:
            delta_time: Tempo desde o último quadro
        """
        # Atualiza o timer de spawn
        self._spawn_timer += delta_time
        if self._spawn_timer >= PIPE_SPAWN_INTERVAL:
            self._spawn_pipe()
            # Não reseta completamente para 0, usa o valor já calculado em _spawn_pipe
            # self._spawn_timer = 0.0 # Resetado dentro de _spawn_pipe com variação

        # Atualiza a posição de cada cano
        for pipe in self._pipes:
            pipe.update(delta_time)

        # Remove canos que saíram da tela (otimização)
        # Filtra a lista, mantendo apenas os canos visíveis
        self._pipes = [pipe for pipe in self._pipes if not pipe.is_offscreen(self.window_width)]

    def render(self) -> None:
        """
        Renderiza todos os canos ativos
        """
        for pipe in self._pipes:
            pipe.render()

    def check_collision(self, bird_rect: CollisionRect) -> bool:
        """
        Verifica se o retângulo do pássaro colide com algum dos canos
        
        Args:
            bird_rect: Retângulo de colisão do pássaro (x, y, width, height)
            
        Returns:
            True se houver colisão, False caso contrário
        """
        bird_x, bird_y, bird_w, bird_h = bird_rect
        
        for pipe in self._pipes:
            pipe_x, pipe_y, pipe_w, pipe_h = pipe.collision_rect
            
            # Verificação simples de colisão AABB (Axis-Aligned Bounding Box)
            if (bird_x < pipe_x + pipe_w and
                bird_x + bird_w > pipe_x and
                bird_y < pipe_y + pipe_h and
                bird_y + bird_h > pipe_y):
                return True # Colisão detectada
                
        return False # Nenhuma colisão

    def check_score(self, bird_x: float) -> int:
        """
        Verifica se o pássaro passou por um par de canos para pontuar
        
        Args:
            bird_x: Posição X do pássaro
            
        Returns:
            1 se um novo par de canos foi passado, 0 caso contrário
        """
        scored_point = 0
        # Consideramos apenas os canos inferiores para verificar a passagem
        # E garantimos que o pássaro esteja após o início do cano
        potential_scoring_pipes = [p for p in self._pipes if not p.is_top_pipe and not p.scored and p.x + p.width < bird_x]

        if potential_scoring_pipes:
             # Ordena por x para garantir que estamos pegando o próximo cano a ser pontuado
            closest_pipe_to_pass = min(potential_scoring_pipes, key=lambda p: p.x)
            
            # Verifica se este cano já foi o último a ser pontuado para evitar contagem dupla rápida
            if self._last_scored_pipe != closest_pipe_to_pass:
                 closest_pipe_to_pass.scored = True
                 self._last_scored_pipe = closest_pipe_to_pass # Marca este como o último pontuado
                 scored_point = 1

        return scored_point


    def reset(self) -> None:
        """
        Remove todos los canos e reinicia o timer de spawn
        """
        self._pipes.clear()
        self._spawn_timer = 0.0
        self._last_scored_pipe = None # Reseta o último cano pontuado
