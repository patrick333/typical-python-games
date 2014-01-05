import pygame,random,sys
from pygame import *
'''
Do not use pygame collision test. stillGroup will merge with grid.
'''

black    = (   0,   0,   0)
white    = ( 255, 255, 255)

cyan=(0, 255, 255)    #I
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

stepOfDropping=3
gameRate=9

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
                
        self.image = pygame.Surface([width-2, height-2])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft=(topleft[0]+1, topleft[1]+1)
        self.rate=0
        #self.boolStill=False
    
        

class Tetromino(sprite.Group):
    def __init__(self,mode,angle): #angle: 0,1,2,3.
        sprite.Group.__init__(self)
        self.mode=mode
        self.angle=angle
        self.color=self.getColor(mode)
        self.array=self.getArray(mode,angle)
        #print2DAr(self.array)
        self.rect=self.getRect(mode)
        #self.group=self.getGroup(self.array, self.color,self.rect)
        self.addSprites(self.array, self.color,self.rect)
        
        self.rate=0
        
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
                array[1][0]=array[1][1]=array[2][1]=array[2][2]=1
            else: #angle==3
                array[0][1]=array[1][0]=array[1][1]=array[2][0]=1
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
    
    def addSprites(self,array,color,rect):
        l=len(array)
        for y in range(l):
            for x in range(l):
                if array[y][x]==1:
                    self.add(self.getBlock(color, rect,y,x))
    
    def turn(self, i): #i=1: clockwise. i=-1: anti-clockwise
        #the function updates array, group
        self.array=self.getArray(mode,angle+i)
    
    def getBlock(self,color,rect,y,x): 
        topleft=(rect.left+x*width, rect.top+y*height)
        return Block(color,topleft)    
    
    
    
    def moveSprites(self,x,y):#move the contained sprites
        for s in self.sprites():
            s.rect.left+=x
            s.rect.top+=y

    def update(self):
        sprite.Group.update(self)
        self.rate+=1
        if self.rate>=gameRate:
            self.rect.y+=height
            self.moveSprites(0,height)
            
            self.rate=0  

