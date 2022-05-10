import pygame
import numpy as np
import random
import math
import copy
import time
from random import choice

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ROWS = 50
Width = 800
sizeOfSquare = (Width / ROWS)


def findPath(board, end):
    xx = 0
    finding = True
    maxValue = np.amax(board)
    resetpl = 0
    cordx, cordy = np.where(board == maxValue)
    startx, starty = np.where(board == 1)
    counter = maxValue + 1

    for i in range(len(cordx)):
        kx = 0

        if cordx[i] + 1 < ROWS:
            if board[cordx[i] + 1, cordy[i]] == 0:
                board[cordx[i] + 1, cordy[i]] = counter

                xx += 1

        if cordx[i] - 1 > -1:
            if board[cordx[i] - 1, cordy[i]] == 0:
                board[cordx[i] - 1, cordy[i]] = counter
                xx += 1

        if cordy[i] + 1 < ROWS:
            if board[cordx[i], cordy[i] + 1] == 0:
                board[cordx[i], cordy[i] + 1] = counter
                xx += 1

        if cordy[i] - 1 > -1:
            if board[cordx[i], cordy[i] - 1] == 0:
                board[cordx[i], cordy[i] - 1] = counter
                xx += 1

    if kx == xx:
        print("stop i systememt!!!")
        print("stop i systememt!!!")
        print("stop i systememt!!!")
        board = fixFail(board, [end[0], end[1]])
        board[startx, starty] = 1
    return board


def fixFail(board, end):
    cdx, cdy = end[0], end[1]
    fix = True
    shortestdist = 20000
    cord = []

    for i in range(ROWS):
        for j in range(ROWS):
            if board[i, j] > 0:
                distance = abs(i - cdx) + abs(j - cdy)
                if distance < shortestdist:
                    shortestdist = distance
                    cord = [i, j]
    print(shortestdist)
    while fix:
        print(cord)
        if cord[0] == cdx and cord[1] == cdy:
            print("fixat?")
            print((cdx, cdy))
            print(cord[0], cord[1])
            break
        elif cdx > cord[0]:
            cord[0] += 1
            board[cord[0], cord[1]] = 0
            pygame.draw.rect(screen, (0, 0, 0), (
                (int(cord[0] * sizeOfSquare)), (int(cord[1] * sizeOfSquare)), int(sizeOfSquare - 1),
                int(sizeOfSquare - 1)))
        elif cdx < cord[0]:
            cord[0] -= 1
            board[cord[0], cord[1]] = 0
            pygame.draw.rect(screen, (0, 0, 0), (
                (int(cord[0] * sizeOfSquare)), (int(cord[1] * sizeOfSquare)), int(sizeOfSquare - 1),
                int(sizeOfSquare - 1)))
        elif cdy > cord[1]:
            cord[1] += 1
            board[cord[0], cord[1]] = 0
            pygame.draw.rect(screen, (0, 0, 0), (
                (int(cord[0] * sizeOfSquare)), (int(cord[1] * sizeOfSquare)), int(sizeOfSquare - 1),
                int(sizeOfSquare - 1)))
        elif cdy < cord[1]:
            cord[1] -= 1
            board[cord[0], cord[1]] = 0
            pygame.draw.rect(screen, (0, 0, 0), (
                (int(cord[0] * sizeOfSquare)), (int(cord[1] * sizeOfSquare)), int(sizeOfSquare - 1),
                int(sizeOfSquare - 1)))

    clearmatrix(board)
    return board


def phasedraw(board, startP, endP):
    board[endP[0], endP[1]] = 0
    board[startP[0], startP[1]] = 1
    Pathing = True
    adda = 1
    while Pathing:
        if adda == 1:

            board = findPath(board, [endP[0], endP[1]])

            if board[endP[0], endP[1]] > 0:
                adda = 2
        if adda == 2:
            fillPath(board, [endP[0], endP[1]])
            board = clearmatrix(board)
            Pathing = False

    return validPath + C1


