"""Crea el ejecutable para Windows con imagenes, sonidos e icono."""
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    proyecto = Path(__file__).resolve().parent
    destino = proyecto.parent / 'ejecutable'
    subprocess.run([
        sys.executable, '-m', 'PyInstaller', '--noconfirm', '--onefile', '--windowed',
        '--name', 'SpaceInvaders', '--icon', str(proyecto / 'title_icon.ico'),
        '--add-data', f'{proyecto / "img"}:img',
        '--add-data', f'{proyecto / "sounds"}:sounds',
        '--add-data', f'{proyecto / "puntajes.txt"}:.',
        '--distpath', str(destino), '--workpath', str(proyecto / 'build'),
        '--specpath', str(proyecto / 'build'), str(proyecto / 'main.py'),
    ], check=True, cwd=proyecto)
    destino.mkdir(exist_ok=True)
    # No reemplazar los resultados de alguien que ya haya usado el ejecutable.
    if not (destino / 'puntajes.txt').exists():
        shutil.copy2(proyecto / 'puntajes.txt', destino / 'puntajes.txt')


if __name__ == '__main__':
    main()
