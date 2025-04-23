"""
Componentes de overlay para o jogo Flappy Bird
Corresponde aos arquivos main_menu_screen.dart e game_over_screen.dart do projeto Flutter
"""

from OpenGL.GL import * # type: ignore
from OpenGL.GL import glPushMatrix, glLoadIdentity, glEnable, glBindTexture, glBegin, glEnd, glDisable, glPopMatrix # type: ignore
from OpenGL.GL import glTexCoord2f, glVertex2f, GL_TEXTURE_2D, GL_QUADS, glTranslatef, glColor4f, glColor3f # type: ignore
import numpy as np # type: ignore
import sys # type: ignore
import os # type: ignore
import typing # type: ignore

# Adiciona o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets import MESSAGE, GAME_OVER, HEART
from assets import NUMBER_0, NUMBER_1, NUMBER_2, NUMBER_3, NUMBER_4, NUMBER_5, NUMBER_6, NUMBER_7, NUMBER_8, NUMBER_9
from texture_manager import TextureManager
from config import HEART_WIDTH, HEART_HEIGHT, HEART_SPACING, SCORE_NUMBER_WIDTH, SCORE_NUMBER_HEIGHT, SCORE_NUMBER_SPACING, MAX_LIVES

class Overlay:
    """
    Classe base para componentes de overlay que serão renderizados 
    sobre o jogo em situações específicas
    """
    
    def __init__(self, texture_manager: TextureManager, window_width: float, window_height: float):
        """
        Inicializa o overlay
        
        Args:
            texture_manager: Gerenciador de texturas
            window_width: Largura da janela
            window_height: Altura da janela
        """
        self.window_width: float = window_width
        self.window_height: float = window_height
        self.texture_manager: TextureManager = texture_manager
        self.is_visible: bool = False
        
    def show(self) -> None:
        """
        Torna o overlay visível
        """
        self.is_visible = True
        
    def hide(self) -> None:
        """
        Esconde o overlay
        """
        self.is_visible = False
        
    def render(self) -> None:
        """
        Renderiza o overlay
        """
        if self.is_visible:
            self._render_impl()
            
    def _render_impl(self) -> None:
        """
        Implementação específica de renderização para cada tipo de overlay
        Deve ser sobrescrita pelas subclasses
        """
        pass
        
    def _render_semitransparent_background(self) -> None:
        """
        Renderiza um fundo semi-transparente
        """
        # Salva o estado da matriz atual
        glPushMatrix()
        
        # Reseta a matriz
        glLoadIdentity()
        
        # Configura uma cor semi-transparente (preto com 70% de opacidade)
        glColor4f(0.0, 0.0, 0.0, 0.7)
        
        # Desenha um retângulo que cobre toda a tela
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.window_width, 0)
        glVertex2f(self.window_width, self.window_height)
        glVertex2f(0, self.window_height)
        glEnd()
        
        # Restaura a cor para branco opaco
        glColor4f(1.0, 1.0, 1.0, 1.0)
        
        # Restaura o estado da matriz
        glPopMatrix()