def clearmatrix(board):
    board[ROWS - 1, ROWS - 1] = 0
    for i in range(ROWS):
        for j in range(ROWS):
            if board[i, j] > 0:
                board[i, j] = 0

    # board[checkpoint[0],checkpoint[1]] = 1

    return board


def fillPath(board, endpoint):
    print("BAM")

    copyX = copy.copy(endpoint[0])
    copyY = copy.copy(endpoint[1])
    currValue = board[copyX, copyY]
    Xxx = copyX
    Yyy = copyY
    global validPath
    validPath = []
    alternativ = []
    currOption = 0
    currOpt = []

    while currValue != 1:
        currOpt = []
        if Yyy + 1 < ROWS:
            if board[Xxx, Yyy + 1] == currValue - 1:
                currOption += 16
                currOpt.append(16)

        if Yyy - 1 > -1:
            if board[Xxx, Yyy - 1] == currValue - 1:
                currOption += 8
                currOpt.append(8)
        if Xxx - 1 > -1:
            if board[Xxx - 1, Yyy] == currValue - 1:
                currOption += 4
                currOpt.append(4)

        if Xxx + 1 < ROWS:
            if board[Xxx + 1, Yyy] == currValue - 1:
                currOption += 2
                currOpt.append(2)
        route = choice(currOpt)

        if currOption > 0:

            if route == 16:
                # alternativ.append(currOption-16)
                validPath.append("u")
                currValue -= 1
                Yyy += 1
                currOption = 0

            elif route == 8:
                # alternativ.append(currOption-8)
                validPath.append("n")
                currValue -= 1
                Yyy -= 1
                currOption = 0

            elif route == 4:
                # alternativ.append(currOption-4)
                validPath.append("h")
                currValue -= 1
                Xxx -= 1
                currOption = 0

            elif route == 2:
                # alternativ.append(currOption-2)
                validPath.append("v")
                currValue -= 1
                Xxx += 1
                currOption = 0
            elif currOption == 0:
                return

        # print(currValue)

        # pygame.draw.rect(screen, (0,0,0), (
        #   (int(Xxx * sizeOfSquare)), (int(Yyy * sizeOfSquare)), int(sizeOfSquare - 1), int(sizeOfSquare - 1)))

        pygame.display.update()


def checkPointFinder(board):
    schackmatt = np.min(board)
    Rangg = int(schackmatt * -0.1)
    print(schackmatt)
    cordzx = []
    cordzy = []

    for i in range(Rangg):
        checkpointy = np.where(grid == int(schackmatt + 10 * i))
        pygame.draw.rect(screen, (255, 255, 255), (
            (int(checkpointy[0] * sizeOfSquare)), (int(checkpointy[1] * sizeOfSquare)), int(sizeOfSquare - 1),
            int(sizeOfSquare - 1)))
        screen.blit(myFont.render(str(i + 1), 1, (0, 0, 0)),
                    (int(checkpointy[0] * sizeOfSquare) + 3, int(checkpointy[1] * sizeOfSquare)-2))
        pygame.display.update()
        cordzx.append(checkpointy[0])
        cordzy.append(checkpointy[1])

    return cordzx, cordzy


def drawGame(screen):
    screen.fill(WHITE)
    pygame.display.update()

    for i in range(ROWS):
        for j in range(ROWS):
            pygame.draw.rect(screen, BLACK, (
                (int(i * sizeOfSquare)), (int(j * sizeOfSquare)), int(sizeOfSquare - 1), int(sizeOfSquare - 1)))
            pygame.display.update()
    grid = np.zeros((ROWS, ROWS))
    checkPoints = random.randint(2, 5)
    for i in range(checkPoints):
        checkPoint1X = random.randint(5, ROWS - 4)
        checkPoint1Y = random.randint(5, ROWS - 4)
        grid[checkPoint1X, checkPoint1Y] = -10 * i - 10
        print(-10 * i)
    pygame.draw.rect(screen, (10, 10, 10), (
        (int(Width + (Width / 12)) - 3), (int(Width - (Width / 6) - 3)), int((Width / 6) + 6), int((Width / 10) + 6)))
    pygame.draw.rect(screen, (10, 200, 10), (
        (int(Width + (Width / 12))), (int(Width - (Width / 6))), int(Width / 6), int(Width / 10)))

    pygame.display.update()

    print(np.min(grid))
    return grid


