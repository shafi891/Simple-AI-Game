import random, pygame,sys
from pygame.locals import*
#from Tkinter import*
#from PIL import ImageTk,Image

FPS =100
Winwidth = 640
Winheight = 480
Bodysize = 40
assert Winwidth % Bodysize == 0, "Window width must be a multiple of cell size."
assert Winheight % Bodysize == 0, "Window height must be a multiple of cell size."
Bodywidth = int(Winwidth / Bodysize )
Bodyheight = int(Winheight / Bodysize )

#        R    G    B
White = (255,255,255)
Black = (0,0,0)
Red = (255,0,0)
Green = (0,255,0)
Darkgreen = (0,155,0)
Darkgrey = (40,40,40)
Bgcolor= Black

UP ='up'
DOWN='down'
LEFT='left'
RIGHT='right'

HEAD = 0

def main():
    global FPSclock, DispSurf, Basicfont

    pygame.init()
    FPSclock= pygame.time.Clock()
    DispSurf = pygame.display.set_mode((Winwidth, Winheight))
    Basicfont = pygame.font.Font('freesansbold.ttf', 20)
    pygame.display.set_caption('Snake Game ')

    ShowStartScreen()
    while True:
        runGame()
        ShowGameOverScreen()

def get_direction(head_, last_direction):
    if head_['x'] == 1:
        if head_['y'] == Bodyheight - 1:
            return LEFT
        elif head_['y'] == 0:
            return RIGHT
        if last_direction == LEFT:
            return DOWN
        elif last_direction == DOWN:
            return RIGHT
    elif head_['x'] >= 1 and head_['x'] <= Bodywidth-2:
        if last_direction == RIGHT:
            return RIGHT
        elif last_direction == LEFT:
            return LEFT
    elif head_['x'] == (Bodywidth-1):
        if last_direction == RIGHT:
            return DOWN
        elif last_direction == DOWN:
            return LEFT
    elif head_['x'] == 0:
        if head_['y'] != 0:
            return UP
        else:
            return RIGHT


def runGame():
    #random start point.
    startx = random.randint(0, Bodywidth -1)
    starty = random.randint(0, Bodyheight -1)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    #apple in a random place.
    apple = getRandomLocation(wormCoords)

    while True:
        # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
        direction = get_direction(wormCoords[0], direction)

        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == Bodywidth or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == Bodyheight:
            return
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return


        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:

            apple = getRandomLocation(wormCoords) # set a apple
        else:
            del wormCoords[-1]


        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DispSurf.fill(Bgcolor)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        FPSclock.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = Basicfont.render('Press any key to play the game.', True, Red)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (Winwidth - 480, Winheight - 30)
    DispSurf.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def ShowStartScreen():
    #app_root =Tk()
    #img=ImageTk.photoImage(Image.open("th.jpeg"))
    #imglabel = Label(app_root, image=img).grid(row=1, column=1)
    #app_root.mainloop()

    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Snake !', True, White, Darkgreen)
    titleSurf2 = titleFont.render('Snake ', True, Green)

    degrees1 = 0
    degrees2 = 0
    while True:
        DispSurf.fill(Bgcolor)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (Winwidth / 2, Winheight / 2)
        DispSurf.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (Winwidth / 2, Winheight / 2)
        DispSurf.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        #FPSCLOCK.tick(FPS)
        degrees1 += 0
        degrees2 += 10 # rotate by 10 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation(worm):
    temp = {'x': random.randint(0, Bodywidth - 1), 'y': random.randint(0, Bodyheight - 1)}
    while test_not_ok(temp, worm):
        temp = {'x': random.randint(0, Bodywidth - 1), 'y': random.randint(0, Bodyheight - 1)}
    return temp

def test_not_ok(temp, worm):
    for body in worm:
        if temp['x'] == body['x'] and temp['y'] == body['y']:
            return True
    return False


def ShowGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, Red)
    overSurf = gameOverFont.render('Over', True, Red)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (Winwidth/ 2, 10)
    overRect.midtop = (Winwidth / 2, gameRect.height + 10 + 25)

    DispSurf.blit(gameSurf, gameRect)
    DispSurf.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

def drawScore(score):
    scoreSurf = Basicfont.render('Score: %s' % (score), True, Red)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (Winwidth - 120, 10)
    DispSurf.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * Bodysize
        y = coord['y'] * Bodysize
        wormSegmentRect = pygame.Rect(x, y, Bodysize, Bodysize)
        pygame.draw.rect(DispSurf, Darkgreen, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, Bodysize - 8, Bodysize - 8)
        pygame.draw.rect(DispSurf, Green, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * Bodysize
    y = coord['y'] * Bodysize
    appleRect = pygame.Rect(x, y, Bodysize, Bodysize)
    pygame.draw.rect(DispSurf, Red, appleRect)


def drawGrid():
    for x in range(0, Winwidth, Bodysize): #draw vertical lines
        pygame.draw.line(DispSurf, Darkgrey, (x, 0), (x, Winheight))
    for y in range(0, Winheight, Bodysize): #draw horizontal lines
        pygame.draw.line(DispSurf, Darkgrey, (0, y), (Winwidth, y))


if __name__ == '__main__':
    main()
