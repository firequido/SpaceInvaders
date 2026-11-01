"""Informacion del proyecto y enlace a Hybridge."""
from pathlib import Path
import webbrowser

import pygame


BASE_DIR = Path(__file__).resolve().parent


class MenuAcercaDe:
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    GRIS = (200, 200, 200)
    ROJO = (255, 0, 0)
    ANCHO = 800
    ALTO = 600
    URL_HYBRIDGE = 'https://hybridge.education'
    CONTENIDO = (
        '¡Explora la galaxia y aprende Programación Orientada a Objetos (POO) '
        'con nuestro emocionante Space Invaders!\n'
        'Cada nave, cada disparo, ¡todo es un objeto interactivo!\n'
        'Únete a nosotros para una experiencia divertida y educativa en este '
        'emocionante cruce de juego y aprendizaje.\n'
        '¡Prepárate para salvar el universo!'
    )

    def __init__(self, back_mtd=None, ventana=None):
        # Importar la clase no abre ventanas: se crean al instanciarla.
        if not pygame.display.get_init():
            pygame.display.init()
        if not pygame.font.get_init():
            pygame.font.init()
        self.ventana = ventana if ventana is not None else pygame.display.set_mode(
            (self.ANCHO, self.ALTO))
        self.ANCHO, self.ALTO = self.ventana.get_size()
        self.back_mtd = back_mtd
        self.clock = pygame.time.Clock()
        self.fondo = pygame.transform.scale(
            self.cargar_imagen('menu_fondo.jpg'), (self.ANCHO, self.ALTO))
        self.boton_atras = pygame.Rect(20, 20, 50, 50)
        self.enlace_rect = pygame.Rect(0, 0, 0, 0)
        self.font_titulo = pygame.font.Font(None, 48)
        self.font_subtitulo = pygame.font.Font(None, 36)
        self.font_contenido = pygame.font.Font(None, 30)

    def cargar_imagen(self, nombre_archivo):
        ruta = BASE_DIR / 'img' / nombre_archivo
        return pygame.image.load(str(ruta)).convert_alpha()

    def mostrar_texto(self, texto, font, color, superficie, x, y):
        texto_objeto = font.render(texto, True, color)
        rectangulo_texto = texto_objeto.get_rect(topleft=(round(x), round(y)))
        superficie.blit(texto_objeto, rectangulo_texto)
        # El rectangulo permite detectar clics exactamente sobre el enlace.
        return rectangulo_texto

    def dibujar_boton(self, texto, font, color, superficie, x, y, ancho, alto):
        pygame.draw.rect(superficie, color, (x, y, ancho, alto))
        texto_ancho, texto_alto = font.size(texto)
        self.mostrar_texto(texto, font, self.NEGRO, superficie,
                           x + (ancho - texto_ancho) // 2,
                           y + (alto - texto_alto) // 2)

    def mostrar_contenido(self, contenido, font_contenido, y_offset):
        espacio_horizontal_disponible = self.ANCHO - 100
        for parrafo in contenido.split('\n'):
            texto_linea = ''
            lineas = []
            for palabra in parrafo.split():
                candidato = f'{texto_linea} {palabra}'.strip()
                if texto_linea and font_contenido.size(candidato)[0] > espacio_horizontal_disponible:
                    lineas.append(texto_linea)
                    texto_linea = palabra
                else:
                    texto_linea = candidato
            lineas.append(texto_linea)
            for linea in lineas:
                x = (self.ANCHO - font_contenido.size(linea)[0]) // 2
                self.mostrar_texto(linea, font_contenido, self.BLANCO,
                                   self.ventana, x, y_offset)
                y_offset += max(font_contenido.get_linesize(), font_contenido.size(linea)[1]) + 4
        return y_offset

    def mostrar_menu(self):
        self.ventana.blit(self.fondo, (0, 0))
        for texto, font, y in (
            ('Acerca De', self.font_titulo, 50),
            ('Space Invaders Hybridge', self.font_subtitulo, 120),
        ):
            x = (self.ANCHO - font.size(texto)[0]) // 2
            self.mostrar_texto(texto, font, self.BLANCO, self.ventana, x, y)
        self.mostrar_contenido(self.CONTENIDO, self.font_contenido, 200)

        texto_enlace = '¡Haz clic aquí para visitar Hybridge!'
        enlace_x = (self.ANCHO - self.font_contenido.size(texto_enlace)[0]) // 2
        self.enlace_rect = self.mostrar_texto(
            texto_enlace, self.font_contenido, self.ROJO, self.ventana, enlace_x, 500)
        self.dibujar_boton('<', self.font_subtitulo, self.GRIS, self.ventana,
                           *self.boton_atras)
        pygame.display.update()

    def volver(self):
        if self.back_mtd is not None:
            return self.back_mtd()
        return True

    def ejecutar(self):
        """True regresa al menu principal; False solicita cerrar el programa."""
        pygame.display.set_caption('Acerca De')
        self.mostrar_menu()
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER):
                    return self.volver()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.boton_atras.collidepoint(event.pos):
                        return self.volver()
                    if self.enlace_rect.collidepoint(event.pos):
                        webbrowser.open(self.URL_HYBRIDGE)
            self.mostrar_menu()


def main():
    pygame.init()
    try:
        MenuAcercaDe().ejecutar()
    finally:
        pygame.quit()

