import pygame, sys
from pygame.locals import *

ancho = 1024
alto = 768

class Personajes(pygame.sprite.Sprite):
        """Clase de los personajes"""
        
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.imagenPersonaje = pygame.image.load("Imagenes\Personaje.png")
                self.rect = self.imagenPersonaje.get_rect()
                self.rect.centerx = ancho/2
                self.rect.centery = alto - 50
                self.vida = 100
                self.maxVida=100
                self.velocidad = 5
                self.listaDisparo = []
                self.listaCuracion=[]
                self.ultimoDisparo = 0
                self.ultimaCuracion = 0
                self.direccion = 'N' #Direcciones: Norte(N), Sur(S), Este(E), Oeste(O)
                self.Fuente = pygame.font.SysFont("Arial", 30)
                self.cooldownCuracion=0
        
        def dibujar(self, superficie):
                superficie.blit(self.imagenPersonaje, self.rect)
                self.mostrarVida(superficie)
                self.mostrarCoolCuracion(superficie)
                
        def mostrarVida(self, superficie):
                texto_vida = self.Fuente.render("Vida: " + str(self.vida), 0, (255, 0, 0))
                superficie.blit(texto_vida, (5, 5))
                
        def mostrarCoolCuracion(self,superficie):
                texto_curacion = self.Fuente.render("Curacion: " + str(self.cooldownCuracion), 0, (255, 0, 0))
                superficie.blit(texto_curacion, (150, 5))
                
        def moverIzquierda(self):
                self.rect.centerx -= self.velocidad
                self.__movimiento()
                self.direccion = 'O'
                #limite de pantalla()

        def moverDerecha(self):
                self.rect.centerx += self.velocidad
                self.__movimiento()
                self.direccion = 'E'
                #limite de pantalla()
        def moverArriba(self):
                self.rect.centery -= self.velocidad
                self.__movimiento()
                self.direccion = 'N'
		#limite pantalla()
        def moverAbajo(self):
                self.rect.centery += self.velocidad
                self.__movimiento()
                self.direccion = 'S'
                #limite patalla()
                
        def __movimiento(self):
                if self.sigueVivo():
                    if self.rect.bottom > alto:
                        self.rect.bottom = alto
                    elif self.rect.top < 0:
                        self.rect.top = 0
                    elif self.rect.left < 0:
                        self.rect.left = 0
                    elif self.rect.right > ancho:
                        self.rect.right = ancho
                
        def sigueVivo(self):
                if self.vida > 1:
                        return True
                else:
                        return False
                
        def aumentarVida(self,tiempo):
                aumento=Curacion(self.rect.centerx,self.rect.centery,self.vida)

                if tiempo >= self.ultimaCuracion + aumento.tiempoReutilizacion:
                        self.vida+=aumento.cantAumento
                        if self.vida>= self.maxVida:
                                self.vida=self.maxVida
                                self.listaCuracion.append(aumento)        
                                self.ultimaCuracion=tiempo
                                self.cooldownCuracion=aumento.tiempoReutilizacion
                                
                """el if lo quise hacer en el metodo aumentar de la clase Curacion pero no me salio"""
        def recibirDanio(self, danio):
                self.vida -= danio
                
        def disparar(self, tiempo):
                disparo = Disparo(self.rect.centerx, self.rect.centery, self.direccion)
                
                
                if tiempo >= self.ultimoDisparo + disparo.tiempoReutilizacion:
                        self.listaDisparo.append(disparo)
                        self.ultimoDisparo = tiempo
        
                


                
class Curacion(pygame.sprite.Sprite):
        """Clase Curacion y aumento de Velocidad"""

        def __init__(self, posX, posY, vida):
                pygame.sprite.Sprite.__init__(self)
                self.imagenCuracion = pygame.image.load("Imagenes\Enemigo1.png")
                self.rect = self.imagenCuracion.get_rect()
                self.rect.centerx = posX
                self.rect.centery = posY
                self.cantAumento = 10
                self.auxiliar=0
                self.tiempoReutilizacion=5
              
        """def aumentar(self):"""
        
        def dibujar(self, superficie):
                superficie.blit(self.imagenCuracion,self.rect)

                     
                     
                     
                     

        
                
