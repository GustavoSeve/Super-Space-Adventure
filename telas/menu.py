from jogo.config import *
from telas.botao import Botao

class Menu():
    def __init__(self, escolhendo, tela, jogo):
        self.rodando = escolhendo
        self.tela = tela
        self.jogo = jogo

        self.imagem_back = pygame.image.load(join('imagens', 'tela_python.png')).convert_alpha()
        self.retangulo_back = self.imagem_back.get_frect()

        self.botao_continue = Botao('white', 30, "CONTINUE", 230, 480)
        self.botao_exit = Botao('white', 30, "EXIT", 230, 530)   
        self.verifica = []

    def coloca_imagens(self):
        mouse = pygame.mouse.get_pos()

        botao_continue, botao_continue_retangulo = self.botao_continue.texto
        botao_exit, botao_exit_retangulo = self.botao_exit.texto

        self.tela.blit(self.imagem_back, self.retangulo_back)

        if (botao_continue_retangulo.collidepoint(mouse)):
            self.botao_continue.cor_fonte = 'gray'
        else:
            self.botao_continue.cor_fonte = 'white'

        if (botao_exit_retangulo.collidepoint(mouse)):
            self.botao_exit.cor_fonte = 'gray'
        else:
            self.botao_exit.cor_fonte = 'white'
            
        self.tela.blit(botao_continue, botao_continue_retangulo)
        self.tela.blit(botao_exit, botao_exit_retangulo)

        return botao_continue_retangulo, botao_exit_retangulo

    def eventos(self):
        mouse = pygame.mouse.get_pos()
        self.verifica = self.coloca_imagens()

        for event in pygame.event.get():
                if event.type == pygame.QUIT:     
                    pygame.quit()
                    sys.exit()                                 # pygame.QUIT event significa que apertou no X da janela 
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == (pygame.K_TAB):
                        self.rodando = False
                        break

                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if (event.button == 1) and (self.verifica[0].collidepoint(mouse)):     # event.button == 1 -> botão esquerdo mouse  
                        self.rodando = False
                        self.jogo.reset_game()
                        break

                    if (event.button == 1) and (self.verifica[1].collidepoint(mouse)):     # event.button == 1 -> botão esquerdo mouse  
                        pygame.quit()
                        sys.exit()
 
    def run(self):
        if self.rodando:
            self.eventos()
            pygame.display.flip()