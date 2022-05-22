import pygame

#determines if the player is in bounds
def colliding(game, player):
    col = True
    for s in game.map.sprites:
        if s["type"] == "collision":
            r = pygame.Rect( s["x"], s["y"], s["width"], s["height"] )
            if r.contains( player.getHitBox() ):
                col = False
    return col
