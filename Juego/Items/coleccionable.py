class Coleccionable:
    def __init__(self, animaciones, pos_x, pos_y):
        self.animaciones = animaciones
        self.rectangulo_principal = self.animaciones[0].get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.contador_pasos = 0
        self.index_actual = 0
        self.animacion_actual = self.animaciones[0]

    def animar(self):
        self.contador_pasos += 1
        if self.contador_pasos >= 5:
            self.index_actual = (self.index_actual + 1) % 2
            self.contador_pasos = 0

        self.animacion_actual = self.animaciones[self.index_actual]

    def obtener_superficie(self):
        return self.animacion_actual

    def obtener_rectangulo_principal(self):
        return self.rectangulo_principal
    
    def obtener_posicion_x(self):
        return self.rectangulo_principal.x
    
    def obtener_posicion_y(self):
        return self.rectangulo_principal.y