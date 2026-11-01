import pygame
import os
from Puntajes import leer_registros


BULLET_IMAGE = pygame.image.load(os.path.join(os.path.dirname(__file__), 'img', 'bullet_image.png'))

class Game:
    def __init__(self, font, FPS, lives, window,screen_width, screen_height, bullets= 0 , clock=None,):
        self.font = font
        self.HEIGTH = screen_height
        self.WIDTH = screen_width
        self.FPS = FPS
        self.lives = lives
        self.level = 1
        self.count = 0
        self.window = window
        self.clock = clock if clock is not None else pygame.time.Clock()
        self.bullets = bullets
        self.quit_requested = False
        self.bullet_img = BULLET_IMAGE
        self.registros = self.leer_registros('puntajes.txt')
        self.max_pun = self.registros[0][1] if self.registros else 0

 
    def leer_registros(self, nombre_archivo):
        return leer_registros(nombre_archivo)

    def escape(self):
        self.quit_requested = any(event.type == pygame.QUIT for event in pygame.event.get())
        return self.quit_requested

    def over(self):
        if self.lives <= 0:
            self.count = 0
            while True:
                if self.escape():
                    return True
                self.clock.tick(self.FPS)
                lost_label = self.font.render('GAME OVER',  1, (255,255,255))
                self.window.blit(lost_label, ((self.WIDTH-lost_label.get_width())/2, (self.HEIGTH-lost_label.get_height())/2))
                pygame.display.update()
                self.count += 1
                if self.count == self.FPS*3:
                    break
            return True
        else:
            return False
    
    def reload_bullet(self, bullet):
        self.bullets = bullet

   
    def draw_HUD(self):
        offset = 0
        lives_label = self.font.render(f'Lives: {self.lives}', 1, (255,255,255))
        level_label = self.font.render(f'Level: {self.level}', 1, (255,255,255))
        self.window.blit(lives_label, (10, 10))
        self.window.blit(level_label, (self.WIDTH-level_label.get_width()-10, 10))
        for i in range(self.bullets):
            offset += self.bullet_img.get_width() 
            self.window.blit(self.bullet_img, (self.WIDTH - offset, self.HEIGTH - 50))


