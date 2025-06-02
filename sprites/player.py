import pygame
from settings.settings import * # Importa todas as constantes

class Player(pygame.sprite.Sprite):
    """Classe para o jogador."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        """Reseta a posição e estado do jogador."""
        self.rect.x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        self.rect.y = GROUND_LEVEL - PLAYER_HEIGHT
        self.vel_y = 0
        self.on_ground = True
        self.health = MAX_PLAYER_HEALTH
        self.current_height_text = "Altura: 0"

    def update(self, static_obstacles_group, falling_obstacles_group): # falling_obstacles_group adicionado
        """Atualiza a posição do jogador."""
        dx = 0
        
        # Input do teclado para movimento horizontal
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -PLAYER_MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = PLAYER_MOVE_SPEED
        
        # Lógica de Pulo
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = -PLAYER_JUMP_STRENGTH
            self.on_ground = False # Jogador não está mais no chão (ou bloco) após pular

        # Aplicar gravidade se não estiver no chão firme
        # Se self.on_ground for True por estar em um bloco em queda, a vel_y será ajustada depois
        if not self.on_ground:
            self.vel_y += PLAYER_GRAVITY
        
        # Limitar velocidade máxima de queda
        if self.vel_y > 15: # Aumentei um pouco o limite para quedas mais longas
            self.vel_y = 15
        
        dy = self.vel_y

        # --- Colisão Horizontal ---
        # Primeiro, move horizontalmente e checa colisão com obstáculos estáticos e bordas
        original_x = self.rect.x
        self.rect.x += dx

        for obstacle in static_obstacles_group:
            if self.rect.colliderect(obstacle.rect):
                if dx > 0: # Movendo para a direita
                    self.rect.right = obstacle.rect.left
                elif dx < 0: # Movendo para a esquerda
                    self.rect.left = obstacle.rect.right
        
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        # --- Colisão Vertical ---
        # Tenta aplicar o movimento vertical e depois verifica colisões
        original_y = self.rect.y
        self.rect.y += dy

        current_frame_on_ground_flag = False # Flag para determinar se o jogador está no chão/bloco nesta frame
        ridden_block_this_frame = False

        # 1. Checar "carona" (riding) em blocos caindo
        # Se o jogador está caindo (vel_y >= 0) e seus pés estavam acima do topo do bloco
        # e agora colidem com o topo do bloco.
        if self.vel_y >= 0: # Só pode aterrissar se estiver caindo ou parado verticalmente
            for obs in falling_obstacles_group: # Checa contra blocos que ainda estão caindo
                if self.rect.colliderect(obs.rect):
                    # Condição de aterrissagem: pés do jogador estavam acima ou no nível do topo do bloco
                    # e agora o jogador está tocando o topo do bloco.
                    # A checagem de obs.rect.top + 1 garante que o jogador está ligeiramente acima ou no mesmo nível
                    # antes de ser considerado "em cima".
                    if (original_y + PLAYER_HEIGHT) <= (obs.rect.top + 2): # Aumentei a margem para 2 pixels
                        # Verifica se o centro horizontal do jogador está sobre o bloco para evitar "grudar" nas laterais
                        player_center_x = self.rect.centerx
                        # Permite que o jogador aterrisse se estiver um pouco para fora da borda do bloco
                        obstacle_tolerant_left_edge = obs.rect.left - (PLAYER_WIDTH / 4) 
                        obstacle_tolerant_right_edge = obs.rect.right + (PLAYER_WIDTH / 4)

                        if player_center_x > obstacle_tolerant_left_edge and player_center_x < obstacle_tolerant_right_edge:
                            self.rect.bottom = obs.rect.top
                            self.vel_y = obs.speed # Jogador agora cai com a mesma velocidade do bloco
                            current_frame_on_ground_flag = True
                            ridden_block_this_frame = True
                            break # Já está "surfando" em um bloco

        # 2. Se não estiver "surfando" num bloco em queda, checar colisão com obstáculos ESTÁTICOS
        if not ridden_block_this_frame:
            for obstacle in static_obstacles_group:
                if self.rect.colliderect(obstacle.rect):
                    if dy > 0: # Caindo sobre o obstáculo estático
                        # Verifica se o jogador estava acima do obstáculo antes do movimento
                        if original_y + PLAYER_HEIGHT <= obstacle.rect.top + 1 :
                            self.rect.bottom = obstacle.rect.top
                            self.vel_y = 0 # Para o movimento vertical
                            current_frame_on_ground_flag = True
                    elif dy < 0: # Pulando e batendo a cabeça no obstáculo estático
                        # Verifica se o jogador estava abaixo do obstáculo antes do movimento
                        if original_y >= obstacle.rect.bottom -1:
                            self.rect.top = obstacle.rect.bottom
                            self.vel_y = 0 # Para o movimento ascendente
                    if current_frame_on_ground_flag or dy < 0: # Se aterrisou ou bateu a cabeça
                        break 
        
        # 3. Colisão com o chão principal (se não estiver em nenhum obstáculo)
        if not ridden_block_this_frame and not current_frame_on_ground_flag: # Adicionado ridden_block_this_frame aqui
            if self.rect.bottom > GROUND_LEVEL:
                self.rect.bottom = GROUND_LEVEL
                self.vel_y = 0 
                current_frame_on_ground_flag = True
        
        self.on_ground = current_frame_on_ground_flag

        # A lógica de DANO por colisão com blocos caindo foi movida para main.py,
        # pois precisa acontecer DEPOIS que os blocos caindo também foram atualizados
        # e sabemos quais deles se tornaram estáticos.

        # Atualiza texto da altura
        player_top_on_screen = self.rect.y
        actual_height = GROUND_LEVEL - player_top_on_screen 
        self.current_height_text = f"Altura: {max(0, actual_height // 10)}"


    def draw(self, surface):
        """Desenha o jogador na tela."""
        surface.blit(self.image, self.rect)
        # Desenha a barra de vida acima do jogador
        health_bar_x = self.rect.x
        health_bar_y = self.rect.y - 7 
        health_bar_width = PLAYER_WIDTH
        health_bar_height = 5
        
        current_health_width = (self.health / MAX_PLAYER_HEALTH) * health_bar_width
        if current_health_width < 0: current_health_width = 0

        pygame.draw.rect(surface, RED, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        if self.health > 0:
            pygame.draw.rect(surface, GREEN, (health_bar_x, health_bar_y, current_health_width, health_bar_height))
