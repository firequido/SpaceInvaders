import pygame


class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, speed):
        self.y += speed

    def collision(self, obj):
        # La segunda mascara se coloca respecto al origen de la primera.
        offset = (round(obj.x) - round(self.x), round(obj.y) - round(self.y))
        return self.mask.overlap(obj.mask, offset) is not None
