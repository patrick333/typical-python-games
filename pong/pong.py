import pygame
import random,sys
from pygame.locals import *

'''
Do not need scores, 
Use the mouse to control the player position.
'''

width = 600 
height = 600

gameFrameWidth=560
gameFrameHeight=560

padH=(width-gameFrameWidth)//2
padV=(height-gameFrameHeight)//2

playerWidth=20
playerHeight=60
oppWidth=20
oppHeight=60
ballWidth=20
ballHeight=20

mouseRelRate=5
mouseRelCount=0


# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)
bgColor= (0,   0,   0)
textColor = (250, 250, 255)

ballSpeedX=-8
ballSpeedY=-2
#ballSpeedY=0
speedYlimit=10

FPS=40

def end():
    pygame.quit()
    sys.exit()

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, textColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: 
                    end()
                return

class Player(pygame.sprite.Sprite):    
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self) 

        self.image = pygame.Surface([width, height])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        
    def update(self):
        pos = pygame.mouse.get_pos()    
        self.rect.y = pos[1]- self.rect.height//2


class Opponent(pygame.sprite.Sprite):    
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self) 

        self.image = pygame.Surface([width, height])
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        
    #def update(self):
        

class Ball(pygame.sprite.Sprite):    
    global padV,height
    def __init__(self, width, height) :
        pygame.sprite.Sprite.__init__(self) 

        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        
    def setSpeed(self, speedX, speedY):    
        self.speedX=speedX
        self.speedY=speedY
    def update(self):    
        self.rect.move_ip(self.speedX, self.speedY)
        if self.rect.top<padV or self.rect.top>height-padV:
            self.speedY=-self.speedY


pygame.init()
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption('Pong')

# game resources setup
font = pygame.font.SysFont(None, 48)
scoreFont=pygame.font.SysFont("arial,tahoma", 20, True, True)

gameOverSound = pygame.mixer.Sound('gameover.wav')
hitSound=pygame.mixer.Sound('basic_hit.wav')
pygame.mixer.music.load('background.mid')  


all_sprites_list = pygame.sprite.Group()
player = Player(playerWidth, playerHeight)
opp=Opponent(oppWidth, oppHeight)
ball=Ball(ballWidth, ballHeight)
all_sprites_list.add(player)
all_sprites_list.add(opp)
all_sprites_list.add(ball)

clock = pygame.time.Clock()


while True:    
    pygame.mouse.set_pos([width//2, height//2])
    #pygame.mouse.set_visible(False)
    
    player.rect.center=(player.rect.width//2, height//2)
    opp.rect.center=(width-opp.rect.width//2, height//2)
    ball.rect.center=(width//2, height//2)
    ball.setSpeed(ballSpeedX,ballSpeedY)

    pygame.mixer.music.play(-1, 0.0)
    while True:  #game loop when the game is playing.
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                end();       
            elif event.type == KEYUP:    
                if event.key == K_ESCAPE:
                        end()   
    
        # --- Game logic
        #opp follow the ball's movement
        opp.rect.centery=ball.rect.centery
   
        # Call the update() method on all the sprites
        all_sprites_list.update()
           
        

            
        # --- Draw a frame
    
        # Clear the screen
        screen.fill(bgColor)      
            

        all_sprites_list.draw(screen)

        pygame.display.flip()
        
        # check if the ball has touched the player or the opp
        mouseRelCount+=1
        if mouseRelCount>=mouseRelRate:
            mouseRelCount=0
            r=pygame.mouse.get_rel()
        player_hit=player.rect.colliderect(ball.rect)
        opp_hit=opp.rect.colliderect(ball.rect)
        if player_hit or opp_hit:
            hitSound.play()
            ball.speedX=-ball.speedX
            if player_hit:                
                #print(r[0],end=' ')
                #print(r[1])
                ball.speedY+=r[1]
                if ball.speedY>speedYlimit:
                    ball.speedY=speedYlimit
                elif ball.speedY<-speedYlimit:
                    ball.speedY=-speedYlimit
                        

        #check if the ball has passed through the player  
        if ball.rect.left<padH-5 or ball.rect.left>width-padH+5:
            break
        
        clock.tick(FPS)
    
    pygame.mixer.music.stop()    
    gameOverSound.play()

    drawText('GAME OVER', font, screen, (width / 3), (height / 3))
    drawText('Press a key to play again...', font, screen, (width / 3) - 80, (height / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()  