class StartScreenOverlay(Overlay):
    """
    Tela de início "Get Ready" que é exibida antes do jogo começar
    Corresponde ao MainMenuScreen no projeto Flutter
    """
    
    def __init__(self, texture_manager: TextureManager, window_width: float, window_height: float):
        """
        Inicializa a tela de início
        
        Args:
            texture_manager: Gerenciador de texturas
            window_width: Largura da janela
            window_height: Altura da janela
        """
        super().__init__(texture_manager, window_width, window_height)
        self.is_visible = True  # Começa visível
        
        # Carrega a textura da mensagem "Get Ready"
        self.message_texture: typing.Optional[int] = texture_manager.load_texture(MESSAGE, "message")
        
        # Dimensões da textura da mensagem
        self.message_width: float = 200.0
        self.message_height: float = 150.0
        
        # Posição da mensagem (centro da tela)
        self.message_x: float = window_width / 2 - self.message_width / 2
        self.message_y: float = window_height / 2 - self.message_height / 2
        
    def _render_impl(self) -> None:
        """
        Renderiza a tela de início com a mensagem "Get Ready"
        """
        # Verifica se a textura foi carregada
        if self.message_texture is None:
            return
            
        # Salva o estado da matriz atual
        glPushMatrix()
        
        # Não precisamos de um fundo semi-transparente aqui
        
        # Ativa o mapeamento de texturas 2D
        glEnable(GL_TEXTURE_2D)
        
        # Vincula a textura da mensagem
        glBindTexture(GL_TEXTURE_2D, self.message_texture)
        
        # Desenha a textura no centro da tela
        glBegin(GL_QUADS)
        
        glTexCoord2f(0, 0)
        glVertex2f(self.message_x, self.message_y)
        
        glTexCoord2f(1, 0)
        glVertex2f(self.message_x + self.message_width, self.message_y)
        
        glTexCoord2f(1, 1)
        glVertex2f(self.message_x + self.message_width, self.message_y + self.message_height)
        
        glTexCoord2f(0, 1)
        glVertex2f(self.message_x, self.message_y + self.message_height)
        
        glEnd()
        
        # Desativa o mapeamento de texturas 2D
        glDisable(GL_TEXTURE_2D)
        
        # Renderiza o texto de instrução "Pressione Espaço para Iniciar"
        self._render_start_text()
        
        # Restaura o estado da matriz
        glPopMatrix()
        
    def _render_start_text(self) -> None:
        """
        Renderiza o texto com instrução para iniciar o jogo
        Em um contexto real, usaríamos uma biblioteca de texto como FTGL ou FreeType,
        mas para simplificar, vamos apenas mostrar um texto simples
        """
        # Salva o estado da matriz atual
        glPushMatrix()
        
        # Reseta a matriz
        glLoadIdentity()
        
        # Configura a cor do texto (branco)
        glColor3f(1.0, 1.0, 1.0)
        
        # Desenhar linhas para formar as letras seria muito complexo aqui
        # Em um contexto real, usaríamos uma biblioteca de texto
        
        # Restaura a cor para branco
        glColor3f(1.0, 1.0, 1.0)
        
        # Restaura o estado da matriz
        glPopMatrix()

