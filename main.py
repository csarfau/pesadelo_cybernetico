# main.py

import pygame
import sys
import random
from settings.settings import *
from sprites.obstacles import Obstacle
from sprites.player import Player
from utils.create_button import create_button
from utils.draw_text import draw_text

# Inicialização do Pygame
pygame.init()
pygame.font.init() # Inicializa o módulo de fontes

# --- Configuração da Tela ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blocos Empilháveis")
clock = pygame.time.Clock()

# Fontes
try:
    DEFAULT_FONT = pygame.font.Font(FONT_NAME, DEFAULT_FONT_SIZE)
    LARGE_FONT = pygame.font.Font(FONT_NAME, LARGE_FONT_SIZE)
    SMALL_FONT = pygame.font.Font(FONT_NAME, SMALL_FONT_SIZE) # Corrigido para SMALL_FONT_SIZE
except pygame.error:
    print("A fonte padrão do sistema não pôde ser carregada. Usando fallback.")
    DEFAULT_FONT = pygame.font.SysFont("arial", DEFAULT_FONT_SIZE)
    LARGE_FONT = pygame.font.SysFont("arial", LARGE_FONT_SIZE)
    SMALL_FONT = pygame.font.SysFont("arial", SMALL_FONT_SIZE)


# --- Estados do Jogo ---
GAME_STATE_MAIN_MENU = "main_menu"
GAME_STATE_LEVEL_SELECT = "level_select"
GAME_STATE_PLAYING = "playing"
GAME_STATE_GAME_OVER = "game_over"
GAME_STATE_LEVEL_COMPLETE = "level_complete"

current_game_state = GAME_STATE_MAIN_MENU
selected_level = 1

# --- Grupos de Sprites e Variáveis do Jogo ---
player = Player()
# all_sprites = pygame.sprite.Group() # Pode ser útil se quiser um grupo para todos os sprites
# all_sprites.add(player)

falling_obstacles = pygame.sprite.Group()
static_obstacles = pygame.sprite.Group() # Obstáculos que viraram plataformas
obstacle_spawn_timer = 0
# score = 0 # Não usado ativamente no momento

def reset_level_state():
    """Reseta o estado para iniciar um novo nível ou tentar novamente."""
    global player, falling_obstacles, static_obstacles, obstacle_spawn_timer #, score
    player.reset()
    falling_obstacles.empty()
    static_obstacles.empty()
    # Se usar all_sprites, limpar e adicionar o jogador novamente:
    # all_sprites.empty()
    # all_sprites.add(player)
    obstacle_spawn_timer = 0
    # score = 0


