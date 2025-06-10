import pygame
import sys
import random
from settings.settings import *
from sprites.obstacles import Obstacle
from sprites.player import Player
from utils.create_button import create_button
from utils.draw_text import draw_text

pygame.init()
pygame.font.init()

# --- Configuração da Tela ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blocos Empilháveis")
clock = pygame.time.Clock()

background_image = pygame.image.load("assets/images/windows_3/background_start.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

background_game_img = pygame.image.load("assets/images/windows_3/win3.0.jpg").convert()
background_game_img = pygame.transform.scale(background_game_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

ground_img = pygame.image.load("assets/images/windows_3/Barra_rolagem_deitado.png").convert_alpha()
ground_img = pygame.transform.scale(ground_img, (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_LEVEL))

btn_start_img = pygame.image.load("assets/images/buttons/start.png").convert_alpha()
btn_select_img = pygame.image.load("assets/images/buttons/choose_level.png").convert_alpha()
btn_exit_img = pygame.image.load("assets/images/buttons/exit.png").convert_alpha()

btn_start_img = pygame.transform.scale(btn_start_img, (200, 40))
btn_select_img = pygame.transform.scale(btn_select_img, (200, 40))
btn_exit_img = pygame.transform.scale(btn_exit_img, (200, 40))

obstacle_images = [
    pygame.transform.scale(pygame.image.load("assets/images/Cartas/carta_bananas.png").convert_alpha(), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/images/Cartas/carta_demolidor.png").convert_alpha(), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/images/Cartas/carta_linux.png").convert_alpha(), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/images/Cartas/carta_minion.png").convert_alpha(), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/images/Cartas/carta_not_found.png").convert_alpha(), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/images/Cartas/carta_scooby.png").convert_alpha(), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/images/Cartas/carta_teletubbies.png").convert_alpha(), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)),
]

try:
    DEFAULT_FONT = pygame.font.Font(FONT_NAME, DEFAULT_FONT_SIZE)
    LARGE_FONT = pygame.font.Font(FONT_NAME, LARGE_FONT_SIZE)
    SMALL_FONT = pygame.font.Font(FONT_NAME, SMALL_FONT_SIZE)
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

falling_obstacles = pygame.sprite.Group()
static_obstacles = pygame.sprite.Group()
obstacle_spawn_timer = 0

def reset_level_state():
    global player, falling_obstacles, static_obstacles, obstacle_spawn_timer
    player.reset()
    falling_obstacles.empty()
    static_obstacles.empty()
    obstacle_spawn_timer = 0

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
        screen.blit(background_image, (0, 0))
        
        mouse_pos = pygame.mouse.get_pos()

        draw_text("Pesadelo Cibernético", LARGE_FONT, DARK_GRAY, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4+50, center=True)

        base_y = SCREEN_HEIGHT // 2 + 100
        spacing = 50

        btn_start_rect = btn_start_img.get_rect(center=(SCREEN_WIDTH // 2, base_y))
        btn_select_rect = btn_select_img.get_rect(center=(SCREEN_WIDTH // 2, base_y + spacing))
        btn_exit_rect = btn_exit_img.get_rect(center=(SCREEN_WIDTH // 2, base_y + spacing * 2))
        
        if btn_start_rect.collidepoint(mouse_pos) or btn_select_rect.collidepoint(mouse_pos) or btn_exit_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        screen.blit(btn_start_img, btn_start_rect)
        screen.blit(btn_select_img, btn_select_rect)
        screen.blit(btn_exit_img, btn_exit_rect)

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
        screen.blit(background_image, (0, 0))
        draw_text("Escolher Fase", LARGE_FONT, DARK_GRAY, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5+50, center=True)

        base_y = SCREEN_HEIGHT // 2 + 100
        spacing = 50

        btn_fase1_rect = btn_exit_img.get_rect(center=(SCREEN_WIDTH // 2, base_y))
        draw_text("Fase 2 (Em breve)", DEFAULT_FONT, GRAY, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + base_y + spacing, center=True)
        draw_text("Fase 3 (Em breve)", DEFAULT_FONT, GRAY, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + base_y + spacing * 2, center=True)
        btn_back_rect = btn_exit_img.get_rect(center=(SCREEN_WIDTH // 2, base_y+spacing*2))

        screen.blit(btn_exit_img, btn_fase1_rect)
        screen.blit(btn_exit_img, btn_back_rect)

        if click_pos:
            if btn_fase1_rect.collidepoint(click_pos):
                selected_level = 1
                reset_level_state()
                current_game_state = GAME_STATE_PLAYING
            elif btn_back_rect.collidepoint(click_pos):
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
            obs_image = random.choice(obstacle_images)
            # Os obstáculos começam um pouco acima da tela para não aparecerem subitamente
            new_obstacle = Obstacle(
                obs_x, 
                -OBSTACLE_HEIGHT - 5,
                OBSTACLE_WIDTH, 
                OBSTACLE_HEIGHT, 
                OBSTACLE_COLOR, 
                OBSTACLE_FALL_SPEED, 
                image=obs_image
            )
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
        screen.fill((0,0,0))
        # screen.blit(background_game_img, (0, 0))

        # Desenha o chão
        screen.blit(ground_img, (0, GROUND_LEVEL))

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