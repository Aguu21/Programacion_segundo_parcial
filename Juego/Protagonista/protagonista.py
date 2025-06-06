import pygame

#El jugador lo controla, salta, camina, dispara y entra por puertas
class Personaje:
    def __init__(self, animaciones, velocidad, pos_x, pos_y):
        self.animaciones = animaciones
        self.velocidad = velocidad
        self.salto = 10
        self.esta_saltando = False
        self.esta_derecha = False
        self.esta_izquierda = False
        self.tocando_piso = False
        self.contador_pasos = 0
        self.animacion_actual = self.animaciones["idle"][self.contador_pasos]
        self.index_actual = 0
        self.rectangulo_principal = self.animacion_actual.get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.velocidad_gravedad = 4 #Se pega al techo si cambio esto
        self.altura_salto = 15  
        self.puede_salir = False
        self.cooldown = 0
        self.vida = 3
        self.donde_apunto = True
        self.lista_rectangulos = self.crear_partes_protagonista()
    

    def crear_partes_protagonista(self):
    #Crea partes del protagonista, no se llego a ausar
        top_rect = pygame.Rect(self.rectangulo_principal.topleft, (self.rectangulo_principal.width, 15))
        bottom_rect = pygame.Rect(self.rectangulo_principal.bottomleft, (self.rectangulo_principal.width, 15))
        left_rect = pygame.Rect(self.rectangulo_principal.topleft, (15, self.rectangulo_principal.height))
        right_rect = pygame.Rect(self.rectangulo_principal.topright, (15, self.rectangulo_principal.height))
        lista_rectangulos = [top_rect, bottom_rect, left_rect, right_rect]
        return lista_rectangulos


    def moverse(self, esta_derecha, esta_izquierda, plataformas, mov = None):
    #Permite el movimiento segun las colisiones
        for plataforma in plataformas:
            if self.rectangulo_principal.colliderect(plataforma.lista_rectangulos[3]):
                self.rectangulo_principal.x = plataforma.rectangulo_principal.x + plataforma.rectangulo_principal.width 
                return
            elif self.rectangulo_principal.colliderect(plataforma.lista_rectangulos[2]):
                self.rectangulo_principal.x = plataforma.rectangulo_principal.x - self.rectangulo_principal.width 
                return

        if (self.rectangulo_principal.x >= 
            (1216 - self.rectangulo_principal.width)):
            self.rectangulo_principal.x = 1216 - self.rectangulo_principal.width - 1
            return
        elif self.rectangulo_principal.x <= 0:
            self.rectangulo_principal.x = 1
            return


        self.esta_izquierda = esta_izquierda
        self.esta_derecha = esta_derecha

        if mov == True:
            self.rectangulo_principal.x -= self.velocidad
            self.donde_apunto = False
        elif mov == False:
            self.rectangulo_principal.x += self.velocidad
            self.donde_apunto = True
        

    def obtener_esta_saltando(self):
        return self.esta_saltando


    def modificar_esta_saltando(self, estado):
        self.esta_saltando = estado


    def mover_rectangulos(self):
    #Acomoda los rectangulos al moverse
        for i in range(0,4):
            self.lista_rectangulos[i].y = self.rectangulo_principal.y
            self.lista_rectangulos[i].x = self.rectangulo_principal.x
            if i == 1:
                self.lista_rectangulos[i].y += self.rectangulo_principal.height // 2
            elif i == 3:
                self.lista_rectangulos[i].x += self.rectangulo_principal.width // 2


    def aplicar_gravedad(self, plataformas):
    #Hace que el protagonista caia hasta encontrar una plataforma
        if self.rectangulo_principal.y >= 610:
            self.vida = 0
            return
        if self.esta_saltando:
            self.rectangulo_principal.y -= self.salto
            self.salto -= 1
            self.tocando_piso = False
        else:
            self.rectangulo_principal.y += self.velocidad_gravedad

        colisiono = False
        for plataforma in plataformas:
            if self.rectangulo_principal.colliderect(plataforma.lista_rectangulos[1]):
                self.rectangulo_principal.y = plataforma.rectangulo_principal.y + plataforma.rectangulo_principal.height
                self.esta_saltando = False

            elif self.rectangulo_principal.colliderect(plataforma.lista_rectangulos[0]):
                if plataforma.movible == True and plataforma.horizontal_vertical == False:
                    self.rectangulo_principal.y = plataforma.rectangulo_principal.y - self.rectangulo_principal.height
                    if plataforma.direccion: #Bajando
                        self.rectangulo_principal.y += 1
                    else: #Subiendo
                        self.rectangulo_principal.y -= 5
                else:
                    self.rectangulo_principal.y = plataforma.rectangulo_principal.y - self.rectangulo_principal.height
                colisiono = True
                self.tocando_piso = True
                self.esta_saltando = False
                break

        if colisiono:
            self.salto = 0
            self.esta_saltando = False
            

    def colision_items(self, items, puntuacion_total, canal_sonido):
        for item in items:
            if self.rectangulo_principal.colliderect(item.rectangulo_principal):
                if item.obtener_tipo() == "Vida":
                    self.vida += 1
                items.remove(item)
                del item 
                puntuacion_total += 1
                agarrar_sonido = pygame.mixer.Sound("Assets/Sonidos/agarrar_protagonista.wav")
                canal_sonido.play(agarrar_sonido)

        return puntuacion_total


    def colision_enemigos(self, enemigos, canal_sonido):
        for enemigo in enemigos:
            if self.rectangulo_principal.colliderect(enemigo.rectangulo_principal) and self.cooldown <= 0:
                self.vida -= 1
                self.cooldown = 60
                dano_sonido = pygame.mixer.Sound("Assets/Sonidos/dano_protagonista.wav")
                canal_sonido.play(dano_sonido)


    def colision_puerta(self, puerta):
        if puerta != "":
            if self.rectangulo_principal.colliderect(puerta.obtener_rectangulo_principal()):
                self.cambiar_puede_salir(True)
            else:
                self.cambiar_puede_salir(False)


    def colision_rayo(self, rayo, canal_sonido):
        if self.rectangulo_principal.colliderect(rayo.obtener_rectangulo_principal()) and self.cooldown <= 0:
            self.vida -= 1
            self.cooldown = 60
            dano_sonido = pygame.mixer.Sound("Assets/Sonidos/dano_protagonista.wav")
            canal_sonido.play(dano_sonido)


    def animar(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        self.contador_pasos += 1
        if self.contador_pasos >= 5:
            self.index_actual = (self.index_actual + 1) % 2
            self.contador_pasos = 0

        self.animacion_actual = self.animaciones["idle"][self.index_actual]
        if self.esta_izquierda:
            self.animacion_actual = self.animaciones["moving_left"][self.index_actual]
        elif self.esta_derecha:
            self.animacion_actual = self.animaciones["moving_right"][self.index_actual]
        elif self.esta_saltando:
            if self.donde_apunto:
                self.animacion_actual = self.animaciones["jumping_right"][self.index_actual]
            else:
                self.animacion_actual = self.animaciones["jumping_left"][self.index_actual]
    

    def actualizar(self, enemigos, items, puerta, puntuacion_total, canal_sonido):
    #Genera los cambios necesarios por iteracion
        self.animar()
        self.colision_enemigos(enemigos, canal_sonido)
        puntuacion = self.colision_items(items, puntuacion_total, canal_sonido)
        self.colision_puerta(puerta)
        self.mover_rectangulos()
        
        return puntuacion


    def obtener_animacion_actual(self):
        return self.animacion_actual
    

    def obtener_posicion_x(self):
        return self.rectangulo_principal.x
    

    def obtener_posicion_y(self):
        return self.rectangulo_principal.y


    def obtener_rectangulo_principal(self):
        return self.rectangulo_principal


    def obtener_puede_salir(self):
        return self.puede_salir
    
    
    def cambiar_puede_salir(self, cambio):
        self.puede_salir = cambio   