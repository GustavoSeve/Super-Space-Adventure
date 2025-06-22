from jogo.config import *

class Botao:
    def __init__(self, cor_fonte, tamanho_fonte, texto_fonte, local_x_fonte, local_y_fonte):
        self.cor_fonte = cor_fonte
        self.tamanho_fonte = tamanho_fonte
        self.texto_fonte = texto_fonte
        self.local_x_fonte = local_x_fonte
        self.local_y_fonte = local_y_fonte
        self.textos = pygame.font.Font("fontes/04B_03__.ttf", tamanho_fonte)

    @property
    def texto(self):
        return [self.textos.render(self.texto_fonte, True, self.cor_fonte), 
                self.textos.render(self.texto_fonte, True, self.cor_fonte).get_frect(center = (self.local_x_fonte, self.local_y_fonte))]