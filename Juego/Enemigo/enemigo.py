import pygame
import random

#Enemigo simple que solo se mueve y causa daño al tocarlo
class Enemigo:
    def __init__(self, animaciones, pos_x, pos_y):
        self.animaciones = animaciones
        self.animacion_actual = self.animaciones["idle"][0]
        self.contador_pasos = 0
        self.index_actual = 0
        self.rectangulo_principal = self.animacion_actual.get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.estoy_muerto = False
        if random.randint(0,1) == 0:
            self.velocidad = 1
        else:
            self.velocidad = -1


    def animar(self):
        self.contador_pasos += 1
        if self.contador_pasos >= 5:
            self.index_actual = (self.index_actual + 1)
            self.contador_pasos = 0
            if self.index_actual == len(self.animaciones["idle"]):
                self.index_actual = 0

        self.animacion_actual = self.animaciones["idle"][self.index_actual]


    def moverse(self, plataformas):
    #Se mueve hasta chocar con algo y cambiar de direccion
        for plataforma in plataformas:
            if self.rectangulo_principal.colliderect(plataforma.lista_rectangulos[2]): #Choque con Izquierda
                self.velocidad *= -1
            elif self.rectangulo_principal.colliderect(plataforma.lista_rectangulos[3]): #Choque con Derecha
                self.velocidad *= -1
        
        if (self.rectangulo_principal.x >= 
            (1216 - self.rectangulo_principal.width)):
            self.velocidad *= -1
        elif self.rectangulo_principal.x <= 0:
            self.velocidad *= -1


        self.rectangulo_principal.x += self.velocidad
        self.animar()


    def chequear_colisones_proyectil(self, proyectiles):
        for proyectil in proyectiles:
            if self.rectangulo_principal.colliderect(proyectil.rectangulo_principal):
                self.estoy_muerto = True


    def obtener_animacion_actual(self):
        return self.animacion_actual
    

    def obtener_posicion_x(self):
        return self.rectangulo_principal.x
    

    def obtener_posicion_y(self):
        return self.rectangulo_principal.y


    def obtener_rectangulo_principal(self):
        return self.rectangulo_principal