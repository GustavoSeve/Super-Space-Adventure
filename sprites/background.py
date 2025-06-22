from jogo.config import *

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(join('imagens', 'background.png')).convert()
        self.rect = self.image.get_frect(topleft = (0, 0))       