def coordsToIndexes(coord): #e.g. (50,25)->(2,1)
    return (coord[0]//width, coord[1]//height)

def isStill(tetro,grid):#whether the tetro cannot drop anymore.
    return not isMovePossible(tetro, grid, 0,1)

def isCompatible(yIndex,xIndex,array,grid):
    l=len(array)
    for y in range(l):
        for x in range(l):
            if (y+yIndex>nRow-1 or y+yIndex<0 or x+xIndex>nColumn-1 or x+xIndex<0) \
            and array[y][x]==1:
                #print('hitting walls: y+yIndex={0}, x+xIndex={1}'.format(y+yIndex, x+xIndex))
                return False
            elif array[y][x]==1 and grid[y+yIndex][x+xIndex]==1:
                #print('superposing')
                return False
    return True

def isMovePossible(tetro,grid,xMove,yMove): #xMove,yMove is -1, 0, or 1. cannot be both non-zero
    yIndex=tetro.rect.y//height
    xIndex=tetro.rect.x//width

    yIndex+=yMove
    xIndex+=xMove
    
    
    return isCompatible(yIndex,xIndex,tetro.array,grid)     

def isRotatePossible(tetro,grid,iRotate): 
    extraArray=tetro.getArray(tetro.mode, (tetro.angle+iRotate)%4 )
    yIndex=tetro.rect.y//height
    xIndex=tetro.rect.x//width
    
    return isCompatible(yIndex,xIndex,extraArray,grid)     

def merge(tetro,grid):
    #condition: tetro.getArray and grid are compatible; tetro is still.
    array=tetro.array
    l=len(array)
    yIndex=tetro.rect.y//height
    xIndex=tetro.rect.x//width
    
    for y in range(l):
        for x in range(l):
            if array[y][x]==1:
                grid[y+yIndex][x+xIndex]=1
    
    #add sprites to still_sprites
    for s in tetro.sprites():
        still_sprites.add(s)
    tetro.empty()
    
'''
def removeLine(grid,r):
    for j in range(nColumn):
        grid[0][j]=0
        
    for i in range(1,r+1):
        for j in range(nColumn):
            grid[i][j]=grid[i-1][j]
            
    #kill some blocks, move some blocks
    extraGroup=still_sprites.copy()
    for s in extraGroup.sprites():
        yIndex=s.rect.y//height
        if yIndex==r:
            s.remove(still_sprites)
        elif yIndex<r:
            s.rect.y+=height
    
    extraGroup.empty()
'''
'''
def removeLine(grid,r):            
    #kill some blocks, move some blocks
    extraGroup=still_sprites.copy()
    for s in extraGroup.sprites():
        xIndex=s.rect.x//width
        yIndex=s.rect.y//height
        if yIndex==r:
            s.remove(still_sprites)
            grid[yIndex][xIndex]=0
        
        elif yIndex<r:
            s.rect.y+=height
            grid[yIndex][xIndex]=0
            grid[yIndex+1][xIndex]=1        
    
    extraGroup.empty()
'''
def removeLine(grid,r):            
    #kill some blocks, move some blocks
    extraGroup=still_sprites.copy()
    for s in extraGroup.sprites():
        yIndex=s.rect.y//height
        if yIndex==r:
            s.remove(still_sprites)
        
        elif yIndex<r:
            s.rect.y+=height       
    
    extraGroup.empty()

def restoreGridFromStillGroup(grid):
    for y in range(nRow):
        grid[y]=[0 for _ in range(nColumn)]
    for s in still_sprites.sprites():
        xIndex=s.rect.x//width
        yIndex=s.rect.y//height
        grid[yIndex][xIndex]=1

def getGridForStillGroup():   
    stillGrid=[] 
    for y in range(nRow):
        stillGrid.append([0 for _ in range(nColumn)])
    
    for s in still_sprites.sprites():
        xIndex=s.rect.x//width
        yIndex=s.rect.y//height
        stillGrid[yIndex][xIndex]=1
    return stillGrid
 
def debugGridStillGroup():
    global stillGrid
    for s in still_sprites.sprites():
        xIndex=s.rect.x//width
        yIndex=s.rect.y//height
        if grid[yIndex][xIndex]==0:
            #no good
            stillGrid=getGridForStillGroup()            
            print('still_sprites and grid is not compatible: grid[{0}][{1}]'.\
                  format(yIndex,xIndex))
            break
    
def evaluateScore(grid):
    numOfLinesScored=0  #numOfLinesScored should be 0->4
    for r in range(nRow):
        for c in range(nColumn):
            #print('grid[{0}][{1}]={2}'.format(r,c,grid[r][c])   )
            if grid[r][c]==0:
                break    
                    
        #remove a line
        if c==nColumn-1 and grid[r][c]==1:
            #print('grid[{0}][{1}]={2}'.format(r,c,grid[r][c])   )
            print('removing a line')
            removeLine(grid,r)
            restoreGridFromStillGroup(grid)
            #debugGridStillGroup()
            numOfLinesScored+=1
    
    return numOfLinesScored

def isOver(grid):#judge after merge.
    for c in range(nColumn):
        if grid[1][c]==1:
            return True
    return False

pygame.init()

grid=[]
for y in range(nRow):
    grid.append([0 for _ in range(nColumn)])


size = [width*nColumn, height*nRow]
screen = display.set_mode(size)
still_sprites=sprite.Group()
stillGrid=[]

display.set_caption("My Tetris")

clock = time.Clock()

readyForNext=True

score=0

while True:
    change=[0,0]
    iRotate=0
    for e in event.get(): 
        if e.type == pygame.QUIT: 
            end()  
        elif e.type == KEYDOWN:    
                if e.key == K_ESCAPE:
                    end()
                elif e.key == K_LEFT:
                    change[0]-=1
                elif e.key == K_RIGHT:
                    change[0]+=1
                elif e.key == K_UP:  #rotate clockwise
                    iRotate=1
                elif e.key == K_SPACE:  #rotate clockwise
                    iRotate=-1
                elif e.key == K_DOWN:  #accelerate in dropping.
                    change[1]+=stepOfDropping
                
                                    
                
    screen.fill(black)
    
    
    if readyForNext: #generate a new tetro
        mode=random.randint(0,6)
        angle=random.randint(0,3)
        tetro=Tetromino(mode,angle)
        
        #still_sprites.add(tetro.sprites())
        readyForNext=False
    
    
    if change[0]!=0 or change[1]!=0:
        #print('try moving')
        if isMovePossible(tetro, grid,change[0], change[1]):
            #print('moving')
            tetro.rect.x+=change[0]*width
            tetro.rect.y+=change[1]*height
            tetro.moveSprites(change[0]*width,change[1]*height)
   
    if iRotate!=0:
        #print('try rotating')
        if isRotatePossible(tetro,grid,iRotate):
            #print('rotating')
            #change array,sprites
            tetro.angle=(tetro.angle+iRotate)%4
            tetro.array=tetro.getArray(tetro.mode, tetro.angle)
            tetro.empty()
            tetro.addSprites(tetro.array, tetro.color, tetro.rect)
           
   
    if isStill(tetro,grid):
        #merge grid with tetro
        merge(tetro,grid)
        #debugGridStillGroup
        readyForNext=True
        
       

    tetro.update()
    tetro.draw(screen)
    
    
    still_sprites.draw(screen)
    
    numOfLines=evaluateScore(grid)
    if numOfLines>0:
        score+=100*(numOfLines**2)
        print('score={0}'.format(score))

    if isOver(grid):
        print('score={0}. GAME OVER! BYE!'.format(score))
        end()

    clock.tick(30)
    display.update()
    

pygame.quit()