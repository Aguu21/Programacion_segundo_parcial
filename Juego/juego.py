import pygame
import sys
import json
import os
import sqlite3
import re
from pygame.locals import *
from Juego.Protagonista.protagonista import *
from Juego.Plataforma.plataforma import *
from Juego.Items.coleccionable import *
from Juego.Enemigo.enemigo import *
from Juego.Enemigo.boss import *
from Juego.Proyectil.proyectil import *
from Juego.Proyectil.rayo import *
from Juego.Boton.boton_nivel import *
from Juego.Puerta.puerta import *

WIDTH = 1216
HEIGHT = 608
FPS = 60
DIR = "Assets/Imagenes/"

#Maneja los cambios de pantalla y la logica del juego
class Juego:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.reloj = pygame.time.Clock()
        self.pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Prehistoric Quest")
        self.debug = False
        self.situacion = "Inicio"
        with open('Data/Config/config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
        with open('Data/Niveles/lvl_puntuacion.json', 'r', encoding='utf-8') as file:
            self.lista_puntuacion = json.load(file)
        self.volumen_ambiental = config["ambiente"]
        self.volumen_sonidos = config["sonidos"]
        pygame.mixer.music.load("Assets/Sonidos/background_music.wav")
        self.click_sonido = pygame.mixer.Sound("Assets/Sonidos/click_sound.wav")

        self.sonidos = pygame.mixer.Channel(0)
        self.hanlder_musica()
        pygame.mixer.music.play(loops=-1)
        self.nivel_a_cargar = 0
        self.gano = None
        self.tiempo_ronda = 60

        self.centrar_objeto_pantalla = lambda x: (self.pantalla.get_width() - x.get_size()[0]) // 2 
        self.validar_input = lambda x: bool(re.match(r'^[A-Z]{1,3}$', x))


    def handler_tiempo(self):
        self.tiempo_ronda = pygame.time.get_ticks() // 1000 + 60


    def hanlder_musica(self):
    #Cambia los volumenes a los marcados
        pygame.mixer.music.set_volume(self.volumen_ambiental)  
        self.sonidos.set_volume(self.volumen_sonidos)


    def run_query(self, query:str, parameters = ()):
    #Envia querys a la db
        with sqlite3.connect("Data/DB/db.db") as conn:
            cursor= conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result


    def cargar(self):
    #Maneja las pantallas
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
            elif self.situacion == "Puntaje":
                self.puntajes()
            self.handler_tiempo()
            pygame.display.update()


    def menu_inicio(self):
    #Pantalla de inicio, con start y config
        fuente_pixel = pygame.font.Font("Assets/Fuentes/upheavtt.ttf", 100)
        texto_titulo = fuente_pixel.render("PREHISTORIC QUEST", True, (255, 255, 255))

        background = pygame.image.load(f"{DIR}background_menu.jpg")
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
        start_rect.x = 200

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
                    self.sonidos.play(self.click_sonido)
                    self.situacion = "Selector"
                    run = False
            elif options_rect.collidepoint(pygame.mouse.get_pos()):
                options_boton = option_boton_press

                if pygame.mouse.get_pressed()[0]:
                    self.sonidos.play(self.click_sonido)
                    self.situacion = "Configuracion"
                    run = False
            else:
                start_boton = start_boton_unpress
                options_boton = option_boton_unpress


            self.pantalla.fill("Black")
            self.pantalla.blit(background, (0, 0))
        
            self.pantalla.blit(start_boton, (start_rect.x, start_rect.y))
            self.pantalla.blit(options_boton, (options_rect.x, options_rect.y))
            self.pantalla.blit(texto_titulo, (self.centrar_objeto_pantalla(texto_titulo), 150))
            pygame.display.update()


    def guardar_config(self):
    #Guarda la config en el json
        with open('Data/Config/config.json', 'w', 
                  encoding='utf-8') as file:
            json.dump(\
                {"ambiente":self.volumen_ambiental,
                 "sonidos":self.volumen_sonidos},
                file, indent=2)


    def guardar_puntuacion(self):
    #Guarda la puntuacion en el json
        with open('Data/Niveles/lvl_puntuacion.json', 'w',
                    encoding='utf-8') as file:
            json.dump(self.lista_puntuacion,
                      file, indent=2)


    def menu_config(self):
    #Pantalla de config de volumen
        fuente_pixel = pygame.font.Font("Assets/Fuentes/upheavtt.ttf", 70)

        background = pygame.image.load(f"{DIR}background_menu.jpg")
        icono_volumen = pygame.image.load(f"{DIR}sound_icon.png")
        barra_volumen = pygame.image.load(f"{DIR}sound_bar.png")
        bola_volumen = pygame.image.load(f"{DIR}sound_ball.png")
        
        titulo_ambiente = fuente_pixel.render("VOLUMEN AMBIENTE", True, (255, 255, 255))
        titulo_sonidos = fuente_pixel.render("VOLUMEN EFECTOS", True, (255, 255, 255))

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
        bola_ambiental_rect.y = 200

        bola_sonidos_rect.x = 150 + self.volumen_sonidos * 4.3 * 100
        bola_sonidos_rect.y = 440

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
                        #La funcion permite no pasarse de los limites de la barra
                        bola_sonidos_rect.x = min(max(evento.pos[0] - bola_volumen.get_width() // 2, 150),\
                                                   150 + barra_volumen.get_width() - bola_volumen.get_width())
                        self.volumen_sonidos = round((bola_sonidos_rect.x - 150) / 435, 2)
                        self.guardar_config()
                        self.hanlder_musica()
                            
                    elif arrastrar_ambiental:
                        bola_ambiental_rect.x = min(max(evento.pos[0] - bola_volumen.get_width() // 2, 150),\
                                                   150 + barra_volumen.get_width() - bola_volumen.get_width())
                        self.volumen_ambiental = round((bola_ambiental_rect.x - 150) / 435, 2)
                        self.guardar_config()
                        self.hanlder_musica()

            if boton_volver_rect.collidepoint(pygame.mouse.get_pos()):
                boton_volver = boton_volver_press
                if pygame.mouse.get_pressed()[0]:
                    self.sonidos.play(self.click_sonido)
                    self.situacion = "Inicio"
                    run = False      
            else:
                boton_volver = boton_volver_unpress

            self.pantalla.fill("White")
            self.pantalla.blit(background, (0, 0))

            self.pantalla.blit(titulo_ambiente, (25, 80))
            self.pantalla.blit(icono_volumen, (25, 180))
            self.pantalla.blit(barra_volumen, (150, 210))
            self.pantalla.blit(bola_volumen, (bola_ambiental_rect.x, bola_ambiental_rect.y))

            self.pantalla.blit(titulo_sonidos, (25, 320))
            self.pantalla.blit(icono_volumen, (25, 420))
            self.pantalla.blit(barra_volumen, (150, 450))
            self.pantalla.blit(bola_volumen, (bola_sonidos_rect.x, bola_sonidos_rect.y))
            
            self.pantalla.blit(boton_volver, (boton_volver_rect.x, boton_volver_rect.y))

            pygame.display.update()


    def selector_niveles(self):
    #Pantalla con botones para elegir el nivel, muestra su % cumplido
        lista_archivos = []

        fuente_pixel = pygame.font.Font("Assets/Fuentes/upheavtt.ttf", 38)
        texto_titulo = fuente_pixel.render("SELECTOR DE NIVELES", True, (255, 255, 255))
        background = pygame.image.load(f"{DIR}background_menu.jpg")

        boton_press = pygame.image.load(f"{DIR}boton_level_mark.png")
        boton_press = pygame.transform.scale(boton_press, (200, 250))
        for nombre_archivo in os.listdir("Data/Niveles"):
            if nombre_archivo != "lvl_puntuacion.json":
                lista_archivos.append(nombre_archivo)
        
        boton_volver_unpress = pygame.image.load(f"{DIR}boton_return_unpress.png")
        boton_volver_press = pygame.image.load(f"{DIR}boton_return_press.png")
        boton_volver_press = pygame.transform.scale(boton_volver_press, (250, 100))
        boton_volver_unpress = pygame.transform.scale(boton_volver_unpress, (250, 100))

        boton_volver = boton_volver_unpress
        
        boton_volver_rect = boton_volver.get_rect()
        boton_volver_rect.x = 950
        boton_volver_rect.y = 490

        lista_botones = []

        for item in self.lista_puntuacion:
            lista_botones.append(Boton_nivel(item["Nivel"],
                                            item["Nivel"] * 225 - 50,
                                            200,
                                            self.txt_a_bool(item["Habilitado"]),
                                            item["Conseguido"],
                                            item["Total"]))
        
        run = True
        while run:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()

            for boton in lista_botones:
                if ((boton.rectangulo_principal.collidepoint(
                    pygame.mouse.get_pos())) 
                and boton.obtener_habilitado()):
                        boton.cambiar_marcado(True)
                        if pygame.mouse.get_pressed()[0] and boton.obtener_marcado() == True:
                            self.sonidos.play(self.click_sonido)
                            self.situacion = "Juego"
                            self.nivel_a_cargar = boton.obtener_numero_nivel()
                            run = False      
                else:
                    boton.cambiar_marcado(False)
            
            if boton_volver_rect.collidepoint(pygame.mouse.get_pos()):
                boton_volver = boton_volver_press
                if pygame.mouse.get_pressed()[0]:
                    self.sonidos.play(self.click_sonido)
                    self.situacion = "Inicio"
                    run = False
            else:
                boton_volver = boton_volver_unpress

            self.pantalla.fill("Black")
            self.pantalla.blit(background, (0, 0))

            for boton in lista_botones:
                if boton.obtener_marcado():
                    self.pantalla.blit(boton_press,(
                                    boton.obtener_rectangulo_principal_x(), 
                                    boton.obtener_rectangulo_principal_y()))
                self.pantalla.blit(boton.textura, 
                                   (boton.obtener_rectangulo_principal_x(), 
                                    boton.obtener_rectangulo_principal_y()))
            
            self.pantalla.blit(boton_volver, (boton_volver_rect.x, boton_volver_rect.y))
            self.pantalla.blit(texto_titulo, (self.centrar_objeto_pantalla(texto_titulo), 100))

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


    def txt_a_bool(self, valor:str):
    #Convierte de txt a bool
        if valor.lower() == "true":
            return True
        else:
            return False


    def cargar_animaciones_enemigo(self): 
        animacion = {"idle":[]}
        for i in range(1, 5):
            img = pygame.image.load(f"{DIR}Cangrejo/cangrejo_mov_{i}.png")
            img = pygame.transform.scale(img, (32,32))
            animacion["idle"].append(img)
        return animacion
    

    def pantalla_final(self, gano):
    #Pantalla que se muestra sobre el final de un nivel.
    #Maneja ganar o perder
        mini_pantalla = pygame.image.load(f"{DIR}mark_empty.png")
        
        fuente_pixel = pygame.font.Font("Assets/Fuentes/upheavtt.ttf", 38)

        total = 0
        conseguido = 0

        for item in self.lista_puntuacion:
            if item["Nivel"] == self.nivel_a_cargar:
                total = item["Total"]
                conseguido = item["Conseguido"]

        texto_superficie = fuente_pixel.render(f"MEJOR SCORE: {conseguido}/{total}", True, (0,0,0))

        boton_siguiente = ""
        boton_siguiente_unpress = ""
        boton_siguiente_press = ""
        if gano:
            boton_siguiente_unpress = pygame.image.load(f"{DIR}boton_continue_unpress.png")
            boton_siguiente_press = pygame.image.load(f"{DIR}boton_continue_press.png")
        else:
            boton_siguiente_unpress = pygame.image.load(f"{DIR}boton_retry_unpress.png")
            boton_siguiente_press = pygame.image.load(f"{DIR}boton_retry_press.png")
        
        boton_siguiente_press = pygame.transform.scale(boton_siguiente_press, (250, 100))
        boton_siguiente_unpress = pygame.transform.scale(boton_siguiente_unpress, (250, 100))

        boton_siguiente_rect = boton_siguiente_press.get_rect()
        boton_siguiente_rect.x = ((self.pantalla.get_width() - 
                                  boton_siguiente_press.get_size()[0])) // 2 
        boton_siguiente_rect.y = 245

        boton_siguiente = boton_siguiente_unpress

        boton_volver_unpress = pygame.image.load(f"{DIR}boton_return_unpress.png")
        boton_volver_press = pygame.image.load(f"{DIR}boton_return_press.png")
        boton_volver_press = pygame.transform.scale(boton_volver_press, (250, 100))
        boton_volver_unpress = pygame.transform.scale(boton_volver_unpress, (250, 100))

        boton_volver = boton_volver_unpress
        
        boton_volver_rect = boton_volver.get_rect()
        boton_volver_rect.x = ((self.pantalla.get_width() - 
                                  boton_volver_press.get_size()[0])) // 2 
        boton_volver_rect.y = 360


        run = True
        while run:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if boton_siguiente_rect.collidepoint(pygame.mouse.get_pos()):
                boton_siguiente = boton_siguiente_press

                if pygame.mouse.get_pressed()[0]:
                    self.sonidos.play(self.click_sonido)
                    if self.nivel_a_cargar == 4:
                        self.situacion = "Puntaje"
                    else:
                        self.situacion = "Juego"
                        if gano:
                            self.nivel_a_cargar = self.nivel_a_cargar + 1
                    run = False
            elif boton_volver_rect.collidepoint(pygame.mouse.get_pos()):
                boton_volver = boton_volver_press
                if pygame.mouse.get_pressed()[0]:
                    self.sonidos.play(self.click_sonido)
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
            
            self.pantalla.blit(texto_superficie, ((self.pantalla.get_width() - texto_superficie.get_size()[0]) // 2, 175))
            pygame.display.update()          


    def nivel_juego(self):
    #Pantalla del juego, carga el nivel segun json y hace la logica

        animaciones_prota = self.cargar_animaciones_prota()
        animaciones_enemigo = self.cargar_animaciones_enemigo()
        animaciones_proyectil = self.cargar_animaciones_proyectil()
        
        with open(f'Data/Niveles/lvl{self.nivel_a_cargar}.json', 'r', encoding='utf-8') as file:
            lista_objetos = json.load(file)

        background = pygame.image.load(f"{DIR}background_lvl{self.nivel_a_cargar}.jpg")
        corazon = pygame.image.load(f"{DIR}corazon.png")

        corazon = pygame.transform.scale(corazon, (64, 64))
        lambda_vida_pos_x = lambda x: 10 + 80 * x

        mini_pantalla = pygame.image.load(f"{DIR}mark_empty.png")
        fuente_pixel = pygame.font.Font("Assets/Fuentes/upheavtt.ttf", 56)

        boton_volver_unpress = pygame.image.load(f"{DIR}boton_return_unpress.png")
        boton_volver_press = pygame.image.load(f"{DIR}boton_return_press.png")
        boton_volver_press = pygame.transform.scale(boton_volver_press, (250, 100))
        boton_volver_unpress = pygame.transform.scale(boton_volver_unpress, (250, 100))

        boton_volver = boton_volver_unpress
        
        boton_volver_rect = boton_volver.get_rect()
        boton_volver_rect.x = ((self.pantalla.get_width() - 
                                  boton_volver_press.get_size()[0])) // 2 
        boton_volver_rect.y = 360

        texto_superficie = fuente_pixel.render(f"PAUSA", True, (0,0,0))


        protagonista = ""
        plataformas = []
        enemigos = []
        items = []
        proyectiles = []
        puerta = ""
        puntuacion_total = 0
        boss = ""
        tiempo_pausa = 0

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
                enemigos.append(Enemigo(animaciones_enemigo,
                                        item["Pos_x"], 
                                        item["Pos_y"]))
            elif item["Objeto"] == "Coleccionable":
                items.append(Coleccionable(item["Tipo"],
                                           item["Pos_x"], 
                                           item["Pos_y"]))
            elif item["Objeto"] == "Puerta":
                puerta = Puerta(f'{DIR}{item["Path"]}',
                                item["Pos_x"],
                                item["Pos_y"])
            elif item["Objeto"] == "Boss":
                boss = Boss(item["Pos_x"], 
                            item["Pos_y"])
        run = True
        pausa = False

        salto_protagonista_sonido = pygame.mixer.Sound("Assets/Sonidos/salto_protagonista.wav")
        disparo_protagonista_sonido = pygame.mixer.Sound("Assets/Sonidos/disparo_protagonista.wav")
        morir_sonido = pygame.mixer.Sound("Assets/Sonidos/enemigo_muerte.wav")
        abrir_puerta_sonido = pygame.mixer.Sound("Assets/Sonidos/abrir_puerta.wav")

        while run:
            self.reloj.tick(FPS)
            timerReal = pygame.time.get_ticks() // 1000
            timer = self.tiempo_ronda - timerReal
            txt_timer = fuente_pixel.render(f"{timer}", True, (0,0,0))

            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_TAB:
                        self.debug = not self.debug
                    elif evento.key == pygame.K_ESCAPE or evento.key == pygame.K_p:
                        if pausa:
                            self.tiempo_ronda += tiempo_pausa - timer
                        else:
                            tiempo_pausa = timer
                        pausa = not pausa

                    if pausa == False:
                        if( evento.key == pygame.K_e and 
                           puerta != "" and
                           protagonista.obtener_puede_salir() and
                           puntuacion_total > 0):
                            
                            run = False
                            self.sonidos.play(abrir_puerta_sonido)
                            self.situacion = "Pantalla Final"
                            self.gano = True
                            puntuacion_total += self.puntaje_tiempo(timer) 
                            for item in self.lista_puntuacion:
                                if item["Nivel"] == self.nivel_a_cargar:
                                    if item["Conseguido"] <= puntuacion_total:
                                        item["Conseguido"] = puntuacion_total
                                if item["Nivel"] == self.nivel_a_cargar + 1:
                                    item["Habilitado"] = "True"
                                    break
                            self.guardar_puntuacion()
                        elif not protagonista.obtener_esta_saltando() and protagonista.tocando_piso \
                            and evento.key == pygame.K_UP:
                            self.sonidos.play(salto_protagonista_sonido)
                            protagonista.modificar_esta_saltando(True)
                            protagonista.salto = protagonista.altura_salto
                        elif evento.key == pygame.K_SPACE:
                            proyectiles.append(Proyectil(animaciones_proyectil,\
                                                    protagonista.rectangulo_principal.x,\
                                                    protagonista.rectangulo_principal.y, \
                                                    protagonista.donde_apunto))
                            self.sonidos.play(disparo_protagonista_sonido)
            
            if not pausa:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    protagonista.moverse(False, True, plataformas, True)
                elif keys[pygame.K_RIGHT]:
                    protagonista.moverse(True, False, plataformas, False)
                else:
                    protagonista.moverse(False, False, plataformas)
                
                if timer <= 0:
                    protagonista.vida = 0

                if protagonista.vida <= 0:
                    run = False
                    self.situacion = "Pantalla Final"
                    self.gano = False

                if boss != "" and boss.murio == True:
                    run = False
                    self.situacion = "Pantalla Final"
                    puntuacion_total += 1
                    self.gano = True
                    puntuacion_total += self.puntaje_tiempo(timer)
                    for item in self.lista_puntuacion:
                        if item["Nivel"] == self.nivel_a_cargar:
                            if item["Conseguido"] <= puntuacion_total:
                                item["Conseguido"] = puntuacion_total
                            break
                    self.guardar_puntuacion()

                self.pantalla.fill("Black")
                self.pantalla.blit(background, (0, 0))
                
                if puerta != "":
                    self.pantalla.blit(puerta.obtener_textura(), (puerta.obtener_posicion_x(), puerta.obtener_posicion_y()))

                self.pantalla.blit(protagonista.obtener_animacion_actual(), (protagonista.obtener_posicion_x(), protagonista.obtener_posicion_y()))

                for enemigo in enemigos:
                    if enemigo.estoy_muerto:
                        enemigos.remove(enemigo)
                        del enemigo
                        puntuacion_total += 1
                        self.sonidos.play(morir_sonido)
                    else:
                        enemigo.moverse(plataformas)
                        enemigo.chequear_colisones_proyectil(proyectiles)
                        self.pantalla.blit(enemigo.obtener_animacion_actual(), (enemigo.obtener_posicion_x(), enemigo.obtener_posicion_y()))
            
                puntuacion_total = protagonista.actualizar(enemigos, items, puerta, puntuacion_total, self.sonidos)
                
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
                        proyectil.actualizar_proyectil(enemigos, plataformas, boss)
                        self.pantalla.blit(proyectil.obtener_animacion_actual(), (proyectil.obtener_posicion_x(), proyectil.obtener_posicion_y()))
                
                for item in items:
                    self.pantalla.blit(item.obtener_superficie(), (item.obtener_posicion_x(), item.obtener_posicion_y()))

                for i in range(protagonista.vida):
                    self.pantalla.blit(corazon, (lambda_vida_pos_x(i), 10))
                if boss != "":
                    boss.que_hacer(proyectiles)
                    protagonista.colision_rayo(boss.rayo, self.sonidos)
                    self.pantalla.blit(boss.obtener_animacion_actual(), (boss.rectangulo_principal.x, boss.rectangulo_principal.y))
                    if boss.rayo.obtener_activo():
                        self.pantalla.blit(boss.rayo.obtener_animacion_actual(), (boss.rayo.rectangulo_principal.x, boss.rayo.rectangulo_principal.y))

                self.pantalla.blit(txt_timer, (1100, 0))
            else:
                if boton_volver_rect.collidepoint(pygame.mouse.get_pos()):
                    boton_volver = boton_volver_press
                    if pygame.mouse.get_pressed()[0]:
                        self.sonidos.play(self.click_sonido)
                        pausa = False
                        self.tiempo_ronda += tiempo_pausa - timer
                else:
                    boton_volver = boton_volver_unpress

                self.pantalla.blit(mini_pantalla, 
                               (((self.pantalla.get_width() - 
                                  mini_pantalla.get_size()[0])) // 2,
                                 100))
                self.pantalla.blit(boton_volver, (boton_volver_rect.x,
                                                  boton_volver_rect.y))
                self.pantalla.blit(texto_superficie, ((self.pantalla.get_width() - texto_superficie.get_size()[0]) // 2, 250))

                

            if self.debug:
                pygame.draw.rect(self.pantalla, (0,0,255), protagonista.obtener_rectangulo_principal(), 3)
                if puerta != "":
                    pygame.draw.rect(self.pantalla, (0,0,255), puerta.obtener_rectangulo_principal(), 3)
                if boss != "":
                    pygame.draw.rect(self.pantalla, (0,0,255), boss.obtener_rectangulo_principal(), 3)
                    pygame.draw.rect(self.pantalla, (0,0,255), boss.rayo.obtener_rectangulo_principal(), 3)
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


    def puntaje_tiempo(self, timer):
        if timer >= 30:
            return 3
        elif timer > 20 and timer < 30:
            return 2
        else:
            return 1


    def obtener_tabla(self, fuente_pixel):
    #Ejecuta un query y devuelve una lista de superficies de texto
        texto_puntajes = []
        query = """SELECT nombre, puntaje_conseguido FROM puntaje 
                ORDER BY puntaje_conseguido DESC
                LIMIT 5; """
        rows = self.run_query(query)
        for row in rows:
            texto_puntajes.append(fuente_pixel.render(
                f"{row[0]} :  {row[1]}", True, (255, 255, 255)))
        return texto_puntajes


    def agregar_puntaje(self, nombre, puntaje):
    #Ejecuta un query y guarda un nuevo puntaje
        query = """INSERT INTO puntaje (nombre, puntaje_conseguido)
                VALUES (?, ?)"""
        self.run_query(query, (nombre, puntaje))


    def puntajes(self):
    #Pantalla de puntajes, se ve el top y se puede ingresar el propio
        puntaje = 0
        for item in self.lista_puntuacion:
            puntaje += item["Conseguido"]
        fuente_pixel = pygame.font.Font("Assets/Fuentes/upheavtt.ttf", 38)
        texto_puntaje = fuente_pixel.render(f"PUNTAJE:         : {puntaje}", True, (255, 255, 255))
        texto_top = fuente_pixel.render("TOP", True, (0,0,0))

        texto_puntajes = self.obtener_tabla(fuente_pixel)
        
        boton_volver_unpress = pygame.image.load(f"{DIR}boton_return_unpress.png")
        boton_volver_press = pygame.image.load(f"{DIR}boton_return_press.png")
        boton_volver_press = pygame.transform.scale(boton_volver_press, (250, 100))
        boton_volver_unpress = pygame.transform.scale(boton_volver_unpress, (250, 100))

        boton_volver = boton_volver_unpress
        
        boton_volver_rect = boton_volver.get_rect()
        boton_volver_rect.x = 950
        boton_volver_rect.y = 490

        background = pygame.image.load(f"{DIR}background_menu.jpg")
        input_box = pygame.Rect(275, 102, 100, 32)
        respuesta_usuario = ""
        active = False
        ingresado = False
        color =  (0,0,0) 

        run = True
        while run:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if not ingresado:
                        if input_box.collidepoint(evento.pos):
                            active = not active
                        else:
                            active = False
                if evento.type == pygame.KEYDOWN:
                    if active and not ingresado:
                        if evento.key == pygame.K_RETURN:
                            ingresado = True
                            self.agregar_puntaje(respuesta_usuario, puntaje)
                            texto_puntajes = self.obtener_tabla(fuente_pixel)
                        elif evento.key == pygame.K_BACKSPACE:
                            respuesta_usuario = respuesta_usuario[:-1]
                        else:
                            try:
                                respuesta_usuario += evento.unicode
                            except UnicodeEncodeError as e:
                                print(f"Palabras no contempladas en unicode: {e}")
                            
                            respuesta_usuario = respuesta_usuario.upper()
                            if not self.validar_input(respuesta_usuario):
                                respuesta_usuario = respuesta_usuario[:-1]
            
            if boton_volver_rect.collidepoint(pygame.mouse.get_pos()):
                boton_volver = boton_volver_press
                if pygame.mouse.get_pressed()[0]:
                    self.sonidos.play(self.click_sonido)
                    self.situacion = "Selector"
                    run = False
            else:
                boton_volver = boton_volver_unpress

            self.pantalla.blit(background, (0, 0))
            txt_input = fuente_pixel.render(respuesta_usuario, True, (255,255,255))

            self.pantalla.blit(txt_input, (input_box.x + 5, input_box.y - 3)) #Input  

            self.pantalla.blit(texto_puntaje, (100, 100))
            self.pantalla.blit(texto_top, (self.centrar_objeto_pantalla(texto_top), 200))

            for i in range (0, len(texto_puntajes)):
                self.pantalla.blit(texto_puntajes[i], (self.centrar_objeto_pantalla(texto_puntajes[i]), 250 + 50 * i))

            self.pantalla.blit(boton_volver, (boton_volver_rect.x, boton_volver_rect.y))

            if active:
                color = (255,255,255)
            else:
                color = (0, 0, 0)
            
            pygame.draw.rect(self.pantalla, color, input_box, 2)


            pygame.display.update()         