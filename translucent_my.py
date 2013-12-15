import pygame, os.path
from pygame.locals import *

backgroundColor=(   150,   150,   200)
white=(255,255,255)

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(backgroundColor)
    clock = pygame.time.Clock()
    
    image = pygame.image.load('basic_plane.png')
    imageRect = image.get_rect()
    playerImage=pygame.transform.scale(image, (imageRect.right//2, imageRect.bottom//2))
    playerImage=playerImage.convert()
    playerImage.set_colorkey(white)
    playerRect = playerImage.get_rect()

    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
              return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
              return

        screen.blit(background, (0,0))
        screen.blit(playerImage, (0,0))
        pygame.display.flip()

if __name__ == '__main__':
    main()

