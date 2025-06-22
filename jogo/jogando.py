from jogo.config import *
from sprites.player import Player
from sprites.meteoro import Meteoro
from sprites.laser import Laser 
from sprites.background import Background

from telas.pause import TelaPausada
from telas.menu import Menu
from telas.game_over import GameOver

class Jogando():
    def __init__(self):
        # pygame setup
        pygame.init()
        pygame.display.set_caption("Super Space Adventure")
        self.screen = pygame.display.set_mode((largura_tela, altura_tela))
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        # Inicializa os grupos e sprites
        self.reset_game()

        # Telas
        self.tela_pausada = TelaPausada(self.screen)
        self.menu_inicial = Menu(True, self.screen, self)

        # Evento de tempo 
        self.plotar_meteoro = pygame.event.custom_type()
        pygame.time.set_timer(self.plotar_meteoro, 600)

        self.plotar_laser = pygame.event.custom_type()
        pygame.time.set_timer(self.plotar_laser, 1750)

    def reset_game(self):
        """Reseta todos os elementos do jogo"""
        # Limpa todos os grupos de sprites
        self.todas_sprites = pygame.sprite.Group()
        self.meteoro_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()

        # Recria os sprites básicos
        background = Background()                                                       
        self.todas_sprites.add(background)

        self.player = Player()
        self.todas_sprites.add(self.player)

        # Reset do tempo
        self.tempo_inicio = 0
        self.tempo_pausado = 0
        self.pausando_agora = 0
        self.tempo_total = 0
        self.jogo_ativo = False
        self.paused = False

        # Reset do contador de acerto do meteoro 
        self.contador_meteoro = 0

    def cronometro(self):
        if self.jogo_ativo and not self.paused:
            tempo_atual = pygame.time.get_ticks()
            self.tempo_total = (tempo_atual - self.tempo_inicio - self.tempo_pausado) // 1000

        minutos = self.tempo_total // 60
        segundos = self.tempo_total % 60
        texto = pygame.font.Font("fontes/04B_03__.ttf", 40).render(f" {minutos:02}:{segundos:02}", True, "white")
        texto_rect = texto.get_rect(center=((largura_tela / 2) - 6, 60))
        self.screen.blit(texto, texto_rect)

    def pontos(self):

        pontuacao_atual = self.contador_meteoro

        # Desenhar pontuação atual
        fonte = pygame.font.Font("fontes/04B_03__.ttf", 40)
        texto_pontuacao = fonte.render(f"{pontuacao_atual}", True, "white")
        self.screen.blit(texto_pontuacao, texto_pontuacao.get_rect(center=((largura_tela / 2), 650)))

        # Desenhar recorde
        if self.contador_meteoro > self.recorde_atual:
            recorde = self.contador_meteoro
            texto_recorde = fonte.render(f"Recorde : {recorde}", True, "yellow")
        else:
            recorde = self.recorde_atual
            texto_recorde = fonte.render(f"Recorde : {recorde}", True, "white")
        self.screen.blit(texto_recorde, texto_recorde.get_rect(topleft=(30, 30)))

    def pontuacao(self):
        dados = {
            "pontuacaoMaxima": {"pontos": 0, "timestamp": 0},
            "historico": []
        }

        # Ler arquivo JSON
        try:
            with open("pontuacao.json", "r") as arquivo:
                dados = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Se não existe, usamos os dados padrão

        pontuacao_atual = self.contador_meteoro
        timestamp_atual = int(time.time())  # Timestamp atual (segundos desde 1970)

        # Verificar e atualizar recorde
        if pontuacao_atual > dados["pontuacaoMaxima"]["pontos"]:
            dados["pontuacaoMaxima"] = {
                "pontos": pontuacao_atual,
                "timestamp": timestamp_atual
            }
            self.recorde_atual = pontuacao_atual  
        # Adiciona ao histórico
        dados["historico"].append({
            "pontos": pontuacao_atual,
            "timestamp": timestamp_atual
        })

        # Salva o JSON atualizado
        with open("pontuacao.json", "w") as arquivo:
            json.dump(dados, arquivo, indent=4)
            
    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.paused = not self.paused

                    if self.paused:
                        self.pausando_agora = pygame.time.get_ticks()
                    else:
                        self.tempo_pausado += pygame.time.get_ticks() - self.pausando_agora

            if self.jogo_ativo and not self.paused:
                if event.type == self.plotar_meteoro:
                    posicao_x = randint(300, 900)
                    posicao_y = -35
                    meteoro = Meteoro(posicao_x, posicao_y)
                    self.todas_sprites.add(meteoro)
                    self.meteoro_sprites.add(meteoro)
                if event.type == self.plotar_laser:
                    pos = self.player.rect.midbottom
                    laser = Laser(pos)
                    self.todas_sprites.add(laser)
                    self.laser_sprites.add(laser)

    def colisoes(self):
        # Dentro do método colisoes da classe Jogo
        if pygame.sprite.spritecollide(self.player, self.meteoro_sprites, False, pygame.sprite.collide_mask):
            self.pontuacao()  # Salva a pontuação
            game_over = GameOver(self.screen, self.contador_meteoro, self.recorde_atual)
            game_over.draw()
            pygame.display.flip()
            
            # Espera o jogador pressionar TAB
            esperando = True
            while esperando:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                        esperando = False
            
            self.reset_game()
            self.menu_inicial.rodando = True
            
            # Loop do menu
            while self.menu_inicial.rodando and self.running:
                self.menu_inicial.run()
                self.clock.tick(60)
                
            # Se saiu do menu e o jogo ainda está rodando, inicia um novo jogo
            if self.running:
                self.jogo_ativo = True
                self.tempo_inicio = pygame.time.get_ticks()

        for laser in self.laser_sprites:
            if pygame.sprite.spritecollide(laser, self.meteoro_sprites, True, pygame.sprite.collide_mask):
                self.contador_meteoro += 1
                laser.kill()

    def coloca_imagens(self):
        dt = self.clock.tick() / 1000
        if self.jogo_ativo and not self.paused:
            self.todas_sprites.update(dt, self.tempo_total)
        self.todas_sprites.draw(self.screen)
        if self.jogo_ativo:
            self.cronometro()
            self.pontos()

    def run(self):
        # Mostra menu inicial
        while self.menu_inicial.rodando and self.running:
            self.menu_inicial.run()
            self.clock.tick(60)
            
        # Inicia o jogo se ainda estiver rodando
        if self.running:
            self.jogo_ativo = True
            self.tempo_inicio = pygame.time.get_ticks()
            # Ler arquivo JSON
            try:
                with open("pontuacao.json", "r") as arquivo:
                    dados = json.load(arquivo)
                    self.recorde_atual = dados["pontuacaoMaxima"]["pontos"]
            except (FileNotFoundError, json.JSONDecodeError):
                self.recorde_atual = 0
            
            # Loop principal do jogo
            while self.running:
                self.eventos()
                self.colisoes()
                self.coloca_imagens()
                
                
                if self.paused:
                    self.tela_pausada.draw()
                    
                pygame.display.flip()

        pygame.quit()
