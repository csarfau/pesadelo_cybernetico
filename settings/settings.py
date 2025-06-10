# --- Constantes do Jogo ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Cores (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230) # Cor do céu/fundo
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
GROUND_COLOR = (139, 69, 19) # Marrom para o chão
OBSTACLE_COLOR = (100, 100, 100) # Cor dos obstáculos
PLAYER_COLOR = (0, 150, 255) # Cor do jogador
GOAL_COLOR = (255, 215, 0) # Dourado para a meta
SUCCESS_GREEN = (60, 179, 113) # Verde para tela de sucesso

# Cores de Hover para Botões
BUTTON_HOVER_GREEN = (0, 200, 0)
BUTTON_HOVER_BLUE = (0, 0, 200)
BUTTON_HOVER_RED = (200, 0, 0)
BUTTON_HOVER_GRAY = (100, 100, 100)

# Propriedades do Jogador
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_MOVE_SPEED = 5 # Renomeado para clareza
PLAYER_JUMP_STRENGTH = 30
PLAYER_GRAVITY = 1
MAX_PLAYER_HEALTH = 3

# Propriedades dos Obstáculos
OBSTACLE_WIDTH = 80
OBSTACLE_HEIGHT = 30
OBSTACLE_FALL_SPEED = 3 # Velocidade de queda
OBSTACLE_SPAWN_RATE = 120 # A cada N frames (ex: 120 frames = 2 segundos a 60FPS)

# Nível
GROUND_LEVEL = SCREEN_HEIGHT - 50 # Nível Y do chão
GOAL_HEIGHT_LEVEL_1 = 150 # Altura Y que o jogador precisa alcançar (menor Y é mais alto)

# Fontes
DEFAULT_FONT_SIZE = 36
LARGE_FONT_SIZE = 60
SMALL_FONT_SIZE = 24 # Adicionado para consistência
FONT_NAME = None # Usa a fonte padrão do sistema, pode ser "arial", "comicsansms", etc.