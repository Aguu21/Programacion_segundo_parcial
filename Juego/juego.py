import pygame
import sys
import json
import os
from pygame.locals import *
from Juego.Protagonista.protagonista import *
from Juego.Plataforma.plataforma import *
from Juego.Items.coleccionable import *
from Juego.Enemigo.enemigo import *
from Juego.Proyectil.proyectil import *
from Juego.Boton.boton_nivel import *
from Juego.Puerta.puerta import *


WIDTH = 1216
HEIGHT = 608
FPS = 60
DIR = "Assets/Imagenes/"

class Juego:

    def __init__(self):
        pygame.init()
        self.reloj = pygame.time.Clock()
        self.pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
        self.debug = False
        self.situacion = "Inicio"
        with open('Data/Config/config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
        with open('Data/Niveles/lvl_puntuacion.json', 'r', encoding='utf-8') as file:
            self.lista_puntuacion = json.load(file)
        self.volumen_ambiental = config["ambiente"]
        self.volumen_sonidos = config["sonidos"]
        self.nivel_a_cargar = 0
        self.gano = None

    
    def cargar(self):
        while True:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if self.situacion == "Inicio":
                self.menu_inicio()
            elif self.situacion == "Configuracion":
                self.menu_config()
            elif self.situacion == "Selector":
                self.selector_niveles()
            elif self.situacion == "Juego":
                self.nivel_juego()
            elif self.situacion == "Pantalla Final":
                self.pantalla_final(self.gano)
            print(self.nivel_a_cargar)
            pygame.display.update()

    def menu_inicio(self):
        start_boton_press = pygame.image.load(f"{DIR}start_boton_press.png")
        start_boton_unpress = pygame.image.load(f"{DIR}start_boton_unpress.png")
        start_boton_press = pygame.transform.scale(start_boton_press, (400, 100))
        start_boton_unpress = pygame.transform.scale(start_boton_unpress, (400, 100))

        option_boton_press = pygame.image.load(f"{DIR}boton_options_press.png")
        option_boton_unpress = pygame.image.load(f"{DIR}boton_options_unpress.png")
        option_boton_press = pygame.transform.scale(option_boton_press, (450, 100))
        option_boton_unpress = pygame.transform.scale(option_boton_unpress, (450, 100))

        start_boton = start_boton_press
        start_rect = start_boton.get_rect()
        start_rect.y = 450
        start_rect.x = 100

        options_boton = option_boton_press
        options_rect = options_boton.get_rect()
        options_rect.x = 650
        options_rect.y = 450

        run = True

        while run:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if start_rect.collidepoint(pygame.mouse.get_pos()):
                start_boton = start_boton_press

                if pygame.mouse.get_pressed()[0]:
                    self.situacion = "Selector"
                    run = False
            elif options_rect.collidepoint(pygame.mouse.get_pos()):
                options_boton = option_boton_press

                if pygame.mouse.get_pressed()[0]:
                    self.situacion = "Configuracion"
                    run = False
            else:
                start_boton = start_boton_unpress
                options_boton = option_boton_unpress


            self.pantalla.fill("Black")
        
            self.pantalla.blit(start_boton, (start_rect.x, start_rect.y))
            self.pantalla.blit(options_boton, (options_rect.x, options_rect.y))
            pygame.display.update()

    def guardar_config(self):
        with open('Data/Config/config.json', 'w', encoding='utf-8') as file:
            json.dump(\
                {"ambiente":self.volumen_ambiental,
                 "sonidos":self.volumen_sonidos},
                file, indent=2)

    def menu_config(self):
        icono_volumen = pygame.image.load(f"{DIR}sound_icon.png")
        barra_volumen = pygame.image.load(f"{DIR}sound_bar.png")
        bola_volumen = pygame.image.load(f"{DIR}sound_ball.png")
        
        boton_volver_unpress = pygame.image.load(f"{DIR}boton_return_unpress.png")
        boton_volver_press = pygame.image.load(f"{DIR}boton_return_press.png")
        boton_volver_press = pygame.transform.scale(boton_volver_press, (450, 100))
        boton_volver_unpress = pygame.transform.scale(boton_volver_unpress, (450, 100))

        boton_volver = boton_volver_unpress
        
        boton_volver_rect = boton_volver.get_rect()
        boton_volver_rect.x = 730
        boton_volver_rect.y = 310

        icono_volumen = pygame.transform.scale(icono_volumen, (100, 100))
        barra_volumen = pygame.transform.scale(barra_volumen, (500, 50))
        bola_volumen = pygame.transform.scale(bola_volumen, (65, 65))

        bola_ambiental_rect = bola_volumen.get_rect()
        bola_sonidos_rect = bola_volumen.get_rect()

        bola_ambiental_rect.x = 150 + self.volumen_ambiental * 4.3 * 100
        bola_ambiental_rect.y = 220

        bola_sonidos_rect.x = 150 + self.volumen_sonidos * 4.3 * 100
        bola_sonidos_rect.y = 420

        arrastrar_ambiental = False
        arrastrar_sonido = False
        
        run = True
        while run:
            eventos = pygame.event.get()
            for evento in eventos:
            
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if bola_ambiental_rect.collidepoint(evento.pos):
                        arrastrar_ambiental = True
                    elif bola_sonidos_rect.collidepoint(evento.pos):
                        arrastrar_sonido = True

                if evento.type == pygame.MOUSEBUTTONUP:
                    arrastrar_ambiental = False
                    arrastrar_sonido = False

                if evento.type == pygame.MOUSEMOTION:
                    if arrastrar_sonido:
                        # Update slider handle position based on mouse movement
                        bola_sonidos_rect.x = min(max(evento.pos[0] - bola_volumen.get_width() // 2, 150),\
                                                   150 + barra_volumen.get_width() - bola_volumen.get_width())
                        self.volumen_sonidos = round((bola_sonidos_rect.x - 150) / 435, 2)
                        self.guardar_config()
                            
                    elif arrastrar_ambiental:
                        bola_ambiental_rect.x = min(max(evento.pos[0] - bola_volumen.get_width() // 2, 150),\
                                                   150 + barra_volumen.get_width() - bola_volumen.get_width())
                        self.volumen_ambiental = round((bola_ambiental_rect.x - 150) / 435, 2)
                        self.guardar_config()

            if boton_volver_rect.collidepoint(pygame.mouse.get_pos()):
                boton_volver = boton_volver_press
                if pygame.mouse.get_pressed()[0]:
                    self.situacion = "Inicio"
                    run = False      
            else:
                boton_volver = boton_volver_unpress

            self.pantalla.fill("White")

            self.pantalla.blit(icono_volumen, (25, 200))
            self.pantalla.blit(barra_volumen, (150, 230))
            self.pantalla.blit(bola_volumen, (bola_ambiental_rect.x, bola_ambiental_rect.y))

            self.pantalla.blit(icono_volumen, (25, 400))
            self.pantalla.blit(barra_volumen, (150, 430))
            self.pantalla.blit(bola_volumen, (bola_sonidos_rect.x, bola_sonidos_rect.y))
            
            self.pantalla.blit(boton_volver, (boton_volver_rect.x, boton_volver_rect.y))

            pygame.display.update()

    def selector_niveles(self):
        lista_archivos = []
        boton_press = pygame.image.load(f"{DIR}boton_level_mark.png")
        boton_press = pygame.transform.scale(boton_press, (200, 250))
        for nombre_archivo in os.listdir("Data/Niveles"):
            if nombre_archivo != "lvl_puntuacion.json":
                lista_archivos.append(nombre_archivo)
        
        lista_botones = []

        for item in self.lista_puntuacion:
            lista_botones.append(Boton_nivel(item["Nivel"],
                                            item["Nivel"] * 225 - 170,
                                            200,
                                            item["Habilitado"],
                                            item["Conseguido"],
                                            item["Total"]))
        
        run = True
        while run:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()

            for boton in lista_botones:
                if (boton.rectangulo_principal.collidepoint(
                    pygame.mouse.get_pos()) 
                and boton.obtener_habilitado() == True):
                    
                    boton.cambiar_marcado(True)
                    if pygame.mouse.get_pressed()[0] and boton.obtener_marcado() == True:
                        self.situacion = "Juego"
                        self.nivel_a_cargar = boton.obtener_numero_nivel()
                        run = False      
                else:
                    boton.cambiar_marcado(False)

            self.pantalla.fill("Black")


            for boton in lista_botones:
                if boton.obtener_marcado():
                    self.pantalla.blit(boton_press,(
                                    boton.obtener_rectangulo_principal_x(), 
                                    boton.obtener_rectangulo_principal_y()))
                self.pantalla.blit(boton.textura, 
                                   (boton.obtener_rectangulo_principal_x(), 
                                    boton.obtener_rectangulo_principal_y()))
                
                
            pygame.display.update()          
    
    def cargar_animaciones_prota(self):
        animaciones_prota = {
            "idle": [
                pygame.image.load(f"{DIR}prota_quieto.png"), 
                pygame.image.load(f"{DIR}prota_quieto.png")],
            "moving_left": [
                pygame.transform.flip(pygame.image.load(
                    f"{DIR}prota_derecha_1.png"), True, False),
                pygame.transform.flip(pygame.image.load(
                    f"{DIR}prota_derecha_2.png"), True, False)],
            "moving_right": [
                pygame.image.load(f"{DIR}prota_derecha_1.png"), 
                pygame.image.load(f"{DIR}prota_derecha_2.png")],
            "jumping_right": [
                pygame.image.load(f"{DIR}prota_salta_derecha.png"),
                pygame.image.load(f"{DIR}prota_salta_derecha.png")],
            "jumping_left": [\
                pygame.transform.flip(pygame.image.load(
                    f"{DIR}prota_salta_derecha.png"), True, False),
                pygame.transform.flip(pygame.image.load(
                    f"{DIR}prota_salta_derecha.png"), True, False)]
        }
        for item in animaciones_prota:
            for i in range (len(animaciones_prota[item])):
                animaciones_prota[item][i] = pygame.transform.scale(
                    animaciones_prota[item][i],
                    (animaciones_prota[item][i].get_width()*2, 
                    animaciones_prota[item][i].get_height()*2))
        
        return animaciones_prota
                       
    def cargar_animaciones_proyectil(self):
        proyectil = [
            pygame.image.load(f"{DIR}roca_1.png"),
            pygame.image.load(f"{DIR}roca_2.png"),
            pygame.image.load(f"{DIR}roca_3.png"),
            pygame.image.load(f"{DIR}roca_4.png")]
        return proyectil

    def cargar_animaciones_item(self, path):
        animaciones_item = [
            pygame.image.load(f"{DIR}{path}"),
            pygame.image.load(f"{DIR}{path}")]
        for item in animaciones_item:
            item = pygame.transform.scale(item,
                                        (item.get_width() * 2,
                                        item.get_height() * 2))
        return animaciones_item

    def txt_a_bool(self, valor:str):
        if valor == "True":
            return True
        else:
            return False

    def pantalla_final(self, gano):
        mini_pantalla = pygame.image.load(f"{DIR}mark_empty.png")
        
        boton_siguiente = ""
        boton_siguiente_unpress = ""
        boton_siguiente_press = ""
        if gano:
            boton_siguiente_unpress = pygame.image.load(f"{DIR}boton_continue_unpress.png")
            boton_siguiente_press = pygame.image.load(f"{DIR}boton_continue_press.png")
        else:
            boton_siguiente_unpress = pygame.image.load(f"{DIR}boton_retry_unpress")
            boton_siguiente_press = pygame.image.load(f"{DIR}boton_retry_press")
        
        boton_siguiente_press = pygame.transform.scale(boton_siguiente_press, (250, 100))
        boton_siguiente_unpress = pygame.transform.scale(boton_siguiente_unpress, (250, 100))

        boton_siguiente_rect = boton_siguiente_press.get_rect()
        boton_siguiente_rect.x = ((self.pantalla.get_width() - 
                                  boton_siguiente_press.get_size()[0])) // 2 
        boton_siguiente_rect.y = 245

        boton_volver_unpress = pygame.image.load(f"{DIR}boton_return_unpress.png")
        boton_volver_press = pygame.image.load(f"{DIR}boton_return_press.png")
        boton_volver_press = pygame.transform.scale(boton_volver_press, (250, 100))
        boton_volver_unpress = pygame.transform.scale(boton_volver_unpress, (250, 100))

        boton_volver = boton_volver_unpress
        
        boton_volver_rect = boton_volver.get_rect()
        boton_volver_rect.x = ((self.pantalla.get_width() - 
                                  boton_volver_press.get_size()[0])) // 2 
        boton_volver_rect.y = 360

        puntuacion_total = 0

        run = True
        while run:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if boton_siguiente_rect.collidepoint(pygame.mouse.get_pos()):
                boton_siguiente = boton_siguiente_press

                if pygame.mouse.get_pressed()[0]:
                    self.situacion = "Juego"
                    if gano:
                        self.nivel_a_cargar = self.nivel_a_cargar + 1
                    run = False
            elif boton_volver_rect.collidepoint(pygame.mouse.get_pos()):
                boton_volver = boton_volver_press
                if pygame.mouse.get_pressed()[0]:
                    self.situacion = "Selector"
                    run = False
            else:
                boton_siguiente = boton_siguiente_unpress
                boton_volver = boton_volver_unpress

            self.pantalla.blit(mini_pantalla, 
                               (((self.pantalla.get_width() - 
                                  mini_pantalla.get_size()[0])) // 2,
                                 100))
            
            self.pantalla.blit(boton_siguiente, (boton_siguiente_rect.x,
                                                  boton_siguiente_rect.y))
            
            self.pantalla.blit(boton_volver, (boton_volver_rect.x,
                                                  boton_volver_rect.y))
            pygame.display.update()          

    def nivel_juego(self):

        animaciones_prota = self.cargar_animaciones_prota()
        animaciones_item = self.cargar_animaciones_item("pata_carne.png")
        animaciones_proyectil = self.cargar_animaciones_proyectil()
        
        with open(f'Data/Niveles/lvl{self.nivel_a_cargar}.json', 'r', encoding='utf-8') as file:
            lista_objetos = json.load(file)

        protagonista = ""
        plataformas = []
        enemigos = []
        items = []
        proyectiles = []
        puerta = ""

        for item in lista_objetos:
            if item["Objeto"] == "Protagonista":
                protagonista = Personaje(animaciones_prota, 
                                         item["Velocidad"], 
                                         item["Pos_x"], 
                                         item["Pos_y"])
            
            elif item["Objeto"] == "Plataforma":
                plataformas.append(Plataforma(item["Pos_x"],
                                              item["Pos_y"], 
                                              item["Alto"], 
                                              item["Ancho"], 
                                              f'{DIR}{item["Path"]}', 
                                              self.txt_a_bool(item["Movible"]), 
                                              self.txt_a_bool(item["H_V"]), 
                                              item["Cant_mov"]))
            elif item["Objeto"] == "Enemigo":
                enemigos.append(Enemigo(animaciones_prota,
                                        item["Pos_x"], 
                                        item["Pos_y"]))
            elif item["Objeto"] == "Coleccionable":
                items.append(Coleccionable(animaciones_item,
                                           item["Pos_x"],
                                           item["Pos_y"]))
            elif item["Objeto"] == "Puerta":
                puerta = Puerta(f'{DIR}{item["Path"]}',
                                item["Pos_x"],
                                item["Pos_y"])
        run = True
        while run:
            self.reloj.tick(FPS)
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_TAB:
                        self.debug = not self.debug
                    elif evento.key == pygame.K_e and protagonista.obtener_puede_salir():
                        run = False
                        self.situacion = "Pantalla Final"
                        self.gano = True
                        for item in self.lista_puntuacion:
                            if item["Nivel"] == self.nivel_a_cargar + 1:
                                item["Habilitado"] = "True"
                                break
                        with open('Data/Niveles/lvl_puntuaciones.json', 'w', encoding='utf-8') as file:
                            json.dump(\
                                self.lista_puntuacion,
                                file, indent=2)
                        #Actualizar puntaje
                        pass
                    elif not protagonista.obtener_esta_saltando() and protagonista.tocando_piso \
                        and evento.key == pygame.K_UP:
                        protagonista.modificar_esta_saltando(True)
                        protagonista.salto = protagonista.altura_salto
                    elif evento.key == pygame.K_SPACE:
                        proyectiles.append(Proyectil(animaciones_proyectil,\
                                                protagonista.rectangulo_principal.x,\
                                                protagonista.rectangulo_principal.y, \
                                                protagonista.donde_apunto))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                protagonista.moverse(False, True, plataformas, True)
            elif keys[pygame.K_RIGHT]:
                protagonista.moverse(True, False, plataformas, False)
            else:
                protagonista.moverse(False, False, plataformas)
            

            self.pantalla.fill("Black")
            
            
            self.pantalla.blit(puerta.obtener_textura(), (puerta.obtener_posicion_x(), puerta.obtener_posicion_y()))

            self.pantalla.blit(protagonista.obtener_animacion_actual(), (protagonista.obtener_posicion_x(), protagonista.obtener_posicion_y()))

            for enemigo in enemigos:
                if enemigo.estoy_muerto:
                    enemigos.remove(enemigo)
                    del enemigo
                else:
                    enemigo.moverse(plataformas)
                    enemigo.chequear_colisones_proyectil(proyectiles)
                    self.pantalla.blit(enemigo.obtener_animacion_actual(), (enemigo.obtener_posicion_x(), enemigo.obtener_posicion_y()))
        
            protagonista.actualizar(enemigos, items, puerta)
            
            for plataforma in plataformas:
                if plataforma.movible:
                    plataforma.mover_plataforma()
                self.pantalla.blit(plataforma.obtener_superficie(), (plataforma.obtener_posicion_x(), plataforma.obtener_posicion_y()))
            
            protagonista.aplicar_gravedad(plataformas)


            for proyectil in proyectiles:
                if proyectil.estoy_muerto:
                    proyectiles.remove(proyectil)
                    del proyectil
                else:
                    proyectil.actualizar_proyectil(enemigos, plataformas)
                    self.pantalla.blit(proyectil.obtener_animacion_actual(), (proyectil.obtener_posicion_x(), proyectil.obtener_posicion_y()))
            
            for item in items:
                self.pantalla.blit(item.obtener_superficie(), (item.obtener_posicion_x(), item.obtener_posicion_y()))


            if self.debug:
                pygame.draw.rect(self.pantalla, (0,0,255), protagonista.obtener_rectangulo_principal(), 3)
                pygame.draw.rect(self.pantalla, (0,0,255), puerta.obtener_rectangulo_principal(), 3)
                for proyectil in proyectiles:
                    pygame.draw.rect(self.pantalla, (0,0,255), proyectil.obtener_rectangulo_principal(), 3)
                for plataforma in plataformas:
                    for i in range(len(plataforma.lista_rectangulos)):
                        pygame.draw.rect(self.pantalla, (0,255,0), plataforma.lista_rectangulos[i], 3)
                    #pygame.draw.rect(self.pantalla, (0,0,255), plataforma.obtener_rectangulo_principal(), 3)
                for enemigo in enemigos:
                    pygame.draw.rect(self.pantalla, (0,0,255), enemigo.obtener_rectangulo_principal(), 3)
                for item in items:
                    pygame.draw.rect(self.pantalla, (0,0,255), item.obtener_rectangulo_principal(), 3)
                
            
            pygame.display.update()