class GameOverOverlay(Overlay):
    """
    Tela de fim de jogo "Game Over" que é exibida quando o jogador perde
    Corresponde ao GameOverScreen no projeto Flutter
    """
    
    def __init__(self, texture_manager: TextureManager, window_width: float, window_height: float):
        """
        Inicializa a tela de fim de jogo
        
        Args:
            texture_manager: Gerenciador de texturas
            window_width: Largura da janela
            window_height: Altura da janela
        """
        super().__init__(texture_manager, window_width, window_height)
        
        # Carrega a textura "Game Over"
        self.game_over_texture: typing.Optional[int] = texture_manager.load_texture(GAME_OVER, "game_over")
        
        # Dimensões da textura "Game Over"
        self.game_over_width: float = 200.0
        self.game_over_height: float = 100.0
        
        # Posição do texto "Game Over" (centro da tela)
        self.game_over_x: float = window_width / 2 - self.game_over_width / 2
        self.game_over_y: float = window_height / 2 - self.game_over_height / 2 + 50
        
        # Botão de restart
        self.restart_button_width: float = 120.0
        self.restart_button_height: float = 40.0
        self.restart_button_x: float = window_width / 2 - self.restart_button_width / 2
        self.restart_button_y: float = self.game_over_y - self.restart_button_height - 20  # 20 pixels abaixo do game over
        
        # Cor do botão (laranja, como no Flutter)
        self.button_color = (1.0, 0.65, 0.0, 1.0)  # RGBA: laranja
        
        # Pontuação atual (será atualizada quando o overlay for mostrado)
        self.score: int = 0
        
    def show_with_score(self, score: int) -> None:
        """
        Mostra o overlay com a pontuação final
        
        Args:
            score: Pontuação final do jogador
        """
        self.score = score
        self.show()
        
    def is_restart_button_clicked(self, x: float, y: float) -> bool:
        """
        Verifica se o botão de restart foi clicado
        
        Args:
            x: Coordenada x do clique
            y: Coordenada y do clique
            
        Returns:
            bool: True se o clique foi dentro do botão, False caso contrário
        """
        # Converter y para sistema de coordenadas OpenGL (invertido em relação ao mouse)
        y = self.window_height - y
        
        return (self.is_visible and 
                x >= self.restart_button_x and 
                x <= self.restart_button_x + self.restart_button_width and
                y >= self.restart_button_y and 
                y <= self.restart_button_y + self.restart_button_height)
        
    def _render_impl(self) -> None:
        """
        Renderiza a tela de fim de jogo com a mensagem "Game Over" e a pontuação
        """
        # Verifica se a textura foi carregada
        if self.game_over_texture is None:
            return
            
        # Renderiza um fundo semi-transparente
        self._render_semitransparent_background()
            
        # Salva o estado da matriz atual
        glPushMatrix()
        
        # Ativa o mapeamento de texturas 2D
        glEnable(GL_TEXTURE_2D)
        
        # Vincula a textura "Game Over"
        glBindTexture(GL_TEXTURE_2D, self.game_over_texture)
        
        # Desenha a textura
        glBegin(GL_QUADS)
        
        glTexCoord2f(0, 0)
        glVertex2f(self.game_over_x, self.game_over_y)
        
        glTexCoord2f(1, 0)
        glVertex2f(self.game_over_x + self.game_over_width, self.game_over_y)
        
        glTexCoord2f(1, 1)
        glVertex2f(self.game_over_x + self.game_over_width, self.game_over_y + self.game_over_height)
        
        glTexCoord2f(0, 1)
        glVertex2f(self.game_over_x, self.game_over_y + self.game_over_height)
        
        glEnd()
        
        # Desativa o mapeamento de texturas 2D
        glDisable(GL_TEXTURE_2D)
        
        # Restaura o estado da matriz
        glPopMatrix()
        
        # Renderiza o botão de restart
        self._render_restart_button()
        
        # Renderiza o texto "Score: X"
        self._render_score_text()
        
    def _render_restart_button(self) -> None:
        """
        Renderiza o botão de restart
        """
        # Salva o estado da matriz atual
        glPushMatrix()
        
        # Reseta a matriz
        glLoadIdentity()
        
        # Configura a cor do botão (laranja)
        glColor4f(*self.button_color)
        
        # Desenha o botão como um retângulo
        glBegin(GL_QUADS)
        glVertex2f(self.restart_button_x, self.restart_button_y)
        glVertex2f(self.restart_button_x + self.restart_button_width, self.restart_button_y)
        glVertex2f(self.restart_button_x + self.restart_button_width, self.restart_button_y + self.restart_button_height)
        glVertex2f(self.restart_button_x, self.restart_button_y + self.restart_button_height)
        glEnd()
        
        # Restaura a cor para branco
        glColor4f(1.0, 1.0, 1.0, 1.0)
        
        # Restaura o estado da matriz
        glPopMatrix()
        
        # Texto "Restart" dentro do botão
        self._render_restart_text()
        
    def _render_restart_text(self) -> None:
        """
        Renderiza o texto "RESTART" dentro do botão
        """
        # Salva o estado da matriz atual
        glPushMatrix()
        
        # Reseta a matriz
        glLoadIdentity()
        
        # Configura a cor do texto (branco)
        glColor3f(1.0, 1.0, 1.0)
        
        # Vamos desenhar o texto "RESTART" com linhas simples
        # Posição central do texto
        text_x = self.restart_button_x + self.restart_button_width / 2
        text_y = self.restart_button_y + self.restart_button_height / 2
        
        # Tamanho das letras - aumentado para letras mais grossas
        letter_height = 16.0
        letter_width = 10.0
        spacing = 3.0
        thickness = 1.5  # Espessura das linhas
        
        # Ajustar a posição inicial para centralizar o texto "RESTART" (7 letras)
        start_x = text_x - ((letter_width * 7 + spacing * 6) / 2)
        start_y = text_y - letter_height / 2
        
        # Define a espessura das linhas (funciona apenas em algumas implementações OpenGL)
        glLineWidth(thickness)
        
        # Desenhar cada letra do texto "RESTART"
        current_x = start_x
        
        # R
        self._draw_letter_r(current_x, start_y, letter_width, letter_height)
        current_x += letter_width + spacing
        
        # E
        self._draw_letter_e(current_x, start_y, letter_width, letter_height)
        current_x += letter_width + spacing
        
        # S
        self._draw_letter_s(current_x, start_y, letter_width, letter_height)
        current_x += letter_width + spacing
        
        # T
        self._draw_letter_t(current_x, start_y, letter_width, letter_height)
        current_x += letter_width + spacing
        
        # A
        self._draw_letter_a(current_x, start_y, letter_width, letter_height)
        current_x += letter_width + spacing
        
        # R
        self._draw_letter_r(current_x, start_y, letter_width, letter_height)
        current_x += letter_width + spacing
        
        # T
        self._draw_letter_t(current_x, start_y, letter_width, letter_height)
        
        # Resetar a espessura da linha
        glLineWidth(1.0)
        
        # Restaura a cor para branco
        glColor3f(1.0, 1.0, 1.0)
        
        # Restaura o estado da matriz
        glPopMatrix()
    
    def _draw_letter_r(self, x: float, y: float, width: float, height: float) -> None:
        """Desenha a letra R"""
        # Versão mais grossa da letra R
        glBegin(GL_LINES)
        # Linha vertical esquerda (principal)
        glVertex2f(x, y)
        glVertex2f(x, y + height)
        
        # Linha vertical esquerda (duplicada para espessura)
        glVertex2f(x + 1, y)
        glVertex2f(x + 1, y + height)
        
        # Linha horizontal superior
        glVertex2f(x, y + height)
        glVertex2f(x + width, y + height)
        
        # Linha horizontal superior (duplicada para espessura)
        glVertex2f(x, y + height - 1)
        glVertex2f(x + width, y + height - 1)
        
        # Linha vertical direita superior
        glVertex2f(x + width, y + height)
        glVertex2f(x + width, y + height / 2)
        
        # Linha vertical direita superior (duplicada para espessura)
        glVertex2f(x + width - 1, y + height)
        glVertex2f(x + width - 1, y + height / 2)
        
        # Linha horizontal meio
        glVertex2f(x, y + height / 2)
        glVertex2f(x + width, y + height / 2)
        
        # Linha horizontal meio (duplicada para espessura)
        glVertex2f(x, y + height / 2 + 1)
        glVertex2f(x + width, y + height / 2 + 1)
        
        # Diagonal inferior
        glVertex2f(x, y + height / 2)
        glVertex2f(x + width, y)
        
        # Diagonal inferior (duplicada para espessura)
        glVertex2f(x, y + height / 2 - 1)
        glVertex2f(x + width - 1, y + 1)
        glEnd()
    
    def _draw_letter_e(self, x: float, y: float, width: float, height: float) -> None:
        """Desenha a letra E"""
        glBegin(GL_LINES)
        # Linha vertical esquerda
        glVertex2f(x, y)
        glVertex2f(x, y + height)
        
        # Linha vertical esquerda (duplicada para espessura)
        glVertex2f(x + 1, y)
        glVertex2f(x + 1, y + height)
        
        # Linha horizontal superior
        glVertex2f(x, y + height)
        glVertex2f(x + width, y + height)
        
        # Linha horizontal superior (duplicada para espessura)
        glVertex2f(x, y + height - 1)
        glVertex2f(x + width, y + height - 1)
        
        # Linha horizontal meio
        glVertex2f(x, y + height / 2)
        glVertex2f(x + width * 0.8, y + height / 2)
        
        # Linha horizontal meio (duplicada para espessura)
        glVertex2f(x, y + height / 2 + 1)
        glVertex2f(x + width * 0.8, y + height / 2 + 1)
        
        # Linha horizontal inferior
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        
        # Linha horizontal inferior (duplicada para espessura)
        glVertex2f(x, y + 1)
        glVertex2f(x + width, y + 1)
        glEnd()
        
    def _draw_letter_s(self, x: float, y: float, width: float, height: float) -> None:
        """Desenha a letra S"""
        glBegin(GL_LINES)
        # Linha horizontal superior
        glVertex2f(x, y + height)
        glVertex2f(x + width, y + height)
        
        # Linha horizontal superior (duplicada para espessura)
        glVertex2f(x, y + height - 1)
        glVertex2f(x + width, y + height - 1)
        
        # Linha vertical esquerda superior
        glVertex2f(x, y + height)
        glVertex2f(x, y + height / 2)
        
        # Linha vertical esquerda superior (duplicada para espessura)
        glVertex2f(x + 1, y + height)
        glVertex2f(x + 1, y + height / 2)
        
        # Linha horizontal meio
        glVertex2f(x, y + height / 2)
        glVertex2f(x + width, y + height / 2)
        
        # Linha horizontal meio (duplicada para espessura)
        glVertex2f(x, y + height / 2 + 1)
        glVertex2f(x + width, y + height / 2 + 1)
        
        # Linha vertical direita inferior
        glVertex2f(x + width, y + height / 2)
        glVertex2f(x + width, y)
        
        # Linha vertical direita inferior (duplicada para espessura)
        glVertex2f(x + width - 1, y + height / 2)
        glVertex2f(x + width - 1, y)
        
        # Linha horizontal inferior
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        
        # Linha horizontal inferior (duplicada para espessura)
        glVertex2f(x, y + 1)
        glVertex2f(x + width, y + 1)
        glEnd()
        
    def _draw_letter_t(self, x: float, y: float, width: float, height: float) -> None:
        """Desenha a letra T"""
        glBegin(GL_LINES)
        # Linha horizontal superior
        glVertex2f(x, y + height)
        glVertex2f(x + width, y + height)
        
        # Linha horizontal superior (duplicada para espessura)
        glVertex2f(x, y + height - 1)
        glVertex2f(x + width, y + height - 1)
        
        # Linha vertical central
        glVertex2f(x + width / 2, y + height)
        glVertex2f(x + width / 2, y)
        
        # Linha vertical central (duplicada para espessura)
        glVertex2f(x + width / 2 + 1, y + height)
        glVertex2f(x + width / 2 + 1, y)
        glEnd()
        
    def _draw_letter_a(self, x: float, y: float, width: float, height: float) -> None:
        """Desenha a letra A"""
        glBegin(GL_LINES)
        # Linha diagonal esquerda
        glVertex2f(x, y)
        glVertex2f(x + width / 2, y + height)
        
        # Linha diagonal esquerda (duplicada para espessura)
        glVertex2f(x + 1, y)
        glVertex2f(x + width / 2 + 1, y + height)
        
        # Linha diagonal direita
        glVertex2f(x + width / 2, y + height)
        glVertex2f(x + width, y)
        
        # Linha diagonal direita (duplicada para espessura)
        glVertex2f(x + width / 2 - 1, y + height)
        glVertex2f(x + width - 1, y)
        
        # Linha horizontal meio
        glVertex2f(x + width * 0.25, y + height / 2)
        glVertex2f(x + width * 0.75, y + height / 2)
        
        # Linha horizontal meio (duplicada para espessura)
        glVertex2f(x + width * 0.25, y + height / 2 + 1)
        glVertex2f(x + width * 0.75, y + height / 2 + 1)
        glEnd()
        
    def _render_score_text(self) -> None:
        """
        Renderiza o texto com a pontuação final
        """
        # Em um caso real, usaríamos uma biblioteca de texto
        # para renderizar algo como "Score: {self.score}"
        # posicionado acima do botão de restart
        pass 

