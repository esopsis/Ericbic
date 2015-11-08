from __future__ import division
import pygame, sys
from pygame.locals import *
pygame.init()

""" ericbic.py
by Eric J.Parfitt (ejparfitt@gmail.com)

This program is designed for coding and decoding the roman alphabet
into and out of a character set I made up.  My characters are all made
up of either one or two of a set of four different character parts which
can be combined in different ways to get a total of 30 new characters.

Version: 1.0 alpha
"""

WIDTH = 500
HEIGHT = 400

windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 60
clock = pygame.time.Clock()

class Icon:
    def __init__(self, image, position=(0, 0)):
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

class Canvas:
    def __init__(self):
        self.isTop = self.isBottom = self.isFlipped = self.isReset = False
        self.text = None
        self.bottomHalf = None
        self.topHalf = None
        
    def getIcon(self, pallet, mouseLoc):
        for i in range(len(pallet)):
            icon = pallet[i]
            if icon.rect.collidepoint(mouseLoc):
                newIcon = Icon(icon.image)
                return newIcon, i
        return None, None
    
    def tryAdd(self, pallet, mouseLoc, position):
        for i in range(len(pallet)):
            icon = pallet[i]
            if icon.rect.collidepoint(mouseLoc):
                newIcon = Icon(icon.image, position)
                windowSurface.blit(newIcon.image, newIcon.rect)
                return i

    def moveBottomHalf(self, bottomHalf, topHalf):
        self.bottomHalf.rect.topleft = self.topHalf.rect.bottomright
        self.bottomHalf.rect.move_ip(0, -int(round(CURVE_WIDTH)))
            
    def update(self, isClick, letter):
        mouseLoc = pygame.mouse.get_pos()
        if letter is not None:
            if self.isFlipped:
                for icon in pallet:
                    icon.image = pygame.transform.flip(icon.image, False,
                                True)
                    pygame.draw.rect(windowSurface, WHITE, icon.rect)
                    windowSurface.blit(icon.image, icon.rect)
                self.isFlipped = False
            letter = letter.capitalize()
            row, col = next(((i, row.index(letter)) for i, row in
                    enumerate(alphabet) if letter in row), (None, None))
            if row is not None:
                self.isReset = True
                oldTopHalf = self.topHalf
                oldBottomHalf = self.bottomHalf
                self.topHalf = Icon(pallet[row].image, TOP_CO)
                if col != 0:
                    self.bottomHalf = Icon(pallet[col - 1].image)
                    self.moveBottomHalf(self.bottomHalf, self.topHalf)
                else:
                    self.bottomHalf = None
                if self.topHalf is not None:
                    for icon in [oldTopHalf, oldBottomHalf]:
                        if icon is not None:
                            pygame.draw.rect(windowSurface, WHITE,
                                        icon.rect)
                    windowSurface.blit(self.topHalf.image,
                            self.topHalf.rect)
                    if self.bottomHalf is not None:
                        self.bottomHalf.image = pygame.transform.flip(
                                self.bottomHalf.image, False, True)
                        windowSurface.blit(self.bottomHalf.image,
                                self.bottomHalf.rect)
                if self.text is not None:
                    pygame.draw.rect(windowSurface, WHITE, self.text.rect) 
                self.text = Icon(font.render(letter, True, BLACK), (300, 300))
                windowSurface.blit(self.text.image, self.text.rect)
                pygame.display.flip() 
            letter = None
        elif isClick:
            newIcon, index = (self.getIcon(pallet, mouseLoc))
            if newIcon is not None:
                if self.isReset:
                    for icon in [self.topHalf, self.bottomHalf]:
                        if icon is not None:
                            pygame.draw.rect(windowSurface, WHITE,
                                    icon.rect)
                    self.isTop = self.isBottom = self.isReset = False
                if not (self.isTop and self.isBottom):
                    if not self.isTop:
                        self.isTop = True
                        self.topHalf = newIcon
                        self.topIndex = index
                        self.topHalf.rect.topleft = TOP_CO
                        windowSurface.blit(self.topHalf.image,
                                self.topHalf.rect)
                        letter = alphabet[self.topIndex][0]
                    else:
                        self.isBottom = True
                        self.bottomHalf = newIcon
                        bottomIndex = index
                        self.moveBottomHalf(self.bottomHalf, self.topHalf)
                        windowSurface.blit(self.bottomHalf.image,
                                self.bottomHalf.rect)
                        letter = alphabet[self.topIndex][bottomIndex + 1]
                        self.isReset = True
                    if self.text is not None:
                        pygame.draw.rect(windowSurface, WHITE, self.text.rect) 
                    self.text = Icon(font.render(letter, True, BLACK),
                            (300, 300))
                    for icon in pallet:
                        #if icon is not None:
                        pygame.draw.rect(windowSurface, WHITE, icon.rect)
                        icon.image = pygame.transform.flip(icon.image, False,
                                True)
                        windowSurface.blit(icon.image, icon.rect)
                    self.isFlipped = not self.isFlipped
                    windowSurface.blit(self.text.image, self.text.rect)
                    pygame.display.flip()
            letter = None
        clock.tick(FPS)
        return letter

windowSurface.fill(WHITE)
imageFiles = ["EribicBump.png", "EribicSpike.png", "EribicLoop.png",
        "EribicLeftWave.png", "EribicRightWave.png"]
pallet = [Icon(pygame.image.load(image)) for image in imageFiles]
noneSymbol = "?"
alphabet =  [["N", "U", "M", "R", "F", noneSymbol],
        ["I", "C", "T", "J", "V", "G"], ["E", "L", "H", "O", "K", "B"],
        ["A", "D", "Y", "Q", noneSymbol, "W"],
        ["S", noneSymbol, "P", "Z", "X", noneSymbol]]
letter = None
font = pygame.font.SysFont("comicsansms", 72)
ICON_HEIGHT = 50
ORIGINAL_ICON_HEIGHT = 75.328
ORIGINAL_CURVE_WIDTH = 2.5
CURVE_WIDTH = (ICON_HEIGHT / ORIGINAL_ICON_HEIGHT) * ORIGINAL_CURVE_WIDTH
TOP_CO = (50, 200)
widthTotal = 0
for icon in pallet:
    width = icon.image.get_width() * ICON_HEIGHT / icon.image.get_height()
    icon.image = pygame.transform.smoothscale(icon.image, 
            (int(round(width)), ICON_HEIGHT))
    icon.rect = icon.image.get_rect()
    widthTotal += width
xLoc = 0
for i in range(len(pallet)):
    icon = pallet[i]
    icon.rect.x = xLoc
    windowSurface.blit(icon.image, icon.rect)
    xLoc += icon.image.get_width() + (WIDTH - widthTotal) / (len(pallet) - 1)
isFlipped = False
pygame.display.flip()
canvas = Canvas()

while(True):
    isClick = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                isClick = True
        elif event.type == KEYDOWN:
            if event.unicode.isalpha():
                letter = event.unicode
    letter = canvas.update(isClick, letter)
