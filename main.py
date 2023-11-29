from Juego.juego import *

class main:
    '''Ejecuta el juego'''

    def __init__(self):
        self.Juego = Juego()

    def inicio(self):
        self.Juego.cargar()


if __name__ == '__main__':
    import pygame
    pygame.init()
    main = main()
    main.inicio()