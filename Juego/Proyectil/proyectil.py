import pygame

#Proyectil disparado por el jugador
class Proyectil:
    def __init__(self, animaciones, pos_x, pos_y, derecha):
        self.animaciones = animaciones
        self.animacion_actual = self.animaciones[0]
        self.rectangulo_principal = self.animacion_actual.get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.direccion = derecha
        self.contador_pasos = 0
        self.index_actual = 0
        self.velocidad = 5
        self.estoy_muerto = False


    def animar(self):
        self.contador_pasos += 1
        if self.contador_pasos >= 5:
            self.index_actual = (self.index_actual + 1)
            if self.index_actual == len(self.animaciones):
                self.index_actual = 0
            self.contador_pasos = 0

        self.animacion_actual = self.animaciones[self.index_actual]


    def moverse(self):
    #Segun la direccion avanza
        self.animar()
        if self.direccion:
            self.rectangulo_principal.x += self.velocidad
        else:
            self.rectangulo_principal.x -= self.velocidad
        

    def chequear_colison(self, enemigos, plataformas, boss):
        for enemigo in enemigos:
            if self.rectangulo_principal.colliderect(enemigo.rectangulo_principal):
                self.estoy_muerto = True
                enemigo.estoy_muerto = True
                return
        for plataforma in plataformas:
            if self.rectangulo_principal.colliderect(plataforma.lista_rectangulos[3]):
                self.estoy_muerto = True
                return
            elif self.rectangulo_principal.colliderect(plataforma.lista_rectangulos[2]):
                self.estoy_muerto = True
                return
        
        if boss != "":
            if self.rectangulo_principal.colliderect(boss.rectangulo_principal):
                self.estoy_muerto = True
                return

        if self.rectangulo_principal.x > 1216 or self.rectangulo_principal.x < 0:
            self.estoy_muerto = True


    def actualizar_proyectil(self, enemigos, plataformas, boss):
    #Genera los cambios necesarios por iteracion
        self.moverse()
        self.chequear_colison(enemigos, plataformas, boss)


    def obtener_animacion_actual(self):
        return self.animacion_actual
    

    def obtener_posicion_x(self):
        return self.rectangulo_principal.x
    

    def obtener_posicion_y(self):
        return self.rectangulo_principal.y


    def obtener_rectangulo_principal(self):
        return self.rectangulo_principal