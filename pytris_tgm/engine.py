# -*- coding: utf-8 -*-

# TODO List
# Initial Rotation System

import random
from random import randint
from math import ceil, floor
from enum import IntEnum
    
# Tetris game
class Engine:
    # Constants
    NUM_COLS = 10
    NUM_ROWS = 20
    HISTORY_ATTEMPTS = 4
    DELAY_ARE = 30 # Entry delay
    DELAY_DAS = 14 # Delayed auto shift
    DELAY_LOCK = 30 # Lock delay
    DELAY_LINE_CLEAR = 41 # Line clear delay
    START_OFFSET = 3 # X Offset from left side of field
    capture = False
    clear = False
    gravityLevels = [0,30,35,40,50,60,70,80,90,100,120,140,160,170,200,220,230,233,236,239,243,247,251,300,330,360,400,420,450,500]
    gravityInteral = [4,6,8,10,12,16,32,48,64,80,96,112,128,144,4,32,64,96,128,160,192,224,256,512,768,1024,1280,1024,768,5120]

    class Tetronimo(IntEnum):
        T = 0
        J = 1
        L = 2
        Z = 3
        S = 4
        I = 5
        O = 6

    class GameType(IntEnum):
        NORMAL = 0
        SCREENSAVER_0 = 1
        SCREENSAVER_1 = 2
        SCREENSAVER_2 = 3

    # tetronimoRotation[tetronimo][rotation][block][x,y]
    tetronimoRotations = {
        Tetronimo.T:
        [[[0,0],[1,0],[2,0],[1,1]],
         [[1,0],[0,1],[1,1],[1,2]],
         [[1,0],[0,1],[1,1],[2,1]],
         [[0,0],[0,1],[1,1],[0,2]]],
        Tetronimo.J:
        [[[0,0],[1,0],[2,0],[2,1]],
         [[1,0],[1,1],[0,2],[1,2]],
         [[0,0],[0,1],[1,1],[2,1]],
         [[0,0],[1,0],[0,1],[0,2]]],
        Tetronimo.L:
        [[[0,0],[1,0],[2,0],[0,1]],
         [[0,0],[1,0],[1,1],[1,2]],
         [[2,0],[0,1],[1,1],[2,1]],
         [[0,0],[0,1],[0,2],[1,2]]],
        Tetronimo.Z:
        [[[0,0],[1,0],[1,1],[2,1]],
         [[1,0],[0,1],[1,1],[0,2]],
         [[0,0],[1,0],[1,1],[2,1]],
         [[1,0],[0,1],[1,1],[0,2]]],
        Tetronimo.S:
        [[[1,0],[2,0],[0,1],[1,1]],
         [[0,0],[0,1],[1,1],[1,2]],
         [[1,0],[2,0],[0,1],[1,1]],
         [[0,0],[0,1],[1,1],[1,2]]],
        Tetronimo.I:
        [[[0,0],[1,0],[2,0],[3,0]],
         [[0,0],[0,1],[0,2],[0,3]],
         [[0,0],[1,0],[2,0],[3,0]],
         [[0,0],[0,1],[0,2],[0,3]]],
        Tetronimo.O:
        [[[0,0],[1,0],[0,1],[1,1]],
         [[0,0],[1,0],[0,1],[1,1]],
         [[0,0],[1,0],[0,1],[1,1]],
         [[0,0],[1,0],[0,1],[1,1]]]}

    # Tetronimo state
    class State(IntEnum):
        START = 0
        NEW_TETRONIMO = 1
        FALLING = 2
        LOCKED = 3
        END = 4

    # tetronimoSizes[tetronimo][width,height]
    tetronimoSizes = {
        Tetronimo.T:[3,2],
        Tetronimo.J:[3,2],
        Tetronimo.L:[3,2],
        Tetronimo.Z:[3,2],
        Tetronimo.S:[3,2],
        Tetronimo.I:[4,1],
        Tetronimo.O:[2,2]}

    tetronimoStartOffset = {
        Tetronimo.T:0,
        Tetronimo.J:0,
        Tetronimo.L:0,
        Tetronimo.Z:0,
        Tetronimo.S:0,
        Tetronimo.I:0,
        Tetronimo.O:1}

    # tetronimoRotationStart[tetronimo][orientation][0:CW 1:CCW][x offset, y offset]
    tetronimoRotationStart = {
        Tetronimo.T:[
            [[0,-1],[1,-1]],
            [[0,1],[0,1]],
            [[1,-1],[0,-1]],
            [[-1,1],[-1,1]]],
        Tetronimo.J:[
            [[0,-1],[1,-1]],
            [[0,1],[0,1]],
            [[1,-1],[0,-1]],
            [[-1,1],[-1,1]]],
        Tetronimo.L:[
            [[0,-1],[1,-1]],
            [[0,1],[0,1]],
            [[1,-1],[0,-1]],
            [[-1,1],[-1,1]]],
        Tetronimo.Z:[
            [[1,-1],[1,-1]],
            [[-1,1],[0,1]],
            [[1,-1],[0,-1]],
            [[-1,1],[-1,1]]],
        Tetronimo.S:[
            [[0,-1],[0,-1]],
            [[0,1],[0,1]],
            [[0,-1],[0,-1]],
            [[0,1],[0,1]]],
        Tetronimo.I:[
            [[2,-1],[2,-1]],
            [[-2,1],[-2,1]],
            [[2,-1],[2,-1]],
            [[-2,1],[-2,1]]],
        Tetronimo.O:[
            [[0,0],[0,0]],
            [[0,0],[0,0]],
            [[0,0],[0,0]],
            [[0,0],[0,0]]]}
        

    TETRONIMO_HISORY_START = [Tetronimo.Z, Tetronimo.Z, Tetronimo.Z, Tetronimo.Z]

    def __init__(self):
        self.gameType = self.GameType.NORMAL
        self.gameStarted = False
        
    def newGame(self):
        self.frame = 0
        self.tetronimoHistory = self.TETRONIMO_HISORY_START
        self.clearGrid()
        self.activeTetronimo = None
        self.activeLocation = [None,None]
        self.activeRotation = None
        self.preview = None
        self.areDelayCount = self.DELAY_ARE
        self.lockDelayCount = self.DELAY_LOCK
        
        self.controlLeft = False
        self.controlRight = False
        self.controlDown = False
        self.controlA = False
        self.controlB = False
        self.controlC = False

        self.controlLeftLast = False
        self.controlRightLast = False
        self.controlDownLast = False
        self.controlALast = False
        self.controlBLast = False
        self.controlCLast = False

        self.controlLeftCount = self.DELAY_DAS
        self.controlRightCount = self.DELAY_DAS
        
        self.atBottom = False
        self.ended = False
        
        self.state = self.State.START
        self.score = 0
        self.level = 1
        self.soft = 0
        self.combo = 1
        self.dropCount = self.getDropCount()

    def getGravity(self):
        gravityIndex = 0
        for i in range(len(self.gravityLevels)):
            if (self.gravityLevels[i] >= self.level):
                break
            gravityIndex = i
        return self.gravityInteral[gravityIndex]

    def getDropCount(self):
        dropCount = 0
        gravity = self.getGravity()
        if (gravity < 256):
            dropCount = floor(256 / gravity) # TODO: Find the right equation
        else:
            dropCount = 0
        return dropCount

    def getDropFrameCount(self):
        dropFrameCount = 1
        gravity = self.getGravity()
        if (gravity < 256):
            dropFrameCount = 1
        else:
            dropFrameCount = floor(gravity / 256) # TODO: Find the right equation
        return dropFrameCount
        
        
    def getNextTetronimo(self):
        bag = list(self.Tetronimo)
        choices = list(self.Tetronimo)
        
        # Set up bag by removing pieces
        if (self.frame == 0):
            # Cannot start game with S, Z, or O
            choices.remove(self.Tetronimo.S)
            choices.remove(self.Tetronimo.Z)
            choices.remove(self.Tetronimo.O)
        else:
            # Remove pieces in history
            for tetronimo in self.tetronimoHistory:
                if (tetronimo in bag):
                    bag.remove(tetronimo)
                    
        # Try to get random piece
        for x in range(self.HISTORY_ATTEMPTS):
            attempt = random.choice(choices)
            if (attempt in bag):
                break

        # Add selected piece to history
        self.tetronimoHistory.pop()
        self.tetronimoHistory.insert(0,attempt)

        return attempt

    def addTetronimo(self, tetronimo, rotation, loc):
        overlap = self.testTetronimo(tetronimo, rotation, loc)
        for i in range(4):
            x = loc[0] + self.tetronimoRotations[tetronimo][rotation][i][0]
            y = loc[1] - self.tetronimoRotations[tetronimo][rotation][i][1]
            self.grid[y][x] = tetronimo
        return overlap

    def removeTetronimo(self, tetronimo, rotation, loc):
        for i in range(4):
            x = loc[0] + self.tetronimoRotations[tetronimo][rotation][i][0]
            y = loc[1] - self.tetronimoRotations[tetronimo][rotation][i][1]
            self.grid[y][x] = None

    def testTetronimo(self, tetronimo, rotation, loc):
        test = True
        # Check to see if tetronimo resides in grid
        if ((loc[1] - self.tetronimoSizes[tetronimo][1] + 1 < 0) or # Bottom border
            (loc[0] < 0) or # Left border
            (loc[1] >= self.NUM_ROWS+2) or # Top border
            (loc[0] + self.tetronimoSizes[tetronimo][0] - 1 >= self.NUM_COLS)): # Right border
            test = False
        else:
            for i in range(4):
                x = loc[0] + self.tetronimoRotations[tetronimo][rotation][i][0]
                y = loc[1] - self.tetronimoRotations[tetronimo][rotation][i][1]
                if (self.grid[y][x] != None):
                    test = False
                    break
        return test

    def addTetronimoTop(self, tetronimo):
        xOffset = self.START_OFFSET + self.tetronimoStartOffset[tetronimo]
        yOffset = self.NUM_ROWS - 1
        self.activeTetronimo = tetronimo
        self.activeLocation = [xOffset,yOffset]
        self.activeRotation = 0
        if (self.level % 100 != 99):
            self.level += 1
        return self.addTetronimo(self.activeTetronimo,self.activeRotation,[xOffset,yOffset])
    
    ## Grid display
    #def displayGrid(self):
    #    print('┌', end='')
    #    for x in range(self.NUM_COLS):
    #        print('─', end='')
    #    print('┐')
    #    for x in reversed(range(self.NUM_ROWS)):
    #        print('│', end='')
    #        for y in range(self.NUM_COLS):
    #            char = None
    #            if (self.grid[x][y]==None):
    #                char = ' '
    #            else:
    #                char = int(self.grid[x][y])
    #            print(char, end='')
    #        print('│')
    #    print('└', end='')
    #    for x in range(self.NUM_COLS):
    #        print('─', end='')
    #    print('┘')

    # Clear the grid
    def clearGrid(self):
        self.grid = [[None for x in range(self.NUM_COLS)] for y in range(self.NUM_ROWS+3)]

    # Is next move possible?
    def isMovePossible(self, oldTetronimo, oldRotation, oldLoc, newTetronimo, newRotation, newLoc):
        if (newTetronimo == None):
            movable = False
        else:
            movable = True
            for i in range(4):
                x = newLoc[0] + self.tetronimoRotations[newTetronimo][newRotation][i][0]
                y = newLoc[1] - self.tetronimoRotations[newTetronimo][newRotation][i][1]
                # Check if location is out of bounds
                if ((y < 0) or (y >= self.NUM_ROWS+2) or (x < 0) or (x >= self.NUM_COLS)):
                    movable = False
                    break
                # Check to see if new location overlaps with any part of old location
                if (self.grid[y][x] != None):
                    good = False
                    for j in range(4):
                        if ((x == (oldLoc[0] + self.tetronimoRotations[oldTetronimo][oldRotation][j][0])) and
                            (y == (oldLoc[1] - self.tetronimoRotations[oldTetronimo][oldRotation][j][1]))):
                            good = True
                            break
                    if (good == False):
                        movable = False
                        break
        return movable

    # Move tetronimo down
    def moveDown(self, num):
        
        for i in range(num):
            movable = self.isMovePossible(self.activeTetronimo,
                                          self.activeRotation,
                                          self.activeLocation,
                                          self.activeTetronimo,
                                          self.activeRotation,
                                          [self.activeLocation[0],self.activeLocation[1] - 1])
            if (movable):
                self.removeTetronimo(self.activeTetronimo,self.activeRotation,self.activeLocation)
                self.activeLocation[1] = self.activeLocation[1] - 1
                self.addTetronimo(self.activeTetronimo,self.activeRotation,self.activeLocation)
            else:
                break
                
        return movable

    # Direction 0:Left, 1:Right
    def moveHoriz(self, direction): 
        if (direction): # Go right
            offset = 1
        else: # Go left
            offset = -1
        movable = self.isMovePossible(self.activeTetronimo,
                                  self.activeRotation,
                                  self.activeLocation,
                                  self.activeTetronimo,
                                  self.activeRotation,
                                  [self.activeLocation[0] + offset,self.activeLocation[1]])
        if (movable):
            self.removeTetronimo(self.activeTetronimo,self.activeRotation,self.activeLocation)
            self.activeLocation[0] = self.activeLocation[0] + offset
            self.addTetronimo(self.activeTetronimo,self.activeRotation,self.activeLocation)
        return movable

    # Rotation 0:CW 1:CCW
    def rotate(self,direction):
        tetronimo = self.activeTetronimo
        rotation = self.activeRotation
        loc = self.activeLocation

        if (direction == 0):
            newRotation = (rotation + 1) % 4
        elif (direction == 1):
            newRotation = (rotation - 1) % 4

        # self.activeLocation is pass by reference, not value
        newLoc = [0,0]
        newLoc[0] = loc[0] + self.tetronimoRotationStart[tetronimo][rotation][direction][0]
        newLoc[1] = loc[1] - self.tetronimoRotationStart[tetronimo][rotation][direction][1]
    
        movable = True
        if ((tetronimo == None) or (newRotation == None)):
            movable = False
        # Try default spot
        elif (self.isMovePossible(tetronimo, rotation, loc, tetronimo, newRotation, newLoc)):
            pass
        # Else try to the right
        elif (self.isMovePossible(tetronimo, rotation, loc, tetronimo, newRotation, [newLoc[0]+1,newLoc[1]])):
            newLoc = [newLoc[0]+1,newLoc[1]]
        # Else try to the left
        elif (self.isMovePossible(tetronimo, rotation, loc, tetronimo, newRotation, [newLoc[0]-1,newLoc[1]])):
            newLoc = [newLoc[0]-1,newLoc[1]]
        else:
            movable = False

        if (movable):
            # Remove old peice
            self.removeTetronimo(tetronimo,rotation,loc)
            # Add new peice
            self.addTetronimo(tetronimo,newRotation,newLoc)
            # Update location
            self.activeLocation = list(newLoc)
            # Update rotation
            self.activeRotation = newRotation
        
        return movable

    # Check and remove completed lines
    def checkLines(self):
        linesCleared = 0
        if (self.activeTetronimo == None):
            for y in range(self.NUM_ROWS+3-1, -1, -1):   
                if (None not in self.grid[y][0:(self.NUM_COLS)]):
                    linesCleared += 1
                    del self.grid[y]
                    self.grid.append([None for x in range(len(self.grid[0]))])
            if (linesCleared > 0):
                self.level += linesCleared
                # score = ((Level + Lines)/4 + Soft) x Lines x Combo x Bravo
                if (None not in self.grid[0][0:(self.NUM_COLS)]):
                    bravo = 4
                else:
                    bravo = 1
                self.combo += 2 * linesCleared - 2
                self.score += (ceil((self.level + linesCleared)/4) + self.soft) * linesCleared * self.combo * bravo
            else:
                self.combo = 1
        return (linesCleared > 0)

    # Add random tetronimo to random location
    def addRandom(self):
        tetronimo = self.getNextTetronimo()
        rotation = randint(0,3)
        if (rotation % 2 == 0):
            sizeX = self.tetronimoSizes[tetronimo][0]
            sizeY = self.tetronimoSizes[tetronimo][1]
        else:
            sizeX = self.tetronimoSizes[tetronimo][1]
            sizeY = self.tetronimoSizes[tetronimo][0]
        gridX = randint(0,self.NUM_COLS-sizeX)
        gridY = randint(sizeY-1,self.NUM_ROWS-1)
        self.addTetronimo(tetronimo,rotation,[gridX,gridY])

    # Add random tetronimo to random location that isnt take
    def addRandomClean(self, tries):
        added = False
        for i in range(tries):
            tetronimo = random.choice(list(self.Tetronimo))
            rotation = randint(0,3)
            if (rotation % 2 == 0):
                sizeX = self.tetronimoSizes[tetronimo][0]
                sizeY = self.tetronimoSizes[tetronimo][1]
            else:
                sizeX = self.tetronimoSizes[tetronimo][1]
                sizeY = self.tetronimoSizes[tetronimo][0]
            gridX = randint(0,self.NUM_COLS-sizeX)
            gridY = randint(sizeY-1,self.NUM_ROWS-1)
            if (self.testTetronimo(tetronimo,rotation,[gridX,gridY])):
                self.addTetronimo(tetronimo,rotation,[gridX,gridY])
                added = True
                break
            else:
                continue
        return added
            
    def nextFrame(self):
        if (self.gameType == self.GameType.NORMAL):
            if (self.state == self.State.START):
                self.preview = self.getNextTetronimo()
                #self.preview = self.Tetronimo.Z
                self.state = self.State.NEW_TETRONIMO
                self.score = 0
                self.level = 0
            elif (self.state == self.State.NEW_TETRONIMO):
                self.dropCount = self.getDropCount()
                self.atBottom = False
                self.soft = 0
                self.lockDelayCount = self.DELAY_LOCK
                self.areDelayCount = self.DELAY_ARE
                if (not self.addTetronimoTop(self.preview)):
                    self.state = self.State.END
                else:
                    self.preview = self.getNextTetronimo()
                    self.state = self.State.FALLING
            elif (self.state == self.State.FALLING):
                if ((self.controlA and not self.controlALast) or (self.controlC and not self.controlCLast)):
                    self.rotate(1)
                elif (self.controlB and not self.controlBLast):
                    self.rotate(0)

                if (self.controlLeft and ((not self.controlLeftLast) or (self.controlLeftCount == 0))):
                    self.moveHoriz(0)
                elif (self.controlRight and ((not self.controlRightLast) or (self.controlRightCount == 0))):
                    self.moveHoriz(1)

                if (self.dropCount == 0 or self.controlDown):
                    self.dropCount = self.getDropCount()
                    if (not self.moveDown(self.getDropFrameCount())):
                        self.atBottom = True
                else:
                    self.dropCount -= 1
                    
                #if (self.dropCount == 0 or self.controlDown):
                #    if (self.moveDown(1)):
                #        self.dropCount = 60
                #    else:
                #        self.atBottom = True
                #else:
                #    self.dropCount -= 1

                if (self.atBottom):
                    if ((self.lockDelayCount == 0) or self.controlDown):
                        self.areDelayCount = self.DELAY_ARE
                        self.state = self.State.LOCKED
                        self.activeTetronimo = None
                    else:
                        self.lockDelayCount -= 1

                if (self.controlDown):
                    self.soft += 1

                self.controlALast = self.controlA
                self.controlBLast = self.controlB
                self.controlCLast = self.controlC
                self.controlLeftLast = self.controlLeft
                self.controlRightLast = self.controlRight
                self.controlDownLast = self.controlDown

                if (self.controlLeft):
                    if (self.controlLeftCount > 0):
                        self.controlLeftCount -= 1
                else:
                    self.controlLeftCount = self.DELAY_DAS

                if (self.controlRight):
                    if (self.controlRightCount > 0):
                        self.controlRightCount -= 1
                else:
                    self.controlRightCount = self.DELAY_DAS
                
            elif (self.state == self.State.LOCKED):
                if (self.areDelayCount == self.DELAY_ARE):
                    self.checkLines()
                    
                if (self.areDelayCount == 0):
                    self.state = self.State.NEW_TETRONIMO
                else:
                    self.areDelayCount -= 1
                
            elif (self.state == self.State.END):
                self.ended = True
                    
        elif (self.gameType == self.GameType.SCREENSAVER_0):
            if (self.frame % 15 == 0):
                self.addRandom()
        elif (self.gameType == self.GameType.SCREENSAVER_1):
            if (self.frame % 15 == 0):
                self.clearGrid()
                self.addRandom()
        elif (self.gameType == self.GameType.SCREENSAVER_2):
            if (self.frame % 1 == 0):
                self.activeTetronimo = None
                self.checkLines()
                if (self.clear):
                    self.clearGrid()
                    self.clear = False
                elif (not self.addRandomClean(100000)):
                    self.clear = True
                    #self.capture = True
        self.frame += 1
