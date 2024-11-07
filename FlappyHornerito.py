import pygame
import Constantes as const
import Sonido
import Puntaje
import Objeto as obj

import sys

from Personaje import Personaje 
from Personaje import Arboles
#limitador de fps (si se cambia se debe ajustar los parametros de velocidad y gravedad)
reloj = pygame.time.Clock()

pygame.init()

#creacion de pantalla y nombre
pantalla = pygame.display.set_mode((const.ancho_pantalla, const.largo_pantalla)) #creamos la pantalla
pygame.display.set_caption('Flappy Hornerito')



# fondo
fondo = pygame.image.load(const.fondo_imagen)
fondo_sonido=Sonido.Sonido(const.fondo_sonido)
fondo_sonido.reproducir()


#Crear personaje

flappy= Personaje(const.Posicion_x,const.Posicion_y,pantalla,const.imagenes_Hornero,const.Velocidad_personaje,const.Velocidad_personaje,const.gravedad)


bloque=Arboles([const.largo_pantalla-10,const.largo_pantalla-10],[120,const.ancho_pantalla-120],pantalla,
               [const.imagen_arbol_alto_superior,const.imagen_arbol_alto_inferior],const.Velocidad_personaje/2,2)

band=False



#crear clase puntaje
puntaje_sonido=Sonido.Sonido(const.puntaje_sonido)
puntaje=Puntaje.Puntaje(posicion=(const.ancho_pantalla-150,10))

caer=True

#Menu
boton_inicio = obj.Boton(const.ancho_pantalla/2-100, const.largo_pantalla/200 + 100, 200, 50, const.AZUL, 'Jugar')

while not const.run:
    
    pantalla.blit(fondo, (0,0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        boton_inicio.manejar_evento(evento)
        

    boton_inicio.dibujar(pantalla)
    

    pygame.display.update()

while const.run: #ciclo de ejecucion del juego
    fondo_sonido.reproducir()

    reloj.tick(const.fps)
    
    pantalla.blit(fondo, (0,0)) #cargamos el fondo


    flappy.dibujar()#dibuja al pj en la pantalla
    flappy.actualizar_sprite()# cambia el sprite
    if caer:
        flappy.caer()# actua la gravedad en el pj

    if band==False:
        bloque.desplazar(0)
        bloque.desplazar(1)
    
    bloque.dibujar()

    puntaje.dibujar(pantalla)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:# comando para cerrar la pantalla
            const.run = False

        if event.type==pygame.KEYDOWN:# detecta la presion del teclado
            
            if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and band==False:#detecta w o space
                flappy.salto()# activa el salto

    if (const.Posicion_x-const.Ancho_personaje/2-5<bloque.lista_obstaculos[1].pos_x+100<const.Posicion_x-const.Ancho_personaje/2):
        puntaje_sonido.reproducir()
        puntaje.aumentar()


    if pygame.sprite.spritecollide(flappy.movimientos, bloque.personaje, False):
        print("¡Colisión detectada con el obstáculo! ", flappy.movimientos.pos_x," ",bloque.lista_obstaculos[1].pos_x)
        if flappy.movimientos.rect.colliderect(bloque.lista_obstaculos[1]):
            if (bloque.lista_obstaculos[1].pos_x<302):
                flappy.movimientos.aceleracion=0
                caer=False
                flappy.movimientos.mover_arriba()

                print("moviendo")
        band=True

    pygame.display.update() #actualiza todo lo que esta en pantalla


pygame.quit()# Cierra el programa

