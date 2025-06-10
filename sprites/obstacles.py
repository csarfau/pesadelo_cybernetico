import pygame
from settings.settings import * # Importa todas as constantes

class Obstacle(pygame.sprite.Sprite):
    """Classe para os obstáculos que caem e podem se empilhar."""
    def __init__(self, x, y, width, height, color, speed, image=None):
        super().__init__()
        self.speed = speed
        self.is_static = False 

        if image:
            self.image = self.image = image
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, static_obstacles_group):
        """Move o obstáculo para baixo e checa colisões para empilhamento."""
        if not self.is_static:
            original_y = self.rect.y
            self.rect.y += self.speed 

            # 1. Checar colisão com obstáculos estáticos abaixo para empilhar
            for static_obs in static_obstacles_group:
                if self.rect.colliderect(static_obs.rect):
                    # Garante que o bloco em queda estava acima ou no mesmo nível do topo do bloco estático
                    if original_y + self.rect.height <= static_obs.rect.top + 1: 
                        self.rect.bottom = static_obs.rect.top 
                        self.is_static = True
                        return 

            # 2. Se não pousou em nenhum obstáculo, checa colisão com o chão
            if self.rect.bottom >= GROUND_LEVEL:
                self.rect.bottom = GROUND_LEVEL
                self.is_static = True
                return
    def draw(self, surface):
        """Desenha o obstáculo na tela."""
        surface.blit(self.image, self.rect)