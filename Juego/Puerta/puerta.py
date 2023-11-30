import pygame

#Permite finalizar un nivel normal
class Puerta:
    def __init__(self, path, pos_x, pos_y):
        self.textura = pygame.image.load(path)
        self.rectangulo_principal = self.textura.get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y


    def obtener_rectangulo_principal(self):
        return self.rectangulo_principal
    

    def obtener_posicion_x(self):
        return self.rectangulo_principal.x
    

    def obtener_posicion_y(self):
        return self.rectangulo_principal.y
    
    
    def obtener_textura(self):
        return self.textura