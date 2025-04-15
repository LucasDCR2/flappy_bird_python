"""
Componente de plano de fundo para o jogo Flappy Bird
Corresponde ao arquivo background.dart do projeto Flutter
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

from assets import BACKGROUND
from texture_manager import TextureManager

class Background:
    """
    Classe para renderizar o plano de fundo.
    Equivalente à classe Background do projeto Flutter:
    
    class Background extends SpriteComponent with HasGameRef<FlappyBirdGame> {
      Background();

      @override
      Future<void> onLoad() async {
        final background = await Flame.images.load(Assets.backgorund);
        size = gameRef.size;
        sprite = Sprite(background);
      }
    }
    """
    
    def __init__(self, texture_manager: TextureManager, window_width: float, window_height: float):
        """
        Inicializa o plano de fundo
        
        Args:
            texture_manager: Gerenciador de texturas para carregar a imagem
            window_width: Largura da janela
            window_height: Altura da janela
        """
        self.width: float = window_width
        self.height: float = window_height
        
        # Carrega a textura do plano de fundo
        self.texture_id: typing.Optional[int] = texture_manager.load_texture(BACKGROUND, "background")
        
    def render(self) -> None:
        """
        Renderiza o plano de fundo usando OpenGL
        Equivalente ao método render do Flame que é chamado automaticamente
        """
        # Verifica se a textura foi carregada corretamente
        if self.texture_id is None:
            return
            
        # Salva o estado da matriz atual
        glPushMatrix()
        
        # Reseta a matriz para identidade (limpa transformações anteriores)
        glLoadIdentity()
        
        # Ativa o mapeamento de texturas 2D
        glEnable(GL_TEXTURE_2D)
        
        # Vincula a textura do plano de fundo
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # Desenha um quadrilátero com a textura do plano de fundo
        glBegin(GL_QUADS)
        
        # Define coordenadas de textura e vértices para cada canto do quadrilátero
        # No OpenGL, o eixo Y começa de baixo para cima
        
        # Inferior esquerdo
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        
        # Inferior direito
        glTexCoord2f(1, 0)
        glVertex2f(self.width, 0)
        
        # Superior direito
        glTexCoord2f(1, 1)
        glVertex2f(self.width, self.height)
        
        # Superior esquerdo
        glTexCoord2f(0, 1)
        glVertex2f(0, self.height)
        
        glEnd()
        
        # Desativa o mapeamento de texturas 2D
        glDisable(GL_TEXTURE_2D)
        
        # Restaura o estado da matriz anterior
        glPopMatrix() 