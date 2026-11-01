"""Captura el nombre del jugador al superar el record maximo."""
from pathlib import Path

import pygame
from Puntajes import guardar_registro


BASE_DIR = Path(__file__).resolve().parent


class PantallaNombre:
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    GRIS = (200, 200, 200)
    ANCHO = 800
    ALTO = 600

    def __init__(self, puntaje, finish_mtd=None, ventana=None):
        if not pygame.display.get_init():
            pygame.display.init()
        if not pygame.font.get_init():
            pygame.font.init()
        self.ventana = ventana if ventana is not None else pygame.display.set_mode(
            (self.ANCHO, self.ALTO))
        self.ANCHO, self.ALTO = self.ventana.get_size()
        self.puntaje = puntaje
        self.finish_mtd = finish_mtd
        self.fuente_titulo = pygame.font.Font(None, 36)
        self.fuente_subtitulo = pygame.font.Font(None, 32)
        self.fuente_input = pygame.font.Font(None, 36)
        self.fuente_aviso = pygame.font.Font(None, 26)
        self.texto_input = ''
        self.input_active = True
        self.error = ''
        self.guardado = False
        self.input_box = pygame.Rect(self.ANCHO // 2 - 200, 230, 400, 50)
        self.boton_aceptar = pygame.Rect(self.ANCHO // 2 - 100, 320, 200, 50)
        self.fondo = self.cargar_imagen('menu_fondo.jpg')
        self.clock = pygame.time.Clock()

    def cargar_imagen(self, nombre_archivo):
        return pygame.transform.scale(pygame.image.load(
            str(BASE_DIR / 'img' / nombre_archivo)).convert(), (self.ANCHO, self.ALTO))

    def escribir_en_archivo(self, nombre_archivo, contenido):
        try:
            nombre, puntuacion = contenido.rsplit(',', 1)
            guardar_registro(nombre_archivo, nombre, puntuacion)
        except ValueError as error:
            self.error = str(error)
            return False
        except OSError:
            self.error = 'No se pudo guardar. Revisa el archivo e inténtalo de nuevo.'
            return False
        return True

    def guardar(self):
        if self.guardado:
            return True
        if not self.escribir_en_archivo('puntajes.txt', f'{self.texto_input},{self.puntaje}'):
            return False
        self.guardado = True
        if self.finish_mtd is not None:
            self.finish_mtd()
        return True

    def dibujar(self):
        self.ventana.blit(self.fondo, (0, 0))
        for texto, fuente, y in (
            ('¡Felicidades! Superaste el récord máximo', self.fuente_titulo, 55),
            ('Space Invaders Hybridge', self.fuente_subtitulo, 105),
            (f'Puntaje: {self.puntaje}', self.fuente_titulo, 160),
            ('Escribe tu nombre:', self.fuente_subtitulo, 205),
            ('Enter: guardar | Esc: volver sin guardar', self.fuente_aviso, 425),
        ):
            superficie = fuente.render(texto, True, self.BLANCO)
            self.ventana.blit(superficie, superficie.get_rect(center=(self.ANCHO // 2, y)))
        color = self.BLANCO if self.input_active else self.GRIS
        pygame.draw.rect(self.ventana, color, self.input_box, 2)
        superficie = self.fuente_input.render(self.texto_input, True, self.BLANCO)
        self.ventana.blit(superficie, (self.input_box.x + 10, self.input_box.y + 10))
        pygame.draw.rect(self.ventana, self.GRIS, self.boton_aceptar)
        superficie = self.fuente_input.render('Aceptar', True, self.NEGRO)
        self.ventana.blit(superficie, superficie.get_rect(center=self.boton_aceptar.center))
        if self.error:
            superficie = self.fuente_aviso.render(self.error, True, (255, 160, 160))
            self.ventana.blit(superficie, superficie.get_rect(center=(self.ANCHO // 2, 480)))
        pygame.display.update()

    def ejecutar(self):
        """True vuelve al menu (guardar o cancelar); False cierra el programa."""
        pygame.display.set_caption('Ingresar nombre')
        pygame.key.start_text_input()
        pygame.key.set_text_input_rect(self.input_box)
        try:
            while True:
                self.clock.tick(60)
                self.dibujar()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.boton_aceptar.collidepoint(event.pos):
                            if self.guardar():
                                return True
                        else:
                            self.input_active = self.input_box.collidepoint(event.pos)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return True
                        if self.input_active:
                            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and self.guardar():
                                return True
                            if event.key == pygame.K_BACKSPACE:
                                self.texto_input = self.texto_input[:-1]
                                self.error = ''
                    # TEXTINPUT admite acentos y evita confundir texto con teclas de control.
                    if event.type == pygame.TEXTINPUT and self.input_active:
                        for caracter in event.text:
                            candidato = self.texto_input + caracter
                            if (caracter.isprintable() and caracter != ','
                                    and len(candidato) <= 24
                                    and self.fuente_input.size(candidato)[0] <= self.input_box.width - 20):
                                self.texto_input = candidato
                        self.error = ''
        finally:
            pygame.key.stop_text_input()

