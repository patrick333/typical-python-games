import pygame
import random,sys
from pygame.locals import *

width = 600 
height = 600
gameFrameWidth=560
gameFrameHeight=560
blockWidth=20
blockHeight=15
playerWidth=20
playerHeight=20
bulletWidth=4
bulletHeight=10

blockCount=0
blockAddRate=6
bulletCount=0
bulletAddRate=3
#bulletAddRate=200

screenSpeed=3
bulletSpeed=5
FPS=40

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)
textColor = (250, 250, 255)


def end():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    end()
                return
              
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, textColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
                
#classes: Block, Player, Bullet.

# This class represents the enemy        
class Block(pygame.sprite.Sprite):
    global screenSpeed
    def __init__(self, color, width, height, speed):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.speed=speed;
    def update(self):
        self.rect.y += self.speed+screenSpeed

# This class represents the Player        
class Player(pygame.sprite.Sprite):    
    def __init__(self, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 

        self.image = pygame.Surface([width, height])
        self.image.fill(red)

        self.rect = self.image.get_rect()
        
    def update(self):
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()
    
        self.rect.x = pos[0]-self.rect.width//2
        self.rect.y = pos[1]- self.rect.height//2
        
# This class represents the bullet        
class Bullet(pygame.sprite.Sprite):    
    global bulletSpeed
    def __init__(self,width, height):
        pygame.sprite.Sprite.__init__(self) 

        self.image = pygame.Surface([width, height])
        self.image.fill(white)

        self.rect = self.image.get_rect()        
    def update(self):
        self.rect.y -= bulletSpeed

'''fontList=pygame.font.get_fonts()
for font in fontList:
    print(font)
'''    
        
pygame.init()
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption('Raiden Simulation Game Engine')

# game resources setup
font = pygame.font.SysFont(None, 48)
#scoreFont=pygame.font.SysFont(["Arial","Tahoma","Times New Roman","Verdana"], 20, True, True)  #how the list should be formatted.
scoreFont=pygame.font.SysFont("arial,tahoma", 20, True, True)
#scoreFont=pygame.font.SysFont("arial", 20, True, True)
gameOverSound = pygame.mixer.Sound('gameover.wav')
shootSound=pygame.mixer.Sound('basic_shoot.wav')
hitSound=pygame.mixer.Sound('basic_hit.wav')
pygame.mixer.music.load('background.mid')  


# sprites for block, player
all_sprites_list = pygame.sprite.Group()
block_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()

'''
for i in range(50):
    # This represents a block
    speed=random.randrange(-2,3)
    block = Block(blue,blockWidth, blockHeight,speed)

    # Set a random location for the block
    block.rect.x = random.randrange(width)
    block.rect.y = random.randrange(height-playerHeight-30)
    
    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)
'''
# Create a red player block
player = Player(playerWidth, playerHeight)
all_sprites_list.add(player)

clock = pygame.time.Clock()

score = 0
topScore=0
player.rect.y = height-playerHeight-10

drawText('RAIDEN', font, screen, (width / 3), (height / 3))
drawText('Press any key to start...', font, screen, (width / 3) - 80, (height / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

# -------- Main Program Loop -----------
while True:    

    pygame.mixer.music.play(-1, 0.0)
    boolFire=False
    while True:  #game loop when the game is playing.
        #pygame.mixer.music.play(-1, 0.0)
        # --- Event Processing
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                end();       
            elif event.type == KEYUP:    
                if event.key == K_ESCAPE:
                        end()     
            elif event.type == pygame.MOUSEBUTTONDOWN:
                boolFire=True
            elif event.type == pygame.MOUSEBUTTONUP:
                boolFire=False
        
        if boolFire:
            bulletCount+=1
        if boolFire and bulletCount>=bulletAddRate:
            bulletCount=0
            #sound for shooting
            #shootSound.play()
            bullet = Bullet(bulletWidth, bulletHeight)
            # Set the bullet so it is where the player is
            bullet.rect.x = player.rect.x+player.rect.width//2-bullet.rect.width//2
            bullet.rect.y = player.rect.y-12
            # Add the bullet to the lists
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)       
            
             
        # --- Game logic
        
        #add blocks
        blockCount+=1
        if blockCount == blockAddRate:
            blockCount = 0
            speed=random.randrange(-2,3)
            block = Block(blue,blockWidth, blockHeight,speed)
            block.rect.x = random.randrange(width)
            #block.rect.y = random.randrange(height-playerHeight-30)
            block.rect.y = 0
            
            # Add the block to the list of objects
            block_list.add(block)
            all_sprites_list.add(block)
        
        # Call the update() method on all the sprites
        all_sprites_list.update()
           
        
        # Calculate mechanics for each bullet
        for bullet in bullet_list:
            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True) #note the "True"
            
            # For each block hit, remove the bullet and add to the score
            for block in block_hit_list:
                hitSound.play()   
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)                             
                score += 3
                
            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < -bulletHeight:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
            
        # --- Draw a frame
    
        # Clear the screen
        screen.fill(black)      
            
        # Draw all the spites
        all_sprites_list.draw(screen)
        
        drawText('Score: %s' % (score), scoreFont, screen, 10, 0)
        drawText('Top Score: %s' % (topScore), scoreFont, screen, 10, 20)
    
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
        # check if any block has touched the player
        player_hit_list = pygame.sprite.spritecollide(player, block_list, True)
        if player_hit_list:
            if score>topScore:
                topScore = score
            break    
        
        # --- Limit to 20 frames per second
        clock.tick(FPS)
    
    pygame.mixer.music.stop()    
    gameOverSound.play()

    drawText('GAME OVER', font, screen, (width / 3), (height / 3))
    drawText('Press a key to play again...', font, screen, (width / 3) - 80, (height / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()    
        
