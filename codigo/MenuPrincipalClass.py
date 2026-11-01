"""Menu inicial: selecciona una pantalla con las flechas y Enter."""
from pathlib import Path

import pygame


BASE_DIR = Path(__file__).resolve().parent


class MenuPrincipal:
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    ROJO = (255, 0, 0)
    ANCHO = 800
    ALTO = 600
    DIR_IMAGENES = BASE_DIR / 'img'
    OPCIONES = ('Iniciar juego', 'Puntajes', 'Acerca de')

    def __init__(self, init_game_mtd=None, init_score_mtd=None, init_about_mtd=None,
                 ventana=None):
        if not pygame.display.get_init():
            pygame.display.init()
        if not pygame.font.get_init():
            pygame.font.init()
        self.ventana = ventana if ventana is not None else pygame.display.set_mode(
            (self.ANCHO, self.ALTO))
        self.ANCHO, self.ALTO = self.ventana.get_size()
        self.init_game_mtd = init_game_mtd
        self.init_score_mtd = init_score_mtd
        self.init_about_mtd = init_about_mtd
        self.clock = pygame.time.Clock()
        self.opcion_seleccionada = 0
        self.fondo = pygame.transform.scale(
            self.cargar_imagen('menu_fondo.jpg'), (self.ANCHO, self.ALTO))
        self.imagen = pygame.transform.scale(self.cargar_imagen('hybridge.gif'), (80, 80))
        self.fuente_titulo = pygame.font.Font(None, 64)
        self.fuente_subtitulo = pygame.font.Font(None, 36)
        self.fuente_opciones = pygame.font.Font(None, 32)

    def cargar_imagen(self, nombre_archivo):
        return pygame.image.load(str(self.DIR_IMAGENES / nombre_archivo)).convert_alpha()

    def mostrar_texto(self, texto, font, color, superficie, x, y):
        texto_objeto = font.render(texto, True, color)
        rectangulo_texto = texto_objeto.get_rect(center=(round(x), round(y)))
        superficie.blit(texto_objeto, rectangulo_texto)
        return rectangulo_texto

    def dibujar(self):
        self.ventana.blit(self.fondo, (0, 0))
        self.mostrar_texto('Space Invaders', self.fuente_titulo, self.BLANCO,
                           self.ventana, self.ANCHO // 2, self.ALTO // 4)
        self.mostrar_texto('Hybridge', self.fuente_subtitulo, self.BLANCO,
                           self.ventana, self.ANCHO // 2, self.ALTO // 4 + 40)
        self.ventana.blit(self.imagen, (self.ANCHO // 2 - 40, self.ALTO // 4 + 60))
        rectangulos_texto = []
        for i, opcion in enumerate(self.OPCIONES):
            rectangulos_texto.append(self.mostrar_texto(
                opcion, self.fuente_opciones, self.BLANCO, self.ventana,
                self.ANCHO // 2, self.ALTO // 4 + 90 * (i + 1) + 100))
        selector_rect = pygame.Rect(0, 0, 300, 50)
        # Centrar el borde en el texto de la opcion seleccionada.
        selector_rect.center = rectangulos_texto[self.opcion_seleccionada].center
        pygame.draw.rect(self.ventana, self.ROJO, selector_rect, 2)
        pygame.display.update()

    def menu_principal(self):
        """Ejecuta la opcion; True vuelve al menu, False o None cierra."""
        pygame.display.set_caption('Space Invaders')
        while True:
            self.clock.tick(60)
            self.dibujar()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return None
                    if evento.key == pygame.K_UP:
                        self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.OPCIONES)
                    elif evento.key == pygame.K_DOWN:
                        self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.OPCIONES)
                    elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        opcion = self.OPCIONES[self.opcion_seleccionada]
                        acciones = (self.init_game_mtd, self.init_score_mtd, self.init_about_mtd)
                        accion = acciones[self.opcion_seleccionada]
                        return accion() if accion is not None else opcion


