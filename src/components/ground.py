"""
Componente de chão para o jogo Flappy Bird com efeito de parallax
Corresponde ao arquivo ground.dart do projeto Flutter
"""

from OpenGL.GL import * # type: ignore
from OpenGL.GL import glPushMatrix, glLoadIdentity, glEnable, glBindTexture, glBegin, glEnd, glDisable, glPopMatrix # type: ignore
from OpenGL.GL import glTexCoord2f, glVertex2f, GL_TEXTURE_2D, GL_QUADS # type: ignore
import numpy as np # type: ignore
import sys # type: ignore
import os # type: ignore
import typing # type: ignore

# Adiciona o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets import GROUND
from config import GROUND_HEIGHT, GAME_SPEED
from texture_manager import TextureManager

class Ground:
    """
    Classe para renderizar o chão com efeito de parallax (movimento contínuo).
    Equivalente à classe Ground do projeto Flutter:
    
    class Ground extends ParallaxComponent<FlappyBirdGame>
        with HasGameRef<FlappyBirdGame> {
      Ground();

      @override
      Future<void> onLoad() async {
        final ground = await Flame.images.load(Assets.ground);
        parallax = Parallax([
          ParallaxLayer(
            ParallaxImage(ground, fill: LayerFill.none),
          ),
        ]);
        add(
          RectangleHitbox(
            position: Vector2(0, gameRef.size.y - Config.groundHeight),
            size: Vector2(gameRef.size.x, Config.groundHeight),
          ),
        );
      }

      @override
      void update(double dt) {
        super.update(dt);
        parallax?.baseVelocity.x = Config.gameSpeed;
      }
    }
    """
    
    def __init__(self, texture_manager: TextureManager, window_width: float, window_height: float):
        """
        Inicializa o componente de chão
        
        Args:
            texture_manager: Gerenciador de texturas para carregar a imagem
            window_width: Largura da janela
            window_height: Altura da janela
        """
        self.width: float = window_width
        self.height: float = GROUND_HEIGHT
        self.window_height: float = window_height
        
        # Posição y do chão (parte inferior da tela)
        # No OpenGL, o eixo Y começa de baixo para cima
        self.y_position: float = 0  # Alterado: agora é 0 para estar na parte inferior
        
        # Posição x para o efeito de parallax (será atualizada para criar movimento)
        self.offset_x: float = 0.0
        
        # Carrega a textura do chão
        self.texture_id: typing.Optional[int] = texture_manager.load_texture(GROUND, "ground")
        
        # Configura a área de colisão do chão
        self.collision_rect: dict[str, float] = {
            'x': 0,
            'y': self.y_position,
            'width': window_width,
            'height': GROUND_HEIGHT
        }
        
    def update(self, delta_time: float) -> None:
        """
        Atualiza a posição do chão para criar efeito de movimento
        
        Args:
            delta_time: Tempo desde o último quadro em segundos
        """
        # Atualiza o offset x baseado na velocidade e no delta_time
        self.offset_x += GAME_SPEED * delta_time
        
        # Garante que o offset fique dentro de um range razoável para evitar problemas de precisão
        # com números de ponto flutuante após muito tempo de jogo
        self.offset_x %= self.width
        
    def render(self) -> None:
        """
        Renderiza o chão com efeito de parallax
        """
        # Verifica se a textura foi carregada corretamente
        if self.texture_id is None:
            return
            
        # Salva o estado da matriz atual
        glPushMatrix()
        
        # Reseta a matriz para identidade
        glLoadIdentity()
        
        # Ativa o mapeamento de texturas 2D
        glEnable(GL_TEXTURE_2D)
        
        # Vincula a textura do chão
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # Para criar o efeito de parallax, precisamos desenhar a textura do chão duas vezes,
        # uma ao lado da outra, e deslizar continuamente
        
        # Calcula as coordenadas de textura baseadas no offset
        tex_offset = self.offset_x / self.width
        
        # Desenha o chão
        glBegin(GL_QUADS)
        
        # Coordenadas de textura ajustadas para o offset
        # Alterado: Os vértices agora vão de 0 até a altura do chão,
        # posicionando-o na parte inferior da tela
        glTexCoord2f(tex_offset, 0)
        glVertex2f(0, self.y_position)
        
        glTexCoord2f(tex_offset + 1, 0)
        glVertex2f(self.width, self.y_position)
        
        glTexCoord2f(tex_offset + 1, 1)
        glVertex2f(self.width, self.y_position + self.height)
        
        glTexCoord2f(tex_offset, 1)
        glVertex2f(0, self.y_position + self.height)
        
        glEnd()
        
        # Desativa o mapeamento de texturas 2D
        glDisable(GL_TEXTURE_2D)
        
        # Restaura o estado da matriz anterior
        glPopMatrix()
        
    def check_collision(self, object_rect: dict[str, float]) -> bool:
        """
        Verifica se há colisão entre o chão e outro objeto
        
        Args:
            object_rect: Retângulo do objeto a verificar colisão (dict com x, y, width, height)
            
        Returns:
            bool: True se há colisão, False caso contrário
        """
        # Implementação simples de colisão AABB (Axis-Aligned Bounding Box)
        return (
            object_rect['x'] < self.collision_rect['x'] + self.collision_rect['width'] and
            object_rect['x'] + object_rect['width'] > self.collision_rect['x'] and
            object_rect['y'] < self.collision_rect['y'] + self.collision_rect['height'] and
            object_rect['y'] + object_rect['height'] > self.collision_rect['y']
        ) 