class Disparo(pygame.sprite.Sprite):
        """Clase del disparo"""
        
        def __init__(self, posX, posY, direccion):
                pygame.sprite.Sprite.__init__(self)
                self.imagenDisparo = pygame.image.load("Imagenes\Disparo.png")
                self.rect = self.imagenDisparo.get_rect()
                self.rect.centerx = posX
                self.rect.centery = posY
                self.danio = 10
                self.velocidad = 6
                self.direccion = direccion
                self.tiempoReutilizacion = 1
                
        def trayectoria(self):
                if self.direccion == 'N':
                        self.rect.centery -= self.velocidad
                elif self.direccion == 'S':
                        self.rect.centery += self.velocidad
                elif self.direccion == 'E':
                        self.rect.centerx += self.velocidad
                elif self.direccion == 'O':
                        self.rect.centerx -= self.velocidad
                
        def dibujar(self, superficie):
                superficie.blit(self.imagenDisparo, self.rect)



class Enemigo(pygame.sprite.Sprite):
        
        """Clase de los enemigos basicos"""

        def __init__(self, posX, posY):
                pygame.sprite.Sprite.__init__(self)
                self.vida = 100
                self.Fuente = pygame.font.SysFont("Arial", 20)
                self.direccion = 'S'
                self.imagenEnemigo = pygame.image.load("Imagenes/Enemigo1.png")
                self.rect = self.imagenEnemigo.get_rect()
                self.rect.centerx = posX
                self.rect.top = posY
                self.velocidad = 2
                self.listaDisparo = []
                self.ultimoDisparo = 0

        def dibujar(self, superficie):
                superficie.blit(self.imagenEnemigo, self.rect)
                self.mostrarVida(superficie)

        def mostrarVida(self, superficie):
                texto_vida = self.Fuente.render("Vida: " + str(self.vida), 0, (255, 0, 0))
                superficie.blit(texto_vida, (self.rect.left +5, self.rect.bottom ))

        def disparar(self, tiempo):
                disparo = Disparo(self.rect.centerx, self.rect.centery, self.direccion)
                if tiempo > self.ultimoDisparo + disparo.tiempoReutilizacion:
                        self.listaDisparo.append(disparo)
                        self.ultimoDisparo = tiempo

        def sigueVivo(self):
                if self.vida > 0:
                        return True
                else:
                        return False

        def moverIzquierda(self):
                self.rect.centerx -= self.velocidad
                self.__movimiento()
                self.direccion = 'O'
                #limite de pantalla()

        def moverDerecha(self):
                self.rect.centerx += self.velocidad
                self.__movimiento()
                self.direccion = 'E'
                #limite de pantalla()
        def moverArriba(self):
                self.rect.centery -= self.velocidad
                self.__movimiento()
                self.direccion = 'N'
		#limite pantalla()
        def moverAbajo(self):
                self.rect.centery += self.velocidad
                self.__movimiento()
                self.direccion = 'S'
                #limite patalla()
                
        def __movimiento(self):
                if self.sigueVivo():
                    if self.rect.bottom > alto:
                        self.rect.bottom = alto
                    elif self.rect.top < 0:
                        self.rect.top = 0
                    elif self.rect.left < 0:
                        self.rect.left = 0
                    elif self.rect.right > ancho:
                        self.rect.right = ancho

        def mover(self, jugador):
                if abs(self.rect.centerx - jugador.rect.centerx) >= abs(self.rect.centery - jugador.rect.centery):
                        if self.rect.centerx > jugador.rect.centerx:
                                self.moverIzquierda()
                        elif self.rect.centerx < jugador.rect.centerx:
                                self.moverDerecha()
                else:
                        if self.rect.centery > jugador.rect.centery:
                                self.moverArriba()
                        elif self.rect.centery < jugador.rect.centery:
                                self.moverAbajo()

                
        def recibirDanio(self, danio):
                self.vida -= danio

        def enRango(self, jugador):
                return ((enemigo.rect.left < jugador.rect.centerx and enemigo.rect.right > jugador.rect.centerx and (self.direccion == 'S' or self.direccion == 'N')) or
                        (enemigo.rect.top < jugador.rect.centery and enemigo.rect.bottom > jugador.rect.centery and (self.direccion == 'E' or self.direccion == 'O')))
        
                        
        