class HeartDisplay(Overlay):
    """
    Overlay para exibir os corações representando as vidas do jogador
    no canto superior esquerdo da tela
    """
    
    def __init__(self, texture_manager: TextureManager, window_width: float, window_height: float, max_lives: int = MAX_LIVES):
        """
        Inicializa o display de corações
        
        Args:
            texture_manager: Gerenciador de texturas
            window_width: Largura da janela
            window_height: Altura da janela
            max_lives: Número máximo de vidas
        """
        super().__init__(texture_manager, window_width, window_height)
        
        # Sempre visível durante o jogo
        self.is_visible = True
        
        # Carrega a textura do coração
        self.heart_texture = texture_manager.load_texture(HEART, "heart")
        
        # Dimensões de cada coração (usando valores do config)
        self.heart_width = HEART_WIDTH
        self.heart_height = HEART_HEIGHT
        
        # Espaçamento entre corações (usando valores do config)
        self.heart_spacing = HEART_SPACING
        
        # Posição inicial (canto superior esquerdo com pequena margem)
        self.initial_x = 10.0
        self.initial_y = window_height - self.heart_height - 10.0
        
        # Número atual e máximo de vidas
        self.current_lives = max_lives
        self.max_lives = max_lives
    
    def update_lives(self, lives: int) -> None:
        """
        Atualiza o número de vidas a ser exibido
        
        Args:
            lives: Número atual de vidas
        """
        self.current_lives = max(0, min(lives, self.max_lives))
    
    def _render_impl(self) -> None:
        """
        Renderiza os corações na tela
        """
        # Verifica se a textura foi carregada
        if self.heart_texture is None:
            return
            
        # Salva o estado da matriz atual
        glPushMatrix()
        
        # Ativa o mapeamento de texturas 2D
        glEnable(GL_TEXTURE_2D)
        
        # Vincula a textura do coração
        glBindTexture(GL_TEXTURE_2D, self.heart_texture)
        
        # Desenha cada coração
        for i in range(self.current_lives):
            x = self.initial_x + (self.heart_width + self.heart_spacing) * i
            y = self.initial_y
            
            glBegin(GL_QUADS)
            
            glTexCoord2f(0, 0)
            glVertex2f(x, y)
            
            glTexCoord2f(1, 0)
            glVertex2f(x + self.heart_width, y)
            
            glTexCoord2f(1, 1)
            glVertex2f(x + self.heart_width, y + self.heart_height)
            
            glTexCoord2f(0, 1)
            glVertex2f(x, y + self.heart_height)
            
            glEnd()
        
        # Desativa o mapeamento de texturas 2D
        glDisable(GL_TEXTURE_2D)
        
        # Restaura o estado da matriz
        glPopMatrix() 

