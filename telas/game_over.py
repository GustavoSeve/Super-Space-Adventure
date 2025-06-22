from jogo.config import *
from telas.botao import Botao 

class GameOver():
    def __init__(self, tela, pontuacao, recorde):
        self.tela = tela
        self.overlay = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))  # Fundo mais escuro que o pause
        
        # Textos da tela de game over
        self.titulo = Botao("blue", 70, "GAME OVER", largura_tela/2, altura_tela/2 - 100)
        self.pontuacao = Botao("white", 30, f"Pontos: {pontuacao}", largura_tela/2, altura_tela/2)
        self.recorde = Botao("yellow", 30, f"Recorde: {recorde}", largura_tela/2, altura_tela/2 + 50)
        self.instrucao = Botao("white", 20, "Pressione TAB para voltar ao menu", largura_tela/2, altura_tela/2 + 150)
    
    def draw(self):
        self.tela.blit(self.overlay, (0, 0))
        
        # Renderiza todos os textos como botões (mesmo que não sejam clicáveis)
        for botao in [self.titulo, self.pontuacao, self.recorde, self.instrucao]:
            texto, rect = botao.texto
            self.tela.blit(texto, rect)