"""""""""""""""""""""""""""MAIN"""""""""""""""""""""""""""""""""        
pygame.init()
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Juego")
pygame.key.set_repeat(True)

imagenFondo = pygame.image.load("Imagenes\Fondo.jpg")
ventana.blit(imagenFondo, (0, 0))

jugador = Personajes()
enemigo = Enemigo(ancho/2, 1)
tiempo = 1

while jugador.sigueVivo():
        tiempo_milesimas = pygame.time.get_ticks()/1000
        if tiempo == tiempo_milesimas:
                print tiempo
                tiempo += 1
                
                if jugador.cooldownCuracion>0:    
                        print jugador.cooldownCuracion
                        jugador.cooldownCuracion-=1
                        
        """if not jugador.sigueVivo():
                Fuente = pygame.font.SysFont("Arial", 20)
                texto_fin = Fuente.render("Perdiste" , 0, (0, 0, 0))
                ventana.blit(texto_fin, (ancho/2, alto/2))"""
        for evento in pygame.event.get():
                if evento.type == QUIT: #agregar la salida al menu y guardado de score
                        pygame.quit()
                        sys.exit()
                if evento.type == pygame.KEYDOWN:
                        if evento.key == K_LEFT:
                                jugador.moverIzquierda()
                        elif evento.key == K_RIGHT:
                                jugador.moverDerecha()
                        elif evento.key == K_UP:
                                jugador.moverArriba()
                        elif evento.key == K_DOWN:
                                jugador.moverAbajo()
                        elif evento.key == K_SPACE:
                                jugador.disparar(tiempo)
                if evento.type == pygame.KEYUP:
                        if evento.key == K_1:
                                jugador.aumentarVida(tiempo)

        ventana.blit(imagenFondo, (0, 0))
        jugador.dibujar(ventana)
        
        
        if enemigo.sigueVivo():
                enemigo.mover(jugador)
                enemigo.dibujar(ventana)
                if enemigo.enRango(jugador):
                        enemigo.disparar(tiempo)

        if len(jugador.listaDisparo) > 0: #aca recorro la lista de disparos pendientes del jugador
                for x in jugador.listaDisparo:
                        x.dibujar(ventana)
                        x.trayectoria()
                        if x.rect.colliderect(enemigo.rect):
                                enemigo.recibirDanio(x.danio)
                                jugador.listaDisparo.remove(x)
                        if x.rect.top < -20:
                                jugador.listaDisparo.remove(x)
                        elif x.rect.bottom > alto+20:
                                jugador.listaDisparo.remove(x)
                        elif x.rect.left < -20:
                                jugador.listaDisparo.remove(x)
                        elif x.rect.right > ancho+20:
                                jugador.listaDisparo.remove(x)

        if len(enemigo.listaDisparo) > 0:
                for y in enemigo.listaDisparo:
                        y.dibujar(ventana)
                        y.trayectoria()
                        if y.rect.colliderect(jugador.rect):
                                jugador.recibirDanio(y.danio)
                                enemigo.listaDisparo.remove(y)
                        if y.rect.top < -20:
                                enemigo.listaDisparo.remove(y)
                        elif y.rect.bottom > alto+20:
                                enemigo.listaDisparo.remove(y)
                        elif y.rect.left < -20:
                                enemigo.listaDisparo.remove(y)
                        elif y.rect.right > ancho+20:
                                enemigo.listaDisparo.remove(y)
                                
        pygame.display.update()
        
pygame.quit()
sys.exit()
