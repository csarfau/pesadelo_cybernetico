import pygame

def create_button(text, font, text_color, button_color, hover_color, surface, x, y, width, height):
    """Desenha um botão e retorna seu Rect. O estado de hover é gerenciado internamente."""
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    is_hovering = button_rect.collidepoint(mouse_pos)

    current_color = hover_color if is_hovering else button_color
    pygame.draw.rect(surface, current_color, button_rect, border_radius=10)
    pygame.draw.rect(surface, (30,30,30), button_rect, width=2, border_radius=10) # Borda escura

    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    surface.blit(text_surf, text_rect)

    return button_rect # Retorna o Rect para checagem de colisão externa no loop principal
