import pygame, os.path
from pygame.locals import *

class TranslucentSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, TranslucentSprite.container)
        #self.image = pygame.image.load(os.path.join('data', 'image.bmp'))
        self.image = pygame.image.load('basic_plane.png')
        self.image = self.image.convert()
        #self.image.set_colorkey(-1, RLEACCEL)
        self.image.set_colorkey((250,250,250))
        self.rect = self.image.get_rect()
        self.rect.center = (320,240)

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((200,200,250))
    #background.fill((50,50,50))
    clock = pygame.time.Clock()
    #transgroups = pygame.sprite.Group()
    #TranslucentSprite.container = transgroups
    
    #Here's the Translucency Code
    transsurface = pygame.display.set_mode(screen.get_size())
    transsurface = transsurface.convert(screen)
    transsurface.fill((255,0,255))
    transsurface.set_colorkey((255,0,255))
    transsurface.set_alpha(50)
    
    TranslucentSprite()
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
              return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
              return
        #transgroups.draw(transsurface)
        screen.blit(background,(0,0))
        #screen.blit(transsurface,(0,0))
        pygame.display.flip()

if __name__ == '__main__':
    main()

