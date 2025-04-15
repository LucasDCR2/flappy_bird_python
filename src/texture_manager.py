"""
Gerenciador de texturas para o jogo Flappy Bird
Responsável por carregar imagens e convertê-las em texturas OpenGL
"""

from OpenGL.GL import * # type: ignore
from OpenGL.GL import glGenTextures, glBindTexture, glTexParameteri, glTexImage2D, glDeleteTextures # type: ignore
from OpenGL.GL import GL_TEXTURE_2D, GL_REPEAT, GL_LINEAR, GL_RGBA, GL_UNSIGNED_BYTE # type: ignore
from OpenGL.GL import GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER # type: ignore
from PIL import Image # type: ignore
import numpy as np # type: ignore
import typing # type: ignore
import os # type: ignore

class TextureManager:
    """
    Gerenciador de texturas para o jogo Flappy Bird.
    Carrega e gerencia texturas para uso com OpenGL.
    """
    
    def __init__(self):
        """Inicializa o gerenciador de texturas."""
        self.textures: dict[str, int] = {}  # Dicionário para armazenar texturas pelo nome

    def load_texture(self, path: str, name: typing.Optional[str] = None) -> typing.Optional[int]:
        """
        Carrega uma imagem e a converte em uma textura OpenGL
        
        Args:
            path: Caminho do arquivo de imagem
            name: Nome para referenciar a textura (opcional, usa o path se não fornecido)
            
        Returns:
            ID da textura OpenGL ou None se houver erro
        """
        if name is None:
            name = path
            
        # Verifica se a textura já está carregada
        if name in self.textures:
            return self.textures[name]
            
        try:
            # Verifica se o arquivo existe
            if not os.path.exists(path):
                print(f"Erro: Arquivo '{path}' não encontrado.")
                return None
                
            # Carrega a imagem com PIL
            image = Image.open(path)
            # No OpenGL, textura começa na parte inferior esquerda, mas no PIL na parte superior esquerda
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            # Converte para RGBA para garantir canal alpha
            img_data = np.array(image.convert("RGBA"), dtype=np.uint8)
            
            # Gera um ID de textura OpenGL
            texture_id = glGenTextures(1)
            
            # Vincula a textura
            glBindTexture(GL_TEXTURE_2D, texture_id)
            
            # Configura parâmetros da textura
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            # Carrega os dados da imagem na textura OpenGL
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGBA,
                image.width,
                image.height,
                0,
                GL_RGBA,
                GL_UNSIGNED_BYTE,
                img_data
            )
            
            # Armazena a textura no dicionário
            self.textures[name] = texture_id
            
            print(f"Textura '{name}' carregada com sucesso. ID: {texture_id}")
            return texture_id
            
        except Exception as e:
            print(f"Erro ao carregar textura '{path}': {e}")
            return None
            
    def get_texture(self, name: str) -> typing.Optional[int]:
        """
        Obtém o ID de uma textura carregada pelo nome
        
        Args:
            name: Nome da textura a ser recuperada
            
        Returns:
            ID da textura ou None se não encontrada
        """
        if name in self.textures:
            return self.textures[name]
        print(f"Aviso: Textura '{name}' não encontrada")
        return None
        
    def cleanup(self) -> None:
        """
        Libera todas as texturas da memória
        """
        for texture_id in self.textures.values():
            glDeleteTextures(1, [texture_id])
        self.textures.clear()
        print("Todas as texturas foram liberadas") 