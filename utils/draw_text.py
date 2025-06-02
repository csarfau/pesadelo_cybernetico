import pygame

def draw_text(text, font, color, surface, x, y, center=False):
    """Desenha texto na tela."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    # Não precisa retornar o rect aqui, pois a checagem de clique é feita no loop principal