import pygame
import random,sys
from pygame.locals import *

''''conclusion: pause() is not working(seems it triggers nothing, and 
as a result, get_busy() is not working with pause() )
'''

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

def end():
    pygame.quit()
    sys.exit()

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
pygame.mixer.music.set_volume(0.5)
paused=False
while True:  #game loop when the game is playing.    
    if not pygame.mixer.music.get_busy(): #is not playing
        print("Not playing")
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            end();       
        elif event.type == KEYUP:    
            if event.key == K_ESCAPE:
                end()   
            elif event.key == K_s:    
                print("pause.")
                #pygame.mixer.music.pause() 
                pygame.mixer.music.stop()

    
    screen.fill(bgColor)
    pygame.display.flip() 
    clock.tick(40)         
            
            
            
            