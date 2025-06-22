from jogo.config import *
from telas.botao import Botao 

class TelaPausada():
    def __init__(self, tela):
        self.tela = tela
        self.overlay = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
        self.overlay.fill((30, 30, 30, 10))
        
        # Texto na tela de game over 
        self.texto_pausado = Botao("white", 50,"PAUSADO", largura_tela / 2 ,altura_tela / 2)
    
    def draw(self):
        self.tela.blit(self.overlay, (0, 0))
        # Obtém o texto renderizado e seu rect através da propriedade
        texto, rect = self.texto_pausado.texto
        self.tela.blit(texto, rect)