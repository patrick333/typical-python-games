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
purple = (159, 0, 197)

bgColor= (0,   0,   0)
textColor = (250, 250, 255)


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
        self.image.fill(purple)
        self.rect = self.image.get_rect()
        
    def setSpeed(self, speedX, speedY):    
        self.speedX=speedX
        self.speedY=speedY
    def update(self):           
        if self.rect.top<padV or self.rect.top>height-padV:
            if self.rect.top<padV:
                self.rect.top=padV
            else:
                self.rect.top=height-padV     
            self.speedY=-self.speedY
        self.rect.move_ip(self.speedX, self.speedY)    

pygame.init()
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption('Pong')

frameImage=pygame.image.load('frame.jpg')
frame=frameImage.get_rect()
frame.center=(width//2, height//2)

# game resources setup
font = pygame.font.SysFont(None, 48)
scoreFont=pygame.font.SysFont("arial,tahoma", 20, True, True)

gameOverSound = pygame.mixer.Sound('gameover.wav')
hitSound=pygame.mixer.Sound('basic_hit.wav')
#pygame.mixer.music.load('background.mid')
pygame.mixer.music.load('background.mp3')    


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
    ballSpeedX=random.randint(-9,-5)
    ballSpeedY=random.randint(-3,3)
    ball.setSpeed(ballSpeedX,ballSpeedY)

    pygame.mixer.music.play(-1, 0.0)
    paused=False
    while True:  #game loop when the game is playing.
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                end();       
            elif event.type == KEYUP:    
                if event.key == K_ESCAPE:
                    end()   
                elif event.key == K_s:    
                    if not paused:#pause it now
                        pygame.mixer.music.pause()
                        #playTime=pygame.mixer.music.get_pos()
                        #pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.unpause()  
                        #pygame.mixer.music.set_pos(playTime)
                        #pygame.mixer.music.start()  
                    paused=not paused  
                    
        
    
        # --- Game logic
        if paused:
            drawText('GAME Paused', font, screen, (width / 3), (height / 3))
            drawText('Press S to continue...', font, screen, (width / 3) - 80, (height / 3) + 50)
            pygame.display.update()       
            continue
        '''
        if paused:
            if pygame.mixer.music.get_busy(): #playing
                #pygame.mixer.music.stop()  
                pygame.mixer.music.pause()  
                print("paused")
            drawText('GAME Paused', font, screen, (width / 3), (height / 3))
            drawText('Press S to continue...', font, screen, (width / 3) - 80, (height / 3) + 50)
            pygame.display.update()       
            continue
        else:
            if not pygame.mixer.music.get_busy():  #get_busy=True: playing. Here, not playing. 
                print("music paused, now unpause it.")
                #pygame.mixer.music.play(-1, 0.0)
                pygame.mixer.music.unpause()
        '''
        
        #opp follow the ball's movement
        opp.rect.centery=ball.rect.centery
   
        # Call the update() method on all the sprites
        all_sprites_list.update()               
            
        # --- Draw a frame
    
        # Clear the screen
        screen.fill(bgColor)      
        screen.blit(frameImage, frame)

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
                ball.speedY+=r[1]//3
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

