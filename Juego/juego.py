import pygame
import sys
import json
from pygame.locals import *
from Juego.Protagonista.protagonista import *
from Juego.Plataforma.plataforma import *
from Juego.Items.coleccionable import *
from Juego.Enemigo.enemigo import *
from Juego.Proyectil.proyectil import *

WIDTH = 1216
HEIGHT = 608
FPS = 60
DIR = "Assets/"

class Juego:

    def __init__(self):
        pygame.init()
        self.reloj = pygame.time.Clock()
        self.pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
        self.debug = False
        self.situacion = "Inicio"
        with open('Data/Config/config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
        self.volumen_ambiental = config["ambiente"]
        self.volumen_sonidos = config["sonidos"]
        self.nivel_a_cargar = 0

    
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
            pygame.display.update()

    def menu_inicio(self):
        start_boton_press = pygame.image.load(f"{DIR}Imagenes/start_boton_press.png")
        start_boton_unpress = pygame.image.load(f"{DIR}Imagenes/start_boton_unpress.png")
        start_boton_press = pygame.transform.scale(start_boton_press, (400, 100))
        start_boton_unpress = pygame.transform.scale(start_boton_unpress, (400, 100))

        option_boton_press = pygame.image.load(f"{DIR}Imagenes/boton_options_press.png")
        option_boton_unpress = pygame.image.load(f"{DIR}Imagenes/boton_options_unpress.png")
        option_boton_press = pygame.transform.scale(option_boton_press, (450, 100))
        option_boton_unpress = pygame.transform.scale(option_boton_unpress, (450, 100))

        start_boton = start_boton_press
        start_rect = start_boton.get_rect()
        start_rect.y = 300
        start_rect.x = (self.pantalla.get_width() - start_boton.get_size()[0]) // 2

        options_boton = option_boton_press
        options_rect = options_boton.get_rect()
        options_rect.x = (self.pantalla.get_width() - options_boton.get_size()[0]) // 2
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
                    self.situacion = "Juego"
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
        icono_volumen = pygame.image.load(f"{DIR}Imagenes/sound_icon.png")
        barra_volumen = pygame.image.load(f"{DIR}Imagenes/sound_bar.png")
        bola_volumen = pygame.image.load(f"{DIR}Imagenes/sound_ball.png")
        
        boton_volver_unpress = pygame.image.load(f"{DIR}Imagenes/boton_return_unpress.png")
        boton_volver_press = pygame.image.load(f"{DIR}Imagenes/boton_return_press.png")
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
        
        #For para lista de botones de cada nivel
        #Cada icono de nivel tiene que ser apretable,
        #Abajo va a tener un tick, un ~ o una cruz segun cuantos items agarraste
        #Los que no se pueden avanzar porque el anterior no se termino, no cambia la skin al pasar el mouse
        #Boton de return
        
        run = True
        while run:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            
    def nivel_juego(self):
        animaciones_prota = {
            "idle": [pygame.image.load(f"{DIR}Imagenes/prota_quieto.png"), pygame.image.load(f"{DIR}Imagenes/prota_quieto.png")],
            "moving_left": [\
                pygame.transform.flip(pygame.image.load(f"{DIR}Imagenes/prota_derecha_1.png"), True, False),
                pygame.transform.flip(pygame.image.load(f"{DIR}Imagenes/prota_derecha_2.png"), True, False)],
            "moving_right": [pygame.image.load(f"{DIR}Imagenes/prota_derecha_1.png"), pygame.image.load(f"{DIR}Imagenes/prota_derecha_2.png")],
            "jumping_right": [pygame.image.load(f"{DIR}Imagenes/prota_salta_derecha.png"), pygame.image.load(f"{DIR}Imagenes/prota_salta_derecha.png")],
            "jumping_left": [\
                pygame.transform.flip(pygame.image.load(f"{DIR}Imagenes/prota_salta_derecha.png"), True, False),
                pygame.transform.flip(pygame.image.load(f"{DIR}Imagenes/prota_salta_derecha.png"), True, False)]
        } 
        for item in animaciones_prota:
            for i in range (len(animaciones_prota[item])):
                animaciones_prota[item][i] = pygame.transform.scale(animaciones_prota[item][i], \
                                                          (animaciones_prota[item][i].get_width()*2, animaciones_prota[item][i].get_height()*2))
        
        
        
        
        plataformas = [Plataforma(0,576,1,38,f"{DIR}Imagenes/piso_pasto.png"), #Piso 0,576 
                       Plataforma(160, 512, 1, 3, f"{DIR}Imagenes/piso_pasto.png"), #Plataforma 1
                       Plataforma(288, 412, 1, 3, f"{DIR}Imagenes/piso_pasto.png"),#Plataforma 2
                       Plataforma(160, 320, 1, 3, f"{DIR}Imagenes/piso_pasto.png"),
                       Plataforma(288, 224, 1, 3, f"{DIR}Imagenes/piso_pasto.png"),
                       Plataforma(480, 224, 1, 5, f"{DIR}Imagenes/piso_pasto.png", True, True, 7),
                       Plataforma(512, 544, 1, 1, f"{DIR}Imagenes/piso_pasto.png"),
                       Plataforma(988, 224, 1, 4, f"{DIR}Imagenes/piso_pasto.png", True, False, 9),
                       Plataforma(1148, 544, 1, 1,f"{DIR}Imagenes/piso_pasto.png")
                       ] 
        

        protagonista = Personaje(animaciones_prota, 5, 100, 200)
        
        proyectiles = []

        enemigos = [Enemigo(animaciones_prota, 544, 546)]
        
        animaciones_item = [pygame.image.load(f"{DIR}Imagenes/pata_carne.png"),pygame.image.load(f"{DIR}Imagenes/pata_carne.png")]
        animaciones_proyectil = [pygame.image.load(f"{DIR}Imagenes/roca_1.png"),pygame.image.load(f"{DIR}Imagenes/roca_2.png"),
                            pygame.image.load(f"{DIR}Imagenes/roca_3.png"),pygame.image.load(f"{DIR}Imagenes/roca_4.png")]
        for item in animaciones_item:
            item = pygame.transform.scale(item, (item.get_width()*2, item.get_height()*2))
        items = [Coleccionable(animaciones_item, 200,300), Coleccionable(animaciones_item, 200, 470)]
        for i in range(5):
            for x in range(5):
                items.append(Coleccionable(animaciones_item, x * 15 + 300, i * 15 + 300))


        while True:
            self.reloj.tick(FPS)
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_TAB:
                        self.debug = not self.debug
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
            
            

            self.pantalla.blit(protagonista.obtener_animacion_actual(), (protagonista.obtener_posicion_x(), protagonista.obtener_posicion_y()))

            for enemigo in enemigos:
                if enemigo.estoy_muerto:
                    enemigos.remove(enemigo)
                    del enemigo
                else:
                    enemigo.moverse(plataformas)
                    enemigo.chequear_colisones_proyectil(proyectiles)
                    self.pantalla.blit(enemigo.obtener_animacion_actual(), (enemigo.obtener_posicion_x(), enemigo.obtener_posicion_y()))
                
            protagonista.animar()
            protagonista.colision_enemigos(enemigos)
            protagonista.colision_items(items)
            protagonista.mover_rectangulos()
            

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