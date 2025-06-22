from jogo.config import *
from sprites.objetos import ObjetosTela

class Laser(pygame.sprite.Sprite, ObjetosTela):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(join('imagens', 'laserr.png')).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.3)   
        self.rect = self.image.get_frect()
        self.rect.midbottom = pos

        # Variáveis de movimentação do laser
        self.velocidade = 350
        self.direcao = pygame.Vector2()
        self.direcao.x = 0
        self.direcao.y = -1

    def __mover(self, dt, tempo_total):
        self.rect.center += self.direcao * self.velocidade * dt 

    def __LimiteTela(self):
        if self.rect.bottom <= 0:
            self.kill()

    def update(self, dt, tempo_total):
        self.__LimiteTela()
        self.__mover(dt, tempo_total)