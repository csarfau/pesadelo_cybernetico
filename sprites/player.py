import pygame
from settings.settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        def load_and_scale(path, size):
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, size)

        sprite_size = (50, 50)  # Tamanho desejado (largura, altura)

        self.walk_right = [load_and_scale(f"assets/images/Avatar/walk_right{i}.png", sprite_size) for i in range(1, 4)]
        self.walk_left = [load_and_scale(f"assets/images/Avatar/walk_left{i}.png", sprite_size) for i in range(1, 4)]
        self.jump_right = load_and_scale("assets/images/Avatar/jump_right.png", sprite_size)
        self.jump_left = load_and_scale("assets/images/Avatar/jump_left.png", sprite_size)

        self.image = self.walk_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 400

        self.vel_y = 0
        self.speed = 5
        self.jump_power = 12
        self.on_ground = False
        self.health = 3
        self.current_height_text = "Altura: 0"
        self.direction = "right"
        self.anim_index = 0
        self.anim_timer = 0

    def reset(self):
        self.rect.x = 100
        self.rect.y = 400
        self.vel_y = 0
        self.on_ground = False
        self.health = 3
        self.direction = "right"

    def update(self, static_obstacles, falling_obstacles):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = "left"
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = "right"

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False

        # Gravidade
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10

        dy = self.vel_y

        # Movimentação horizontal
        self.rect.x += dx
        # Colisão horizontal
        for obstacle in static_obstacles:
            if self.rect.colliderect(obstacle.rect):
                if dx > 0:
                    self.rect.right = obstacle.rect.left
                elif dx < 0:
                    self.rect.left = obstacle.rect.right

# Movimentação vertical
        self.rect.y += dy
        self.on_ground = False
        for obstacle in static_obstacles:
            if self.rect.colliderect(obstacle.rect):
                if dy > 0:
                    self.rect.bottom = obstacle.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif dy < 0:
                    self.rect.top = obstacle.rect.bottom
                    self.vel_y = 0

        # Garantir que o jogador não caia abaixo do chão
        if self.rect.bottom > GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.vel_y = 0
            self.on_ground = True

        # Atualiza altura
        self.current_height_text = f"Altura: {SCREEN_HEIGHT - self.rect.y}"

        # --- Animação ---
        self.anim_timer += 1
        if self.anim_timer >= 6:  # Controla a velocidade da animação
            self.anim_index = (self.anim_index + 1) % 3
            self.anim_timer = 0

        if not self.on_ground:
            self.image = self.jump_right if self.direction == "right" else self.jump_left
        elif dx == 0:
            self.image = self.walk_right[0] if self.direction == "right" else self.walk_left[0]
        else:
            if self.direction == "right":
                self.image = self.walk_right[self.anim_index]
            else:
                self.image = self.walk_left[self.anim_index]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
