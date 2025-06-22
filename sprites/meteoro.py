from jogo.config import *
from sprites.objetos import ObjetosTela

class Meteoro(pygame.sprite.Sprite, ObjetosTela):
    def __init__(self, posicao_x, posicao_y):
        super().__init__()
        # Variáveis image e rect 
        self.image = self.__escolhe_meteoro()
        self.image = pygame.transform.scale_by(self.image, uniform(2.0, 2.5))  
        self.rect  = self.image.get_frect()
        self.rect.center = (posicao_x, posicao_y)

        # Variáveis de movimentação do meteoro
        self.velocidade = randint(40, 50)
        self.direcao = pygame.Vector2()
        self.direcao.x = randint(-5, 5)
        self.direcao.y = 5

        # Variáveis para rotação do meteoro
        self.incremento = 0
        self.imagem_recebida = self.image 

        # Variáveis para conferir se meteoro saiu da tela
        self.limite_tela = pygame.FRect(0, 0, largura_tela + 400, altura_tela + 400)
        self.limite_tela.center = 640, 360
        

    def __escolhe_meteoro(self):
        imagem_0 = pygame.image.load(join('imagens', 'meteoro0.png')).convert_alpha()
        imagem_1 = pygame.image.load(join('imagens', 'meteoro1.png')).convert_alpha()
        total_imagens = [imagem_1, imagem_1, imagem_1, imagem_0]
        indice = randint(0,3)
        return total_imagens[indice]
        
    def __girar(self, dt):
        self.image = pygame.transform.rotozoom(self.imagem_recebida, self.__incrementar(dt), 1)
        self.rect = self.image.get_frect(center = self.rect.center)
        
    def __incrementar(self, dt):
        self.incremento += (4 * dt * (self.velocidade))
        return self.incremento 
    
    def __LimiteTela(self):
        if (not(self.limite_tela.contains(self.rect))):
            self.kill()
            
    def __mover(self, dt, tempo_total):
        velocidade_atual = self.velocidade + (tempo_total * 1.5)
        movimentar = (self.direcao * velocidade_atual * dt)
        self.rect.center += movimentar

    def update(self,dt, tempo_total):
        self.__girar(dt)
        self.__mover(dt, tempo_total)
        self.__LimiteTela()