# --- Loop Principal do Jogo ---
running = True
while running:
    click_pos = None # Posição do clique do mouse neste frame, resetado a cada frame
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Botão esquerdo do mouse
                click_pos = event.pos

    # --- Lógica dos Estados do Jogo ---

    if current_game_state == GAME_STATE_MAIN_MENU:
        screen.fill(LIGHT_BLUE)
        draw_text("Blocos Empilháveis", LARGE_FONT, DARK_GRAY, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, center=True)

        btn_start_rect = create_button("Iniciar Jogo", DEFAULT_FONT, WHITE, GREEN, BUTTON_HOVER_GREEN, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 60)
        btn_select_rect = create_button("Escolher Fase", DEFAULT_FONT, WHITE, BLUE, BUTTON_HOVER_BLUE, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 80, 300, 60)
        btn_exit_rect = create_button("Sair", DEFAULT_FONT, WHITE, RED, BUTTON_HOVER_RED, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 160, 300, 60)

        if click_pos:
            if btn_start_rect.collidepoint(click_pos):
                selected_level = 1
                reset_level_state()
                current_game_state = GAME_STATE_PLAYING
            elif btn_select_rect.collidepoint(click_pos):
                current_game_state = GAME_STATE_LEVEL_SELECT
            elif btn_exit_rect.collidepoint(click_pos):
                running = False

    elif current_game_state == GAME_STATE_LEVEL_SELECT:
        screen.fill(LIGHT_BLUE)
        draw_text("Escolher Fase", LARGE_FONT, DARK_GRAY, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5, center=True)

        btn_fase1_rect = create_button("Fase 1", DEFAULT_FONT, WHITE, GREEN, BUTTON_HOVER_GREEN, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
        draw_text("Fase 2 (Em breve)", DEFAULT_FONT, GRAY, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, center=True)
        draw_text("Fase 3 (Em breve)", DEFAULT_FONT, GRAY, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70, center=True)
        btn_voltar_ls_rect = create_button("Voltar", DEFAULT_FONT, WHITE, RED, BUTTON_HOVER_RED, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)

        if click_pos:
            if btn_fase1_rect.collidepoint(click_pos):
                selected_level = 1
                reset_level_state()
                current_game_state = GAME_STATE_PLAYING
            elif btn_voltar_ls_rect.collidepoint(click_pos):
                current_game_state = GAME_STATE_MAIN_MENU

    elif current_game_state == GAME_STATE_PLAYING:
        # --- Lógica do Jogo ---
        # Atualiza o jogador, passando os obstáculos estáticos e os que estão caindo
        player.update(static_obstacles, falling_obstacles) 

        # Spawning de obstáculos
        obstacle_spawn_timer += 1
        if obstacle_spawn_timer >= OBSTACLE_SPAWN_RATE:
            obstacle_spawn_timer = 0
            obs_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
            # Os obstáculos começam um pouco acima da tela para não aparecerem subitamente
            new_obstacle = Obstacle(obs_x, -OBSTACLE_HEIGHT - 5, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_COLOR, OBSTACLE_FALL_SPEED)
            falling_obstacles.add(new_obstacle)
            # all_sprites.add(new_obstacle) # Adicionar a all_sprites se for usar para desenhar/atualizar tudo

        # Atualizar obstáculos em queda (eles caem, checam empilhamento em static_obstacles)
        for obs in list(falling_obstacles): # Iterar sobre uma cópia para poder remover
            obs.update(static_obstacles) # Passa os obstáculos estáticos para checar empilhamento
            if obs.is_static:
                falling_obstacles.remove(obs) # Remove do grupo de queda
                static_obstacles.add(obs)   # Adiciona ao grupo de estáticos
            elif obs.rect.top > SCREEN_HEIGHT: # Se saiu da tela por baixo (raro com a lógica atual)
                obs.kill() # Remove de todos os grupos a que pertence

        # LÓGICA DE DANO AO JOGADOR POR BLOCOS EM QUEDA
        # Esta lógica deve vir DEPOIS que o jogador e os blocos em queda foram atualizados.
        
        # Primeiro, determina se o jogador está "surfando" em um bloco que AINDA está caindo.
        # O player.on_ground pode ser True por estar em um bloco estático, então precisamos de uma checagem mais específica.
        is_player_definitively_riding_a_FALLING_block = False
        if player.on_ground: 
            # Cria um pequeno rect abaixo dos pés do jogador para checar a colisão com o topo do bloco em queda
            player_feet_check_rect = player.rect.copy()
            player_feet_check_rect.y += 1 # Um pixel abaixo dos pés
            player_feet_check_rect.height = 1 # Altura mínima para o rect de checagem

            for current_falling_obs in falling_obstacles: # Checa contra blocos que AINDA estão caindo
                # Se os pés (ajustados) colidem com o bloco em queda
                # E o fundo do jogador está alinhado com o topo do bloco em queda (confirmando que está em cima)
                if player_feet_check_rect.colliderect(current_falling_obs.rect) and \
                    abs(player.rect.bottom - current_falling_obs.rect.top) < 2: # Pequena tolerância para alinhamento
                    is_player_definitively_riding_a_FALLING_block = True
                    break # Encontrou o bloco em que está surfando
        
        # Se o jogador NÃO está "surfando" em um bloco em queda, então qualquer colisão com um bloco em queda causa dano.
        if not is_player_definitively_riding_a_FALLING_block:
            # Verifica colisões com os blocos que ainda estão no grupo falling_obstacles
            # O terceiro argumento False significa que os sprites atingidos não são removidos automaticamente do grupo falling_obstacles
            hit_by_falling_for_damage = pygame.sprite.spritecollide(player, falling_obstacles, False) 
            
            for obs_that_hit_player in hit_by_falling_for_damage:
                # Se colidiu e não estava surfando de forma segura, é dano.
                # A condição "atingido na cabeça ou nas laterais" é implicitamente coberta aqui,
                # pois uma aterrissagem segura nos pés já teria sido classificada como "surfar".
                player.health -= 1
                obs_that_hit_player.kill() # O bloco que causou dano desaparece (removido de todos os grupos)
                
                # print(f"JOGADOR ATINGIDO! Vida: {player.health}") # Para debug

                if player.health <= 0:
                    current_game_state = GAME_STATE_GAME_OVER
                    break # Processa apenas um acerto danoso por frame e sai se game over
            if current_game_state == GAME_STATE_GAME_OVER: # Checa se o estado mudou para sair do loop de jogo
                pass # O loop principal tratará a mudança de estado

        # Checar condição de vitória (alcançar altura Y)
        if player.rect.top <= GOAL_HEIGHT_LEVEL_1 and current_game_state == GAME_STATE_PLAYING: # Garante que só vence se ainda estiver jogando
            current_game_state = GAME_STATE_LEVEL_COMPLETE
        
        # --- Desenho do Jogo ---
        screen.fill(LIGHT_BLUE) # Fundo do céu

        # Desenha o chão
        pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_LEVEL))

        # Desenha a linha de meta
        pygame.draw.line(screen, GOAL_COLOR, (0, GOAL_HEIGHT_LEVEL_1), (SCREEN_WIDTH, GOAL_HEIGHT_LEVEL_1), 3)
        draw_text("META", SMALL_FONT, GOAL_COLOR, screen, SCREEN_WIDTH - 60, GOAL_HEIGHT_LEVEL_1 - 25)

        # Desenha obstáculos estáticos e caindo
        static_obstacles.draw(screen)
        falling_obstacles.draw(screen)
        
        # Desenha o jogador
        player.draw(screen) # Ou all_sprites.draw(screen) se tudo estiver lá

        # HUD (Heads-Up Display)
        draw_text(f"Vida: {player.health}", DEFAULT_FONT, DARK_GRAY, screen, 10, 10)
        draw_text(player.current_height_text, DEFAULT_FONT, DARK_GRAY, screen, 10, 50)
        draw_text(f"Fase: {selected_level}", DEFAULT_FONT, DARK_GRAY, screen, SCREEN_WIDTH - 150, 10)


    elif current_game_state == GAME_STATE_GAME_OVER:
        screen.fill(DARK_GRAY)
        draw_text("GAME OVER", LARGE_FONT, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, center=True)
        
        btn_jogar_novamente_go_rect = create_button("Jogar Novamente", DEFAULT_FONT, WHITE, GREEN, BUTTON_HOVER_GREEN, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 60)
        btn_menu_principal_go_rect = create_button("Menu Principal", DEFAULT_FONT, WHITE, BLUE, BUTTON_HOVER_BLUE, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 80, 300, 60)

        if click_pos:
            if btn_jogar_novamente_go_rect.collidepoint(click_pos):
                reset_level_state() # Reseta para o nível que estava sendo jogado
                current_game_state = GAME_STATE_PLAYING
            elif btn_menu_principal_go_rect.collidepoint(click_pos):
                current_game_state = GAME_STATE_MAIN_MENU
    
    elif current_game_state == GAME_STATE_LEVEL_COMPLETE:
        screen.fill(SUCCESS_GREEN) # Cor de sucesso
        draw_text(f"Fase {selected_level} Completa!", LARGE_FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, center=True)
        
        btn_jogar_novamente_lc_rect = create_button("Jogar Novamente", DEFAULT_FONT, WHITE, BLUE, BUTTON_HOVER_BLUE, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 60)
        btn_menu_principal_lc_rect = create_button("Menu Principal", DEFAULT_FONT, WHITE, GRAY, BUTTON_HOVER_GRAY, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 80, 300, 60)

        if click_pos:
            if btn_jogar_novamente_lc_rect.collidepoint(click_pos):
                reset_level_state() # Reinicia a mesma fase
                current_game_state = GAME_STATE_PLAYING
            elif btn_menu_principal_lc_rect.collidepoint(click_pos):
                current_game_state = GAME_STATE_MAIN_MENU


    pygame.display.flip() # Atualiza a tela inteira
    clock.tick(FPS) # Controla a taxa de quadros por segundo

pygame.quit()
sys.exit()