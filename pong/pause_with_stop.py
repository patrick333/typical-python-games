import pygame
import random,sys
from pygame.locals import *

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)
purple = (159, 0, 197)

bgColor= (0,   0,   0)
textColor = (250, 250, 255)

width = 600 
height = 600

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, textColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

pygame.init()
screen = pygame.display.set_mode([width,height])

pygame.mixer.music.load('background.mid')  
font = pygame.font.SysFont(None, 48)

clock = pygame.time.Clock()

pygame.mixer.music.play(-1, 0.0)
paused=False
while True:  #game loop when the game is playing.    
    if not pygame.mixer.music.get_busy(): #is not playing
        #print("Not playing")
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            end();       
        elif event.type == KEYUP:    
            if event.key == K_ESCAPE:
                end()   
            elif event.key == K_s:    
                paused=not paused  

    # --- Game logic
    if paused==True:
        if pygame.mixer.music.get_busy(): #playing
            pygame.mixer.music.stop()
            #pygame.mixer.music.pause()    
            print("paused")
        drawText('GAME Paused', font, screen, (width / 3), (height / 3))
        drawText('Press S to continue...', font, screen, (width / 3) - 80, (height / 3) + 50)
        pygame.display.update()       
        continue
    else:
        if not pygame.mixer.music.get_busy():  #get_busy=True: playing. Here, not playing. 
            print("music paused, now unpause it.")
            pygame.mixer.music.play(-1, 0.0)
    
    screen.fill(bgColor)
    pygame.display.flip() 
    clock.tick(40)         
            
            
            
            