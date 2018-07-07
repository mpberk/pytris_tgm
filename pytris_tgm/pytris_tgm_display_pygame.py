
import pygame as pg
from pytris_tgm import Engine

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)

tetronimoColors = {
    Engine.Tetronimo.T:(   0, 255, 255), # T - light blue
    Engine.Tetronimo.J:(   0,   0, 255), # J - dark blue
    Engine.Tetronimo.L:( 255, 191,   0), # L - orange
    Engine.Tetronimo.Z:(   0, 255,   0), # Z - green
    Engine.Tetronimo.S:( 191,   0, 255), # S - purple
    Engine.Tetronimo.I:( 255,   0,   0), # I - red
    Engine.Tetronimo.O:( 255, 255,   0)} # O - yellow

class PytrisTGMDisplay:

    def __init__(self):
        pg.init()
        self.game = Engine()
        self.SIXTYHERTSEVENT = pg.USEREVENT+1
        pg.time.set_timer(self.SIXTYHERTSEVENT, 17)
        self.NUM_COLS = 10
        self.NUM_ROWS = 20

        self.done = False
        self.clock = pg.time.Clock()

    #def __del__(self):
    #    pg.quit()

    def setupWindow(self):
        self.colorBorder = ( 100, 100, 100)
        self.colorField = ( 50, 50, 50)
        self.sizeSquare = 20
        self.sizeBorder = 5
        self.sizePreview = 4 * self.sizeSquare
        self.heightStart = self.sizePreview
        self.heightEnd = 10
        self.widthStart = 10
        self.widthEnd = 10
        self.windowWidth = self.widthStart + self.widthEnd + 2*self.sizeBorder + self.NUM_COLS*self.sizeSquare #+ 50
        self.windowHeight = self.heightStart + self.heightEnd + 2*self.sizeBorder + self.NUM_ROWS*self.sizeSquare
        self.size = (self.windowWidth,self.windowHeight)

        self.screen = pg.display.set_mode(self.size)
        pg.display.set_caption("PytrisTGM")

    def setupPytrisTGM(self):
        self.game = Engine()
        self.game.NUM_COLS = self.NUM_COLS
        self.game.NUM_ROWS = self.NUM_ROWS

    def drawField(self):
        width = 2*self.sizeBorder + self.NUM_COLS * self.sizeSquare
        height = 2*self.sizeBorder + self.NUM_ROWS * self.sizeSquare
        pg.draw.rect(self.screen, self.colorBorder, [self.widthStart,
                                                         self.heightStart,
                                                         width,
                                                         height])
        width = self.NUM_COLS * self.sizeSquare
        height = self.NUM_ROWS * self.sizeSquare
        pg.draw.rect(self.screen, self.colorField, [self.widthStart+self.sizeBorder,
                                                        self.heightStart+self.sizeBorder,
                                                        width,
                                                        height])

    def drawLines(self):
        width = self.widthStart + self.sizeBorder + self.sizeSquare - 1
        height = self.heightStart + self.sizeBorder
        heightSize = self.NUM_ROWS * self.sizeSquare
        for x in range(self.NUM_COLS-1):
            widthNew = width + x * self.sizeSquare
            pg.draw.rect(self.screen, self.colorBorder, [widthNew,
                                                             height,
                                                             2,
                                                             heightSize])
        width = self.widthStart + self.sizeBorder
        height = self.heightStart + self.sizeBorder + self.sizeSquare - 1
        widthSize = self.NUM_COLS *self. sizeSquare
        for y in range(self.NUM_ROWS-1):
            heightNew = height + y * self.sizeSquare
            pg.draw.rect(self.screen, self.colorBorder, [width,
                                                             heightNew,
                                                             widthSize,
                                                             2])

    def drawSquareAt(self, gridX, gridY, color):
        x = self.widthStart  + self.sizeBorder + (gridX) * self.sizeSquare
        y = self.heightStart + self.sizeBorder + (self.NUM_ROWS - gridY - 1) * self.sizeSquare
        pg.draw.rect(self.screen, tetronimoColors[color], [x,
                                                               y,
                                                               self.sizeSquare,
                                                               self.sizeSquare])

    def drawLevel(self):
        if (self.game.state == self.game.State.END):
            levelString = "End: {0}".format(self.game.level)
        else:
            levelString = str(self.game.level)
        level = pg.font.Font(None,20).render(levelString, True, WHITE)
        x = self.windowWidth - 70
        y = 5
        self.screen.blit(level, (x, y))

    def drawScore(self):
        if (self.game.state == self.game.State.END):
            scoreString = "End: {0}".format(self.game.score)
        else:
            scoreString = str(self.game.score)
        score = pg.font.Font(None,20).render(scoreString, True, WHITE)
        x = self.windowWidth - 70
        y = 20
        self.screen.blit(score, (x, y))

    def drawFPS(self):
        fps = pg.font.Font(None,20).render(str(int(self.clock.get_fps())), True, WHITE)
        x = 5
        y = 5
        self.screen.blit(fps, (x, y))
        
    def drawState(self):
        if (self.game.state == 0):
            stateString = "Start"
        elif (self.game.state == 1):
            stateString = "New Tetronimo"
        elif (self.game.state == 2):
            stateString = "Falling"
        elif (self.game.state == 3):
            stateString = "Locked"
        elif (self.game.state == 4):
            stateString = "End"
        state = pg.font.Font(None,20).render(stateString, True, WHITE)
        x = self.windowWidth - 70
        y = 35
        self.screen.blit(state, (x, y))

    def drawTest(self):
        stringTest = pg.font.Font(None,20).render(str(self.game.dropCount), True, WHITE)
        x = 5
        y = 20
        self.screen.blit(stringTest, (x, y))

    def drawGrid(self, grid):
        for x in range(self.NUM_COLS):
            for y in range(self.NUM_ROWS):
                color = grid[y][x]
                if (color != None):
                    self.drawSquareAt(x, y, color)

    def drawPreview(self):
        if (self.game.preview != None):
            for i in range(4):
                x = self.game.START_OFFSET + self.game.tetronimoStartOffset[self.game.preview] + self.game.tetronimoRotations[self.game.preview][0][i][0]
                y = self.game.NUM_ROWS + 2 - self.game.tetronimoRotations[self.game.preview][0][i][1]
                xloc = self.widthStart + self.sizeBorder - 1 + self.sizeSquare * x
                yloc = self.sizeBorder + self.sizeSquare * (1 + self.game.tetronimoRotations[self.game.preview][0][i][1]) - 1
                self.drawSquareAt(x,y,self.game.preview)

                length = self.sizeSquare + 2
                pg.draw.rect(self.screen, self.colorBorder, [xloc,
                                                                 yloc,
                                                                 length,
                                                                 2])
                pg.draw.rect(self.screen, self.colorBorder, [xloc,
                                                                 yloc + self.sizeSquare,
                                                                 length,
                                                                 2])
                pg.draw.rect(self.screen, self.colorBorder, [xloc,
                                                                 yloc,
                                                                 2,
                                                                 length])
                pg.draw.rect(self.screen, self.colorBorder, [xloc + self.sizeSquare,
                                                                 yloc,
                                                                 2,
                                                                 length])

    def eventLogic(self):
        for event in pg.event.get(): # User did something
            if event.type == pg.QUIT: # If user clicked close
                self.done = True
            if event.type == self.SIXTYHERTSEVENT: # 60 Hz event
                self.game.nextFrame()
                pass
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.game.controlLeft = True
                if event.key == pg.K_RIGHT:
                    self.game.controlRight = True
                if event.key == pg.K_DOWN:
                    self.game.controlDown = True
                if event.key == pg.K_z:
                    self.game.controlA = True
                if event.key == pg.K_x:
                    self.game.controlB = True
                if event.key == pg.K_c:
                    self.game.controlC = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    self.game.controlLeft = False
                if event.key == pg.K_RIGHT:
                    self.game.controlRight = False
                if event.key == pg.K_DOWN:
                    self.game.controlDown = False
                if event.key == pg.K_z:
                    self.game.controlA = False
                if event.key == pg.K_x:
                    self.game.controlB = False
                if event.key == pg.K_c:
                    self.game.controlC = False
                

    def gameLogic(self):
        if (self.game.capture):
            name = "screenshot_{0}.jpeg".format(self.game.frame)
            pg.image.save(self.screen, name)
            print("Saved screenshot: {0}".format(name))
            self.game.capture = False

    def drawGame(self):
        self.screen.fill(BLACK)

        self.drawField()
        self.drawGrid(self.game.grid)
        self.drawLines()
        self.drawPreview()
        self.drawFPS()
        self.drawState()
        self.drawScore()
        self.drawLevel()
        self.drawTest()
        
        # Update the screen with what we've drawn
        pg.display.flip()

    def gameLoop(self):
        self.done = False
        # Main Program Loop
        while not self.done:
            
            self.eventLogic()

            self.gameLogic()

            self.drawGame()

            # Limit to 60 frams per second
            self.clock.tick(60)
        pg.quit()

    def start(self):
        self.setupPytrisTGM()
        self.setupWindow()
        self.game.newGame()
        self.game.gameType = self.game.GameType.NORMAL
        self.gameLoop()

def main():
    display = PytrisTGMDisplay()
    display.start()
    
if __name__ == '__main__':
    main()
