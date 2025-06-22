from jogo.config import *
from sprites.objetos import ObjetosTela

class Player(pygame.sprite.Sprite, ObjetosTela):
    def __init__(self):
        super().__init__()
        # Variáveis básicas
        self.image = pygame.image.load(join('imagens', 'nave.png')).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 1.5)   
        self.rect = self.image.get_frect()
        self.rect.center = (largura_tela / 2, altura_tela - 120)

        self.limite_tela = pygame.FRect(0, 0, largura_tela - 1, altura_tela - 1)
        self.limite_tela.center = 640, 360

        # Variáveis de movimentação do player
        self.velocidade = 275
        self.direcao = pygame.Vector2()
        self.direcao.x = 0
        self.direcao.y = 0  
                    
    def __input(self):
        teclas = pygame.key.get_pressed()
        self.direcao.x = int(teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) - int(teclas[pygame.K_LEFT] or teclas[pygame.K_a])                                                      
        self.direcao.y = int(teclas[pygame.K_DOWN] or teclas[pygame.K_s]) - int(teclas[pygame.K_UP] or teclas[pygame.K_w])
        if (self.direcao.x != 0 and self.direcao.y != 0) and int((self.limite_tela.contains(self.rect))):
            self.direcao = self.direcao.normalize()
    
    def __mover(self, dt, tempo_total):
        # Mover
        self.rect.center += self.direcao * self.velocidade * dt 

    def __LimiteTela(self):
        # Limitar nos cantos da tela
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= largura_tela:
            self.rect.right = largura_tela
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= altura_tela:
            self.rect.bottom = altura_tela
        
    def update(self, dt, tempo_total):
        self.__input()
        self.__LimiteTela()
        self.__mover(dt, tempo_total)