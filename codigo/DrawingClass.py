import os
import pygame


BACKGROUND = pygame.image.load(
    os.path.join(os.path.dirname(__file__), 'img', 'background.png')
)


class Drawing:
    def __init__(self, window):
        self.window = window
        self.background = pygame.transform.scale(BACKGROUND, window.get_size())

    def drawing(self, game, player, enemies, FPS, puntos=0):
        self.window.blit(self.background, (0, 0))
        for enemy in enemies:
            enemy.draw(self.window)
        player.draw(self.window)
        for bullet in player.fired_bullets:
            bullet.draw(self.window)
        game.draw_HUD()
        points_label = game.font.render(f'Points: {puntos}', True, (255, 255, 255))
        self.window.blit(points_label, points_label.get_rect(center=(self.window.get_width() // 2, 20)))
        pygame.display.update()