def updateDrawing(grid, COLOR):
    for i in range(ROWS):
        for j in range(ROWS):
            if grid[i, j] > 0:
                pygame.draw.rect(screen, COLOR, (
                    (int(i * sizeOfSquare)), (int(j * sizeOfSquare)), int(sizeOfSquare - 1), int(sizeOfSquare - 1)))

    pygame.draw.rect(screen, (0, 0, 255), (
        (int(end[0] * sizeOfSquare)), (int(end[1] * sizeOfSquare)), int(sizeOfSquare - 1), int(sizeOfSquare - 1)))


size = (Width + int(Width / 3), Width)
pygame.init()
drawphase = 0
end = (10, 10)
start = [ROWS - 1, ROWS - 1]
myFont = pygame.font.SysFont("Times New Roman", 16, 0, 0)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Väghittarspel")
grid = drawGame(screen)
clock = pygame.time.Clock()
Sparpunkterx, Sparpunktery = checkPointFinder(grid)
gameOn = True
counter = 0
C1 = []

pygame.draw.rect(screen, (0, 0, 255), (
    (int(end[0] * sizeOfSquare)), (int(end[1] * sizeOfSquare)), int(sizeOfSquare - 1), int(sizeOfSquare - 1)))

while gameOn:
    clock.tick(60)

    if drawphase == 3:

        for i in range(len(Sparpunkterx)):

            if i == 0:
                C1 = phasedraw(grid, start, [Sparpunkterx[0], Sparpunktery[0]])
            else:
                C1 = phasedraw(grid, [Sparpunkterx[i - 1], Sparpunktery[i - 1]], [Sparpunkterx[i], Sparpunktery[i]])


        C1 = phasedraw(grid, [Sparpunkterx[len(Sparpunkterx) - 1], Sparpunktery[len(Sparpunkterx) - 1]],
                        [end[0], end[1]])
        xx = start[0]
        yy = start[1]
        listerx = []
        listery = []
        listerx.append(xx)
        listery.append(yy)
        delay_timer = 1000
        path = C1[::-1]
        stepy = len(path)
        step = 0
        drawphase = 4
        RGB = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.rect(screen, (255, 255, 255), (int(Width), int(Width/6), Width/4, int(Width/6)))
        screen.blit(myFont.render(str(len(path)) +" Path Length", 1, (0, 0, 0)),
                    (int(Width + Width/6),int(Width/6)))

    if drawphase == 4:

        for k in range(len(Sparpunkterx)):
            pygame.draw.rect(screen, (255, 255, 255), (
                (int(Sparpunkterx[k] * sizeOfSquare)), (int(Sparpunktery[k] * sizeOfSquare)), int(sizeOfSquare - 1),
                int(sizeOfSquare - 1)))
            screen.blit(myFont.render(str(k + 1), 1, (0, 0, 0)),
                        (int(Sparpunkterx[k] * sizeOfSquare) + 3, int(Sparpunktery[k] * sizeOfSquare)-3))
        drawphase = 5

    if drawphase == 5:
        clock.tick(30)

        if step == 0:
            pygame.draw.rect(screen, (0, 0, 255), (
                (int(start[0] * sizeOfSquare)), (int(start[1] * sizeOfSquare)), int(sizeOfSquare - 1),
                int(sizeOfSquare - 1)))

        if path[step] == "v":
            xx -= 1
            listerx.insert(0, xx)
            listery.insert(0, yy)
            for i in range(delay_timer):
                pygame.draw.rect(screen, RGB, (
                    (int((xx + 1) * sizeOfSquare)), (int(yy * sizeOfSquare)), int(sizeOfSquare - 1),
                    int(sizeOfSquare - 1)))

        if path[step] == "h":
            xx += 1
            listerx.insert(0, xx)
            listery.insert(0, yy)
            for i in range(delay_timer):
                pygame.draw.rect(screen, RGB, (
                    (int((xx - 1) * sizeOfSquare)), (int(yy * sizeOfSquare)), int(sizeOfSquare - 1),
                    int(sizeOfSquare - 1)))

        if path[step] == "u":
            yy -= 1
            listerx.insert(0, xx)
            listery.insert(0, yy)
            for i in range(delay_timer):
                pygame.draw.rect(screen, RGB, (
                    (int(xx * sizeOfSquare)), int((yy + 1) * sizeOfSquare), int(sizeOfSquare - 1),
                    int(sizeOfSquare - 1)))
        if path[step] == "n":
            yy += 1
            listerx.insert(0, xx)
            listery.insert(0, yy)
            for i in range(delay_timer):
                pygame.draw.rect(screen, RGB, (
                    (int(xx * sizeOfSquare)), int((yy -1) * sizeOfSquare), int(sizeOfSquare - 1),
                    int(sizeOfSquare - 1)))
        if step > 3:
            pygame.draw.rect(screen, (0, 0, 0), (
                (int(listerx[5] * sizeOfSquare)), (int(listery[5] * sizeOfSquare)), int(sizeOfSquare - 1),
                int(sizeOfSquare - 1)))
            listerx.pop()
            listery.pop()
        if step > stepy - 2:
            for k in range(len(listerx)):
                pygame.draw.rect(screen, (0, 0, 0), (
                    (int(listerx[k] * sizeOfSquare)), (int(listery[k] * sizeOfSquare)), int(sizeOfSquare - 1),
                    int(sizeOfSquare - 1)))
            print("jadå")
            updateDrawing(grid, BLACK)
            drawphase = 0
            print(stepy)
        else:

            step += 1
            drawphase = 4

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
            pygame.quit()
        if drawphase == 0:
            C1 = []
        if event.type == pygame.MOUSEBUTTONDOWN and drawphase == 0:
            drawphase = 1

        if event.type == pygame.MOUSEBUTTONUP and drawphase == 1:
            drawphase = 0

        if drawphase == 1 and pygame.MOUSEMOTION and event.pos[0] > int(Width + (Width / 12)) and event.pos[1] > int(
                Width - (Width / 6)):
            if event.pos[0] < int(Width + (Width / 12) + (Width / 6)) and event.pos[1] < int(
                    Width - (Width / 6) + (Width / 10)):
                drawphase = 3
        if drawphase == 1 and pygame.MOUSEMOTION and event.pos[0] < Width and event.pos[1] < Width:

            xpos = int(math.floor(event.pos[0] / sizeOfSquare))
            ypos = int(math.floor(event.pos[1] / sizeOfSquare))

            if xpos == end[0] and ypos == end[1]:
                pygame.draw.rect(screen, (0, 0, 255), (
                    (int(xpos * sizeOfSquare)), (int(ypos * sizeOfSquare)), int(sizeOfSquare - 1),
                    int(sizeOfSquare - 1)))
            if grid[xpos, ypos] > -9:
                pygame.draw.rect(screen, (255, 255, 0), (
                    (int(xpos * sizeOfSquare)), (int(ypos * sizeOfSquare)), int(sizeOfSquare - 1),
                    int(sizeOfSquare - 1)))
                grid[xpos, ypos] = -1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                drawphase = 3

    pygame.display.update()
