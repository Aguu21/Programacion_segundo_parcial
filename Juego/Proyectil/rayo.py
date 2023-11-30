import pygame

#Proyectil del boss
class Rayo:
    def __init__(self, pos_x, pos_y):
        blast = self.ajustar_tamano("Assets/Imagenes/Golem/blast_golem_", 9)
        self.animaciones = blast
        self.animacion_actual = self.animaciones[0]
        self.rectangulo_principal = self.animacion_actual.get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.contador_pasos = 0
        self.index_actual = 0
        self.velocidad = 5
        self.activo = False


    def ajustar_tamano(self, path, cant_frames):
        var = []
        for i in range(1,cant_frames):
            temp = pygame.image.load(f"{path}{i}.png")
            temp = pygame.transform.scale(temp, (temp.get_width() * 2, temp.get_height() * 2))
            var.append(temp)
        return var


    def animar(self):
        if self.activo:
            if self.index_actual == len(self.animaciones) - 1:
                return
            self.contador_pasos += 1
            if self.contador_pasos >= 5:
                self.index_actual = (self.index_actual + 1)
                self.contador_pasos = 0
            self.animacion_actual = self.animaciones[self.index_actual]
            self.rectangulo_principal = self.animacion_actual.get_rect()


    def reiniciar_animacion(self):
        self.index_actual = 0
        self.contador_pasos = 0
        self.animacion_actual = self.animaciones[0]
        self.rectangulo_principal = self.animacion_actual.get_rect()


    def obtener_animacion_actual(self):
        return self.animacion_actual
    

    def obtener_posicion_x(self):
        return self.rectangulo_principal.x


    def cambiar_posicion_x(self, pos_x):
        self.rectangulo_principal.x = pos_x


    def obtener_posicion_y(self):
        return self.rectangulo_principal.y


    def cambiar_posicion_y(self, pos_y):
        self.rectangulo_principal.y = pos_y


    def obtener_rectangulo_principal(self):
        return self.rectangulo_principal
    
    
    def obtener_activo(self):
        return self.activo
    

    def cambiar_activo(self, activo):
        self.activo = activo