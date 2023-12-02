import pygame

#Guarda la informacion necesaria del nivel asi como la del boton
class Boton_nivel:
    def __init__(self, numero_nivel, pos_x, pos_y, habilitado, puntuacion_obtenida, puntuacion_max):
        self.numero_nivel = numero_nivel
        self.textura = pygame.image.load(f"Assets/Imagenes/boton_level_empty.png")
        self.habilitado = habilitado
        self.marcado = False
        self.definir_imagen(puntuacion_obtenida, puntuacion_max)
        self.textura = pygame.transform.scale(self.textura, (200, 250))
        self.rectangulo_principal = self.textura.get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y


    def definir_imagen(self, puntuacion_conseguida, puntuacion_maxima):
        #Segun el puntaje esta nunca revisado, completo o incompleto
        if puntuacion_conseguida == -1:
            self.textura = pygame.image.load(f"Assets/Imagenes/boton_level_empty.png")
        elif puntuacion_conseguida >= puntuacion_maxima:
            self.textura = pygame.image.load(f"Assets/Imagenes/boton_level_check.png")
        else:
            self.textura = pygame.image.load(f"Assets/Imagenes/boton_level_block.png")


    def obtener_marcado(self):
        return self.marcado
    

    def cambiar_marcado(self, cambio):
        self.marcado = cambio


    def obtener_numero_nivel(self):
        return self.numero_nivel
    

    def obtener_habilitado(self):
        return self.habilitado


    def obtener_rectangulo_principal_x(self):
        return self.rectangulo_principal.x
    
    
    def obtener_rectangulo_principal_y(self):
        return self.rectangulo_principal.y
    