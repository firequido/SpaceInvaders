"""Pantalla con los cinco mejores registros del archivo de puntajes."""
from pathlib import Path

import pygame
from Puntajes import leer_registros


BASE_DIR = Path(__file__).resolve().parent


class MenuPuntajes:
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    GRIS = (200, 200, 200)
    ROJO = (255, 0, 0)
    ANCHO = 800
    ALTO = 600

    def __init__(self, back_mtd=None, ventana=None):
        # Crear la ventana al instanciar, no al importar este archivo.
        if not pygame.display.get_init():
            pygame.display.init()
        if not pygame.font.get_init():
            pygame.font.init()
        self.ventana = ventana if ventana is not None else pygame.display.set_mode(
            (self.ANCHO, self.ALTO))
        self.ANCHO, self.ALTO = self.ventana.get_size()
        self.boton_atras = pygame.Rect(20, 20, 50, 50)
        self.back_mtd = back_mtd
        self.clock = pygame.time.Clock()
        # El fondo se carga una vez, en lugar de leerlo en cada dibujo.
        self.fondo = pygame.transform.scale(
            self.cargar_imagen('menu_fondo.jpg'), (self.ANCHO, self.ALTO))

    def cargar_puntajes(self, archivo):
        return leer_registros(archivo)

    def cargar_imagen(self, nombre_archivo):
        ruta = BASE_DIR / 'img' / nombre_archivo
        return pygame.image.load(str(ruta)).convert_alpha()

    def mostrar_texto(self, texto, font, color, superficie, x, y):
        texto_objeto = font.render(texto, True, color)
        rectangulo_texto = texto_objeto.get_rect(center=(round(x), round(y)))
        superficie.blit(texto_objeto, rectangulo_texto)

    def dibujar_boton(self, texto, font, color, superficie, x, y, ancho, alto):
        pygame.draw.rect(superficie, color, (x, y, ancho, alto))
        self.mostrar_texto(texto, font, self.NEGRO, superficie,
                           x + ancho / 2, y + alto / 2)

    def mostrar_puntajes(self, puntajes):
        self.ventana.blit(self.fondo, (0, 0))
        self.mostrar_texto('Mejores Puntajes', pygame.font.Font(None, 48),
                           self.BLANCO, self.ventana, self.ANCHO // 2, 50)
        self.mostrar_texto('Space Invaders Hybridge', pygame.font.Font(None, 36),
                           self.BLANCO, self.ventana, self.ANCHO // 2, 120)
        if not puntajes:
            self.mostrar_texto('Aún no hay registros', pygame.font.Font(None, 36),
                               self.ROJO, self.ventana, self.ANCHO // 2, self.ALTO // 2)
        else:
            for i, (nombre, puntaje) in enumerate(puntajes[:5], 1):
                color = self.BLANCO if i == 1 else self.ROJO
                tamano = 42 if i == 1 else 36
                self.mostrar_texto(f'{i}. {nombre}: {puntaje}',
                                   pygame.font.Font(None, tamano), color,
                                   self.ventana, self.ANCHO // 2, 250 + (i - 1) * 60)
        self.dibujar_boton('<', pygame.font.Font(None, 36), self.GRIS,
                           self.ventana, *self.boton_atras)
        pygame.display.update()

    def volver(self):
        if self.back_mtd is not None:
            return self.back_mtd()
        return True

    def ejecutar(self):
        """Devuelve True al volver y False si se cierra la ventana."""
        pygame.display.set_caption('Mejores Puntajes')
        puntajes = self.cargar_puntajes('puntajes.txt')
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return self.volver()
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                        and self.boton_atras.collidepoint(event.pos)):
                    return self.volver()
            self.mostrar_puntajes(puntajes)


def main():
    pygame.init()
    try:
        MenuPuntajes().ejecutar()
    finally:
        pygame.quit()

