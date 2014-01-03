import pygame,random,sys
from pygame import *

black    = (   0,   0,   0)
white    = ( 255, 255, 255)

cyan=(255, 255, 255)    #I
yellow=(255,255,0)      #O
purple=(128,0,128)      #T
green=( 0, 255, 0)      #S
red=(255,0,0)           #Z
blue=(0,0,255)          #J
orange=(255,165,0)      #L

width  = 25
height = 25
margin = 0

nColumn=10 
nRow=25


colorDict={0:cyan, 1:yellow, 2:purple, 3:green, 4:red, 5:blue, 6:orange}


def end():
    pygame.quit()
    sys.exit()

def printAr(args):    
    print(" ".join(str(v) for v in args))

def print2DAr(args):    
    for arg in args:
        printAr(arg)

class Block(sprite.Sprite):
    def __init__(self,color,topleft):
        sprite.Sprite.__init__(self) 
                
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft=topleft
        self.rate=0
        self.boolStill=False
    def update(self):
        
            
            
        self.rate+=1
        if self.rate>=4:
            self.rect.y+=height
            self.rate=0
        

class Tetromino():
    def __init__(self,mode,angle): #angle: 0,1,2,3.
        self.mode=mode
        self.color=self.getColor(self.mode)
        self.array=self.getArray(self.mode,angle)
        #print2DAr(self.array)
        self.rect=self.getRect(self.mode)
        self.group=self.getGroup(self.array, self.color,self.rect)
        
        
    def getColor(self,mode):
        return colorDict[mode]
    def getRect(self,mode):
        topleft=(width*3,0)
        if mode==0 or mode==1:            
            size=(width*4, height*3)
        else:
            size=(width*3, height*3)
        return Rect(topleft,size)
    def getArray(self,mode,angle):
        array=[]
        if mode==0 or mode==1:
            l=4
        else:
            l=3
        for _ in range(l):
            array.append([0 for i in range(l)])
            
        if mode==0:   #I
            if angle==0:
                array[1]=[1 for i in range(l)]
            elif angle==1:
                for i in range(l):
                    array[i][2]=1
            elif angle==2:
                array[2]=[1 for i in range(l)]
            else: #angle==3
                for i in range(l):
                    array[i][1]=1
        elif mode==1:   # O
            array[1][1]=1
            array[1][2]=1
            array[2][1]=1
            array[2][2]=1
        elif mode==2: #T
            if angle==0:
                array[0][1]=array[1][0]=array[1][1]=array[1][2]=1
            elif angle==1:
                array[1][2]=array[0][1]=array[1][1]=array[2][1]=1
            elif angle==2:
                array[2][1]=array[1][0]=array[1][1]=array[1][2]=1
            else: #angle==3
                array[1][0]=array[0][1]=array[1][1]=array[2][1]=1
        elif mode==3:  #S
            if angle==0:
                array[0][1]=array[0][2]=array[1][0]=array[1][1]=1
            elif angle==1:
                array[0][1]=array[1][1]=array[1][2]=array[2][2]=1
            elif angle==2:
                array[1][1]=array[1][2]=array[2][0]=array[2][1]=1
            else: #angle==3
                array[0][0]=array[1][0]=array[1][1]=array[2][1]=1
        elif mode==4: #Z
            if angle==0:
                array[0][0]=array[0][1]=array[1][1]=array[1][2]=1
            elif angle==1:
                array[0][2]=array[1][2]=array[1][1]=array[2][1]=1
            elif angle==2:
                array[2][1]=array[1][0]=array[1][1]=array[1][2]=1
            else: #angle==3
                array[1][0]=array[1][1]=array[2][1]=array[2][2]=1
        elif mode==5: #J
            if angle==0:
                array[0][0]=1
                array[1]=[1 for i in range(l)]
            elif angle==1:
                array[0][2]=1
                for i in range(l):
                    array[i][1]=1
            elif angle==2:
                array[2][2]=1
                array[1]=[1 for i in range(l)]
            else: #angle==3
                array[2][0]=1
                for i in range(l):
                    array[i][1]=1
        else:   #mode==6 #L
            if angle==0:
                array[0][2]=1
                array[1]=[1 for i in range(l)]
            elif angle==1:
                array[2][2]=1
                for i in range(l):
                    array[i][1]=1
            elif angle==2:
                array[2][0]=1
                array[1]=[1 for i in range(l)]
            else: #angle==3
                array[0][0]=1
                for i in range(l):
                    array[i][1]=1
        return array
    
    def getGroup(self,array,color,rect):
        group=sprite.Group()
        l=len(array)
        for y in range(l):
            for x in range(l):
                if array[y][x]==1:
                    group.add(self.getBlock(color, rect,y,x))
        return group

    def getBlock(self,color,rect,y,x): 
        topleft=(rect.left+x*width, rect.top+y*height)
        return Block(color,topleft)    
    
pygame.init()


size = [width*nColumn+margin*(nColumn+1), height*nRow+margin*(nRow+1)]
screen = display.set_mode(size)
still_sprites=sprite.Group()

display.set_caption("My Tetris")

clock = time.Clock()

readyForNext=True
mode=random.randint(0,6)
angle=random.randint(0,3)
tetro=Tetromino(mode,angle)        

while True:
    for e in event.get(): 
        if e.type == pygame.QUIT: 
            end()  
        elif e.type == KEYDOWN:             
                xDelta,yDelta=0,0
                if e.key == K_ESCAPE:
                    end()
                    
    screen.fill(black)
    
    if readyForNext: #generate a new tetro
        mode=random.randint(0,6)
        angle=random.randint(0,3)
        tetro=Tetromino(mode,angle)
        
        readyForNext=False

    tetro.group.update()
    tetro.group.draw(screen)
    still_sprites.draw(screen)
    
    #collision test between tetro and stillGroup+walls.
    for s in tetro.group:
        if s.rect.bottom>=size[1] or sprite.spritecollide(s, still_sprites, False):
            readyForNext=True
            #update still_sprites
            still_sprites.add(tetro.group)
            
    if readyForNext:
        for s in tetro.group:
            s.boolStill=True
            
    #hit_list=sprite.spritecollide(tetro, block_list, True)

    clock.tick(30)
 
    # Go ahead and update the screen with what we've drawn.
    display.update()
     

pygame.quit()











