"""Inicio del programa: menu principal, partida y mejores puntajes."""
from pathlib import Path

import pygame
from pygame import mixer
from PlayerClass import Player, PLAYER_IMAGE, WIDTH, HEIGHT
from EnemyClass import Enemy
from GameClass import Game
from DrawingClass import Drawing
from MenuPrincipalClass import MenuPrincipal
from MenuPuntajesClass import MenuPuntajes
from MenuAcercaDeClass import MenuAcercaDe
from PantallaNombreClass import PantallaNombre


BASE_DIR = Path(__file__).resolve().parent
TITLE = 'Space Invaders Hybridge'


def cargar_sonido(nombre_archivo):
    try:
        return mixer.Sound(str(BASE_DIR / 'sounds' / nombre_archivo))
    except (pygame.error, OSError) as error:
        print(f'No se pudo cargar {nombre_archivo}: {error}')
        return None


def jugar(window):
    """True vuelve al menu; False solicita cerrar todo el programa."""
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    game = Game(pygame.font.SysFont(None, 30), 60, 3, window, WIDTH, HEIGHT,
                clock=clock)
    puntaje = 0
    explosion = cargar_sonido('explosion.wav')
    ganar = cargar_sonido('ganar.mp3')
    drawing = Drawing(window)
    player_x = (WIDTH - PLAYER_IMAGE.get_width()) / 2
    player = Player(player_x, 480, 5, 4)
    enemy_init = Enemy(speed=0.8)
    enemy_wave = 4
    enemies = enemy_init.create(enemy_wave)

    while True:
        clock.tick(game.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
        if not enemies:
            game.level += 1
            enemy_wave += 1
            enemy_init.increase_speed()
            player.increase_speed()
            enemies = enemy_init.create(enemy_wave)

            # Se premia una sola vez al ENTRAR en un multiplo de tres.
            if game.level % 3 == 0:
                player.max_amount_bullets = min(10, player.max_amount_bullets + 1)
                game.lives = min(6, game.lives + 1)

        player.move()
        player.create_bullets()
        player.fire(window)
        player.cooldown()
        for enemy in enemies[:]:
            enemy.move()
            if player.hit(enemy):
                # hit() ya elimina la bala que impacto al enemigo.
                enemies.remove(enemy)
                puntaje += 1
                if explosion is not None:
                    explosion.play()
            elif enemy.y + enemy.get_height() >= HEIGHT:
                enemies.remove(enemy)
                game.lives -= 1

        game.reload_bullet(len(player.bullets))
        drawing.drawing(game, player, enemies, game.FPS, puntaje)
        if game.over():
            if game.quit_requested:
                return False
            # La leccion registra solo puntajes que SUPEREN el record maximo.
            if puntaje > game.max_pun:
                if ganar is not None:
                    ganar.play()
                try:
                    return PantallaNombre(puntaje, ventana=window).ejecutar()
                finally:
                    if ganar is not None:
                        ganar.stop()
            return True


def main():
    pygame.init()
    try:
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_icon(pygame.image.load(str(BASE_DIR / 'img' / 'title_icon.png')))
        try:
            mixer.music.load(str(BASE_DIR / 'sounds' / 'background_song.mp3'))
            mixer.music.play(-1)
        except (pygame.error, OSError) as error:
            print(f'No se pudo reproducir la musica: {error}')

        # Cada funcion retorna al mismo bucle; no se llama main() recursivamente.
        def volver_al_menu():
            return True

        def initGame():
            return jugar(window)

        def initPuntaje():
            return MenuPuntajes(back_mtd=volver_al_menu, ventana=window).ejecutar()

        def initAbout():
            return MenuAcercaDe(back_mtd=volver_al_menu, ventana=window).ejecutar()

        menu = MenuPrincipal(initGame, initPuntaje, initAbout, ventana=window)
        while True:
            if not menu.menu_principal():
                break
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
