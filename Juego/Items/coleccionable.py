import pygame
#Item coleccionable del juego, da puntos
class Coleccionable:
    def __init__(self, tipo, pos_x, pos_y):
        if tipo == "coleccionable":
            textura = (f"Assets/Imagenes/Items/pata_carne.png")
        else:
            textura = (f"Assets/Imagenes/Items/cura.png")
        self.textura = pygame.image.load(textura)
        self.textura = pygame.transform.scale(self.textura, (16, 16))
        self.rectangulo_principal = self.textura.get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.contador_pasos = 0
        self.index_actual = 0
        self.tipo = tipo

    def obtener_superficie(self):
        return self.textura


    def obtener_rectangulo_principal(self):
        return self.rectangulo_principal
    

    def obtener_posicion_x(self):
        return self.rectangulo_principal.x
    

    def obtener_posicion_y(self):
        return self.rectangulo_principal.y
    
    def obtener_tipo(self):
        return self.tipo