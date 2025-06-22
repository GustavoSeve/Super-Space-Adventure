from jogo.config import *

class ObjetosTela(ABC):
    def __init__(self):
        self.image = None
        self.rect = None
        self.velocidade = None
        self.direcao = None

    @abstractmethod
    def update(self):
        pass

    