import pygame 

class Plataforma():
    def __init__(self, pos_x, pos_y,\
                altura, ancho, \
                path, \
                movible = False, horizontal_vertical = False, cant_mov = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.textura = pygame.image.load(path)
        self.superficie, self.rectangulo_principal = self.crear_plataforma(ancho, altura)
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.movible = movible
        self.direccion = True
        self.horizontal_vertical = horizontal_vertical
        self.cant_mov = cant_mov
        self.lista_rectangulos = self.crear_partes_plataforma()
        self.acomodar_rectangulos()

    def crear_plataforma(self, largo, alto):
        rect_textura = self.textura.get_rect()

        superficie_completa = pygame.Surface((rect_textura.width * largo, rect_textura.height * alto))

        rectangulo_completo = superficie_completa.get_rect()

        for y in range(alto):
            for x in range(largo):
                superficie_completa.blit(self.textura, (x * rect_textura.width, y * rect_textura.height))
        
        return superficie_completa, rectangulo_completo
    
    def crear_partes_plataforma(self):
        
        top_rect = pygame.Rect(self.rectangulo_principal.topleft, \
                                (self.rectangulo_principal.width, \
                                self.rectangulo_principal.height - self.rectangulo_principal.height // 5))
        bottom_rect = pygame.Rect(self.rectangulo_principal.bottomleft,\
                                (self.rectangulo_principal.width,\
                                self.rectangulo_principal.height // 5))

        left_rect = pygame.Rect(self.rectangulo_principal.topleft, (15, self.rectangulo_principal.height // 2))
        right_rect = pygame.Rect(self.rectangulo_principal.topright, (15, self.rectangulo_principal.height // 2))
        
        lista_rectangulos = [top_rect, bottom_rect, left_rect, right_rect]
        
        return lista_rectangulos

    def acomodar_rectangulos(self):
        for i in range(0,4):
            self.lista_rectangulos[i].y = self.rectangulo_principal.y
            self.lista_rectangulos[i].x = self.rectangulo_principal.x
            if i == 1:
                self.lista_rectangulos[i].y += (self.rectangulo_principal.height // 5) * 4
            elif i == 2:
                self.lista_rectangulos[i].y += self.rectangulo_principal.height // 4
            elif i == 3:
                self.lista_rectangulos[i].x += self.rectangulo_principal.width - 15
                self.lista_rectangulos[i].y += self.rectangulo_principal.height // 4

    def mover_plataforma(self):
        velocidad = 2
        if self.horizontal_vertical:
            if self.direccion:
                self.rectangulo_principal.x += velocidad
                if (self.rectangulo_principal.x >= (self.pos_x + 32 * self.cant_mov)):
                    self.direccion = not self.direccion
            else:
                self.rectangulo_principal.x -= velocidad
                if self.rectangulo_principal.x <= self.pos_x:
                    self.direccion = not self.direccion
        else:
            if self.direccion:
                self.rectangulo_principal.y += velocidad
                if self.rectangulo_principal.y >= (self.pos_y + 32 * self.cant_mov):
                    self.direccion = not self.direccion
            else:
                self.rectangulo_principal.y -= velocidad
                if self.rectangulo_principal.y <= self.pos_y:
                    self.direccion = not self.direccion
        self.acomodar_rectangulos()


    def obtener_superficie(self):
        return self.superficie

    def obtener_rectangulo_principal(self):
        return self.rectangulo_principal
    
    def obtener_posicion_x(self):
        return self.rectangulo_principal.x
    
    def obtener_posicion_y(self):
        return self.rectangulo_principal.y