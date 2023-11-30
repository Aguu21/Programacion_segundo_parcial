import pygame
import random
from Juego.Proyectil.rayo import *

#Jefe final del juego, lanza un rayo al atacar
class Boss:
    def __init__(self, pos_x, pos_y):
        idle = self.ajustar_tamano("Assets/Imagenes/Golem/golem_idle_", 5)
        laser = self.ajustar_tamano("Assets/Imagenes/Golem/golem_laser_", 9)
        muerte = self.ajustar_tamano("Assets/Imagenes/Golem/golem_muerte_", 15)
        
        self.animaciones = {
            "idle": idle,
            "laser": laser,
            "muerte": muerte
            }
        
        self.animacion_actual = self.animaciones["idle"][0]
        self.nombre_animacion_actual = "idle"
        self.contador_pasos = 0
        self.index_actual = 0
        self.rectangulo_principal = self.animacion_actual.get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.rayo = Rayo(self.rectangulo_principal.x + 100, self.rectangulo_principal.y)
        self.que_hago = "Elegir"
        self.murio = False
        self.posicion_y = pos_y
        self.vida = 10


    def ajustar_tamano(self, path, cant_frames):
        var = []
        for i in range(1,cant_frames):
            temp = pygame.image.load(f"{path}{i}.png")
            temp = pygame.transform.scale(temp, (240, 160))
            var.append(temp)
        return var


    def mover_rayo(self):
    #Mueve el rayo de ataque para que coincida con la cabeza
        self.rayo.cambiar_posicion_y(self.rectangulo_principal.y + 15)
        self.rayo.cambiar_posicion_x(self.rectangulo_principal.x + 100)


    def animar(self):
    #Rota la animacion
        if self.rayo.obtener_activo:
            self.rayo.animar()
        self.contador_pasos += 1
        if self.contador_pasos >= 10:
            self.index_actual = (self.index_actual + 1)
            if self.index_actual == len(self.animaciones[self.nombre_animacion_actual]):
                self.index_actual = 0
            self.contador_pasos = 0
        
        self.animacion_actual = self.animaciones[self.nombre_animacion_actual][self.index_actual]
        if self.animacion_actual == self.animaciones["muerte"][len(self.animaciones["muerte"]) - 1]:
            self.murio = True


    def chequear_colisones_proyectil(self, proyectiles):
        if self.vida == 0:
            self.que_hago = "Morir"
            return
        for proyectil in proyectiles:
            if self.rectangulo_principal.colliderect(proyectil.rectangulo_principal):
                self.vida -= 1


    def que_hacer(self, proyectiles):
    #Define que ejecutar segun los estados posibles
        self.animar()
        self.chequear_colisones_proyectil(proyectiles)
        rand = -1
        if self.que_hago == "Elegir":
            rand = random.randint(1, 150)
            if rand == 100:
                self.que_hago = "Moverme"
                posicion_extra = random.randint(1,5) * 50
                direccion = random.randint(0, 1)
                while (((self.posicion_y + posicion_extra) > 400 and direccion == 1 ) or
                       ((self.posicion_y - posicion_extra) < 200 and direccion == 0 )):
                    posicion_extra = random.randint(1,5) * 50
                    direccion = random.randint(0,1)
                if direccion == 1:
                    self.posicion_y += posicion_extra
                else:
                    self.posicion_y -= posicion_extra

        elif self.que_hago == "Moverme":
            if self.rectangulo_principal.y < self.posicion_y:
                self.rectangulo_principal.y += 2
            elif self.rectangulo_principal.y > self.posicion_y:
                self.rectangulo_principal.y -= 2
            else:
                self.que_hago = "Disparar"

        elif self.que_hago == "Disparar":
            self.index_actual = 0
            self.contador_pasos = 0
            self.nombre_animacion_actual = "laser"
            self.que_hago = "Disparando"
            self.rayo.cambiar_activo(True)

        elif self.que_hago == "Disparando":
            if (self.index_actual == len(self.animaciones["laser"]) - 1):
                self.index_actual = 0
                self.contador_pasos = 0
                self.nombre_animacion_actual = "idle"
                self.que_hago = "Elegir"
                self.rayo.cambiar_activo(False)
                self.rayo.reiniciar_animacion()
                
        elif self.que_hago == "Morir":
            self.nombre_animacion_actual = "muerte"
            self.rayo.cambiar_activo(False)
            self.rectangulo_principal.y = 415

        self.mover_rayo()


    def obtener_animacion_actual(self):
        return self.animacion_actual
    

    def obtener_posicion_x(self):
        return self.rectangulo_principal.x
    
    
    def obtener_posicion_y(self):
        return self.rectangulo_principal.y


    def obtener_rectangulo_principal(self):
        return self.rectangulo_principal