class ScoreDisplay(Overlay):
    """
    Overlay para exibir a pontuação atual na parte superior central da tela
    """
    
    def __init__(self, texture_manager: TextureManager, window_width: float, window_height: float):
        """
        Inicializa o display de pontuação
        
        Args:
            texture_manager: Gerenciador de texturas
            window_width: Largura da janela
            window_height: Altura da janela
        """
        super().__init__(texture_manager, window_width, window_height)
        
        # Sempre visível durante o jogo
        self.is_visible = True
        
        # Lista de constantes de números
        self.number_textures = [
            texture_manager.load_texture(NUMBER_0, "number_0"),
            texture_manager.load_texture(NUMBER_1, "number_1"),
            texture_manager.load_texture(NUMBER_2, "number_2"),
            texture_manager.load_texture(NUMBER_3, "number_3"),
            texture_manager.load_texture(NUMBER_4, "number_4"),
            texture_manager.load_texture(NUMBER_5, "number_5"),
            texture_manager.load_texture(NUMBER_6, "number_6"),
            texture_manager.load_texture(NUMBER_7, "number_7"),
            texture_manager.load_texture(NUMBER_8, "number_8"),
            texture_manager.load_texture(NUMBER_9, "number_9")
        ]
        
        # Dimensões de cada número (usando valores do config)
        self.number_width = SCORE_NUMBER_WIDTH
        self.number_height = SCORE_NUMBER_HEIGHT
        
        # Espaçamento entre números (usando valores do config)
        self.number_spacing = SCORE_NUMBER_SPACING
        
        # Posição Y (topo da tela com margem)
        self.position_y = window_height - self.number_height - 20.0  # Margem um pouco maior
        
        # Pontuação atual
        self.score = 0
    
    def update_score(self, score: int) -> None:
        """
        Atualiza a pontuação atual
        
        Args:
            score: Nova pontuação
        """
        self.score = max(0, score)
    
    def _render_impl(self) -> None:
        """
        Renderiza a pontuação atual na tela
        """
        # Converte a pontuação para string
        score_str = str(self.score)
        
        # Calcula a largura total para centralizar
        total_width = len(score_str) * self.number_width + (len(score_str) - 1) * self.number_spacing
        
        # Posição X inicial (centralizada)
        start_x = (self.window_width - total_width) / 2
        
        # Salva o estado da matriz atual
        glPushMatrix()
        
        # Ativa o mapeamento de texturas 2D
        glEnable(GL_TEXTURE_2D)
        
        # Desenha cada dígito da pontuação
        for i, digit in enumerate(score_str):
            # Posição X deste dígito
            x = start_x + i * (self.number_width + self.number_spacing)
            
            # Obtém o índice da textura (convertendo o caractere para inteiro)
            digit_index = int(digit)
            
            # Verifica se a textura para este dígito foi carregada corretamente
            if 0 <= digit_index < 10 and self.number_textures[digit_index] is not None:
                # Vincula a textura para este dígito
                glBindTexture(GL_TEXTURE_2D, self.number_textures[digit_index])
                
                # Desenha o dígito
                glBegin(GL_QUADS)
                
                glTexCoord2f(0, 0)
                glVertex2f(x, self.position_y)
                
                glTexCoord2f(1, 0)
                glVertex2f(x + self.number_width, self.position_y)
                
                glTexCoord2f(1, 1)
                glVertex2f(x + self.number_width, self.position_y + self.number_height)
                
                glTexCoord2f(0, 1)
                glVertex2f(x, self.position_y + self.number_height)
                
                glEnd()
        
        # Desativa o mapeamento de texturas 2D
        glDisable(GL_TEXTURE_2D)
        
        # Restaura o estado da matriz
        glPopMatrix() 