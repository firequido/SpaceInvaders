"""Lectura y guardado comunes para la partida y el menu de puntajes."""
from pathlib import Path
import shutil
import sys


RECURSOS_DIR = Path(__file__).resolve().parent
BASE_DIR = Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else RECURSOS_DIR


def ruta_puntajes(archivo='puntajes.txt'):
    ruta = Path(archivo)
    if not ruta.is_absolute():
        ruta = BASE_DIR / ruta
    # La descarga del curso tiene una carpeta y un archivo con el mismo nombre.
    if ruta.is_dir():
        ruta = ruta / 'puntajes.txt'
    return ruta


def leer_registros(archivo='puntajes.txt'):
    ruta = ruta_puntajes(archivo)
    # Si se distribuye solo el exe, mostrar los registros iniciales incluidos.
    if not ruta.exists() and getattr(sys, 'frozen', False) and Path(archivo).name == 'puntajes.txt':
        ruta = RECURSOS_DIR / 'puntajes.txt'
    registros = []
    try:
        with ruta.open('r', encoding='utf-8-sig') as file:
            for numero, linea in enumerate(file, 1):
                if not linea.strip():
                    continue
                try:
                    nombre, puntuacion = linea.strip().rsplit(',', 1)
                    nombre = nombre.strip()
                    if not nombre:
                        raise ValueError('nombre vacio')
                    registros.append((nombre, int(puntuacion.strip())))
                except ValueError:
                    print(f'Se omitio la linea {numero}: formato de puntaje invalido.')
    except FileNotFoundError:
        print(f'No se encontro el archivo {ruta}')
    return sorted(registros, key=lambda registro: registro[1], reverse=True)[:5]


def guardar_registro(archivo, nombre, puntuacion):
    nombre = nombre.strip()
    if not nombre or any(caracter in nombre for caracter in ',\r\n'):
        raise ValueError('Escribe un nombre sin comas ni saltos de línea.')
    puntuacion = int(puntuacion)
    if puntuacion < 0:
        raise ValueError('El puntaje no puede ser negativo.')
    ruta = ruta_puntajes(archivo)
    if not ruta.exists() and getattr(sys, 'frozen', False) and Path(archivo).name == 'puntajes.txt':
        iniciales = RECURSOS_DIR / 'puntajes.txt'
        if iniciales.exists():
            shutil.copyfile(iniciales, ruta)
    # a+ conserva los registros y crea el archivo si aun no existe.
    with ruta.open('a+', encoding='utf-8') as file:
        file.seek(0)
        contenido = file.read()
        if contenido and not contenido.endswith('\n'):
            file.write('\n')
        file.write(f'{nombre}, {puntuacion}\n')
