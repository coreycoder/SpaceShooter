__author__ = 'azian'

import pygame
import time
from colors import *


spriteHeight = 64
spriteWidth = 64

class Player(pygame.sprite.Sprite):
    def __init__(self, color=white, width=spriteWidth, height=spriteHeight):
        super(Player, self).__init__()

        self.explosion = pygame.mixer.Sound("explosion.wav")
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.health = 1

    def setHealth(self, value):
        self.health = value
        self.explosion.play()
        if self.health <= 0:
            self.kill()

    def destroy(self):
        self.kill()

    def getHealth(self):
        return self.health

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_image(self, filename=None):
        if (filename != None):
            self.image = pygame.image.load(filename)
            self.rect = self.image.get_rect()

    def update_image(self, filename = None):
        if (filename != None):
            self.image = pygame.image.load(filename)


    def update(self, loopCount):
        if loopCount % 9 == 0:
            self.image = pygame.image.load("hero1Thrust.png")
        else:
            self.image = pygame.image.load("hero1Thrust2.png")

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y

class Bullet(pygame.sprite.Sprite):
    def __init__(self, color=white, width=spriteWidth, height=spriteHeight):
        super(Bullet, self).__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()


    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_image(self, filename = None):
        if (filename != None):
            self.image = pygame.image.load(filename)
            self.rect = self.image.get_rect()

    def update_image(self, filename = None):
        if (filename != None):
            self.image = pygame.image.load(filename)

    def checkCollision(self, object1, object2, spriteWidth=spriteWidth, spriteHeight=spriteHeight):
        #if pygame.sprite.collide_rect(self, object1):
        #if self.rect.collidrect(object1.rect):
        #col = pygame.sprite.collide_rect(object1, object2)
        #if col:
        if (object1.getX() >= object2.getX() and object1.getX() <= (object2.getX() + spriteWidth)) and \
                (object1.getY() >= object2.getY() and object1.getY() <= (object2.getY() + spriteHeight)):
            return True
        return False

    def update(self, type):
        if type == "player":
            self.rect.y -= 10
        elif type == "enemy":
            self.rect.y += 10

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y

    def destroy(self):
        self.rect.x = -1000
        self.rect.y = -1000
        self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, color=white, width=spriteWidth, height=spriteHeight):
        super(Enemy, self).__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.health = 1
        self.index = 0
        self.spriteCounter = 0

        self.explosion = pygame.mixer.Sound("explosion.wav")

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_image(self, filename=None):
        if (filename != None):
            self.image = pygame.image.load(filename)
            self.rect = self.image.get_rect()

    def set_rect(self, width, height):
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect

    def update_image(self, filename=None):
        if (filename != None):
            self.image = pygame.image.load(filename)

    def checkCollision(self, object1, object2, spriteWidth=spriteWidth, spriteHeight=spriteHeight):
        if (object1.getX() >= object2.getX() and object1.getX() <= (object2.getX() + spriteWidth)) and \
                (object1.getY() >= object2.getY() and object1.getY() <= (object2.getY() + spriteHeight)):
            return True
        return False

    def setSpriteCounter(self, value):
        self.spriteCounter = value

    def getSpriteCounter(self):
        return self.spriteCounter

    def set_Health(self, value):
        self.health = value

    def get_Health(self):
        return self.health

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y

    def decrement_Health(self):
        self.explosion.play()
        self.health -= 2

    def enemyDead(self):
        if self.health < 0:
            return True
        return False

    def destroy(self):
        #move rect out of window
        self.rect.x = -500
        self.rect.y = -500
        self.kill()

class Background(pygame.sprite.Sprite):
    def __init__(self, color=white, width=spriteWidth, height=spriteHeight):
        super(Background, self).__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_image(self, filename=None):
        if (filename != None):
            self.image = pygame.image.load(filename)
            self.rect = self.image.get_rect()

    def get_image(self):
        return self.image

    def get_size(self):
        return self.image.get_size()

    def get_rect(self):
        return self.image.get_rect()

def main():
    #initializes pygame
    pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=4096)
    x = pygame.init()
    #returns (6,0) : 6 successes, 0 failures
    print(x)

    windowWidth = 540
    windowHeight = 702

    #this returns a pygame surface object of given dimensions as a tuple argument
    gameDisplay = pygame.display.set_mode((windowWidth, windowHeight))

    #name of the game
    pygame.display.set_caption('Cool Space Shooter')

    #updates entire surface all at once
    #pygame.display.flip()

    playerWidth = 50
    playerHeight = 50
    playerMovedDistance = 10

    clock = pygame.time.Clock()
    fps = 60
    startMenuLoop = 0

    pygame.mixer.music.load("afterlife.mp3")
    gameLoop(windowWidth, windowHeight, gameDisplay, playerMovedDistance, playerWidth, playerHeight, clock, fps, startMenuLoop)

def message_to_screen(msg, color, font, gameDisplay, windowWidth):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [windowWidth/4, 50])

def gameLoop(windowWidth, windowHeight, gameDisplay, playerMovedDistance, playerWidth, playerHeight, clock, fps, startMenuLoop):

    pygame.mixer.music.play()
    processRunning = True
    gameOver = False

    playerXLocation = windowWidth/2
    playerYLocation = windowHeight - 100

    #returns font object to variable font
    font = pygame.font.SysFont(None, 20)

    block_group = pygame.sprite.Group()
    backgroundGroup = pygame.sprite.Group()
    exitScreenGroup = pygame.sprite.Group()
    startMenuGroup = pygame.sprite.Group()
    bulletGroup = pygame.sprite.Group()
    enemyBulletGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()
    player = Player()
    background = Background()
    background2 = Background()
    exitScreen = Background()
    startMenu = Background()
    missile = Bullet()
    missile2 = Bullet()
    enemyMissile = Bullet()
    enemyMissile2 = Bullet()
    playerFire = pygame.mixer.Sound("fire.wav")
    enemy = Enemy()

    background.set_image("starfield2.png")
    background2.set_image("starfield2.png")
    exitScreen.set_image("gameOver.png")
    startMenu.set_image("startMenu.png")
    player.set_image("hero1Thrust.png")
    playerImageList = ["hero1Thrust.png", "hero1Thrust2.png"]
    enemy.set_image("lightenemy2.png")

    deathAnimation = []
    deathAnimation.append("lightenemy3Death1.png")
    deathAnimation.append("lightenemy3Death2.png")
    deathAnimation.append("lightenemy3Death3.png")
    deathAnimation.append("lightenemy3Death4.png")
    deathAnimation.append("lightenemy3Death5.png")
    deathAnimation.append("lightenemy3Death6.png")
    deathAnimation.append("lightenemy3Death7.png")
    deathAnimation.append("enemyDeath.png")

    block_group.add(player)
    backgroundGroup.add(background)
    backgroundGroup.add(background2)
    exitScreenGroup.add(exitScreen)
    startMenuGroup.add(startMenu)
    enemyGroup.add(enemy)

    start1X = 1
    start1Y = 10

    patrolRight1 = True

    scrollValue = -1800
    loopCount = 0
    lowerCount = 0

    enemyExists = True
    enemiesKilled = 0
    waveKilled = False
    waveNumber = 1
    enemyArmy = []
    boss = False

    y = 0
    while processRunning:

        while startMenuLoop == 0:
            startMenuGroup.draw(gameDisplay)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        startMenuLoop += 1
                        gameLoop(windowWidth, windowHeight, gameDisplay, playerMovedDistance, playerWidth, playerHeight, clock, fps, startMenuLoop)

        while gameOver:
            #gameDisplay.fill(white)
            #message_to_screen("GAME OVER, C to play again or Q to quit", black, font, gameDisplay, windowWidth)
            exitScreenGroup.draw(gameDisplay)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        processRunning = False
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop(windowWidth, windowHeight, gameDisplay, playerMovedDistance, playerWidth, playerHeight, clock, fps, startMenuLoop)


        background.set_position(0, y-702)
        background2.set_position(0, y)

        loopCount += 1

        y += 4
        if y >= 702:
            y = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                processRunning = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.set_image("hero1Thrust.png")
                    player.set_position(playerXLocation, playerYLocation)
                elif event.key == pygame.K_RIGHT:
                    player.set_image("hero1Thrust.png")
                    player.set_position(playerXLocation, playerYLocation)
                elif event.key == pygame.K_UP:
                    player.set_image("hero1Thrust.png")
                    player.set_position(playerXLocation, playerYLocation)
                elif event.key == pygame.K_DOWN:
                    player.set_image("hero1Thrust.png")
                    player.set_position(playerXLocation, playerYLocation)

            print(event)

        if loopCount % 5 == 0:
            player.update_image("hero1Thrust2.png")
        else:
            player.update_image("hero1Thrust.png")

        player.set_position(playerXLocation, playerYLocation)
        # this handles if keys are pressed AND HELD
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if (playerXLocation - playerMovedDistance) < 0:
                #gameOver = True
                pass
            else:
                playerXLocation = playerXLocation - playerMovedDistance
                player.set_image("hero1Left.png")
                player.set_position(playerXLocation, playerYLocation)
        if keys[pygame.K_RIGHT]:
            if (playerXLocation + playerMovedDistance) >= (windowWidth - playerWidth):
                pass
            else:
                playerXLocation = playerXLocation + playerMovedDistance
                player.set_image("hero1Right.png")
                player.set_position(playerXLocation, playerYLocation)
        if keys[pygame.K_UP]:
            if (playerYLocation - playerMovedDistance) < 0:
                pass
            else:
                playerYLocation = playerYLocation - playerMovedDistance
                player.set_image("hero1Thrust2.png")
                player.set_position(playerXLocation, playerYLocation)
        if keys[pygame.K_DOWN]:
            if (playerYLocation + playerMovedDistance) >= (windowHeight - playerHeight):
                pass
            else:
                playerYLocation = playerYLocation + playerMovedDistance
                player.set_image("hero1Thrust.png")
                player.set_position(playerXLocation, playerYLocation)
        if keys[pygame.K_SPACE]:
            if loopCount % 7 == 0:
                playerFire.play()
                missile1X = playerXLocation+8
                missile1Y = playerYLocation+4
                missile = Bullet()
                missile.update_image("playerMissile.png")
                missile.set_position(missile1X, missile1Y)
                missile2X = playerXLocation+32
                missile2Y = playerYLocation+4
                missile2 = Bullet()
                missile2.update_image("playerMissile.png")
                missile2.set_position(missile2X, missile2Y)

                bulletGroup.add(missile)
                bulletGroup.add(missile2)

        for missile in bulletGroup:
            if (missile.getY() < 0):
                bulletGroup.remove(missile)
            missile.update("player")

        for enemyMissile in enemyBulletGroup:
            if (missile.getY() > windowHeight):
                enemyBulletGroup.remove(enemyMissile)
            enemyMissile.update("enemy")

        if enemyExists == False:
            enemyArmy = []
            for i in range(0, waveNumber, 1):
                enemyArmy.append(Enemy())
            for enemy in enemyArmy:
                if boss:
                    enemy.set_Health(100)
                    #enemy.set_rect(5000,5000)
                    enemy.set_image("boss.png")
                    enemy.update_image("boss.png")
                else:
                    enemy.set_image("lightenemy2.png")
                enemyGroup.add(enemy)

            #enemy = Enemy()
            start1X = 1
            start1Y = 10
            lowerCount = 0

            enemyExists = True

        else:
            for enemy in enemyGroup:
                if loopCount % 200  == 0:
                    enemyMissile = Bullet()
                    enemyMissile2 = Bullet()

                    if boss == False:
                        enemyMissile.update_image("enemyMissile.png")
                        enemyMissile2.update_image("enemyMissile.png")

                        enemyMissileStartX = enemy.getX() + 20
                        enemyMissileStartY = enemy.getY() + 10

                        enemyMissileStartX2 = enemy.getX() + 30
                        enemyMissileStartY2 = enemy.getY() + 10

                    elif boss == True:
                        enemyMissile.update_image("bossMissile.png")
                        enemyMissile2.update_image("bossMissile.png")

                        enemyMissileStartX = enemy.getX() + 50
                        enemyMissileStartY = enemy.getY() + 100

                        enemyMissileStartX2 = enemy.getX() + 170
                        enemyMissileStartY2 = enemy.getY() + 100

                    enemyMissile.set_position(enemyMissileStartX, enemyMissileStartY)
                    enemyMissile2.set_position(enemyMissileStartX2, enemyMissileStartY2)

                    enemyBulletGroup.add(enemyMissile)
                    enemyBulletGroup.add(enemyMissile2)

        tempX = start1X
        tempY = start1Y
        tempDiff = 250
        tempDiff2 = 75

        for enemy in enemyGroup:
            #enemy.set_position(start1X, start1Y)
            enemy.set_position(tempX, tempY)
            #enemy.set_position(300, 0)
            if boss:
                tempX += tempDiff
            else:
                tempX += tempDiff2
        lowerY = 0
        enemyWidth = playerWidth
        if boss:
            tempX -= tempDiff
            enemyWidth = 236
            lowerY += 20
        else:
            tempX -= tempDiff2
            lowerY += 6

        if patrolRight1:
            if tempX + playerMovedDistance >= windowWidth - enemyWidth:
                if lowerCount < lowerY:
                    lowerCount += 1
                else:
                    start1Y += 50
                    lowerCount = 0
                patrolRight1 = False
            else:
                start1X += playerMovedDistance
                patrolRight1 = True

        else:
            if start1X - playerMovedDistance < 0:
                if lowerCount < lowerY:
                    lowerCount += 1
                else:
                    start1Y += 50
                    lowerCount = 0
                patrolRight1 = True
            else:
                start1X -= playerMovedDistance
                patrolRight1 = False
        if boss:
            tempSpriteWidth = 300
            tempSpriteHeight = 150
        else:
            tempSpriteWidth = 64
            tempSpriteHeight = 64
        for enemy in enemyGroup:
            for missile in bulletGroup:
                if missile.checkCollision(missile, enemy, spriteWidth=tempSpriteWidth, spriteHeight=tempSpriteHeight):
                    if boss:
                        enemy.update_image("bossDamaged.png")
                    else:
                        enemy.update_image("lightenemy3Damaged.png")
                    missile.destroy()
                    bulletGroup.remove(missile)
                    enemy.decrement_Health()
                    if enemy.get_Health() < 0:
                        enemy.enemyDead() == True
                    else:
                        if enemy.enemyDead() == False:
                            if boss:
                                enemy.update_image("boss.png")
                            else:
                                enemy.update_image("lightenemy3.png")

            ### Enemy Missile Collision
            for enemyMissile in enemyBulletGroup:
                if enemyMissile.checkCollision(enemyMissile, player):
                    enemyMissile.destroy()
                    enemyBulletGroup.remove(enemyMissile)
                    player.setHealth(0)
                    gameOver = True
                elif enemyMissile2.checkCollision(enemyMissile2, player):
                    enemyMissile2.destroy()
                    enemyBulletGroup.remove(enemyMissile2)
                    player.setHealth(0)
                    gameOver = True

            if enemy.enemyDead():
                if loopCount % 7 == 0:
                    if enemy.getSpriteCounter() < len(deathAnimation)-1:
                        enemy.update_image(deathAnimation[enemy.getSpriteCounter()])
                        enemy.setSpriteCounter(enemy.getSpriteCounter() + 1)
                    else:
                        enemy.destroy()
                        enemiesKilled += 1
                        #if enemiesKilled <= 1:
                        if enemiesKilled == 1:
                            if boss:
                                gameOver = True
                            waveKilled = True
                            waveNumber += 1
                            enemyExists = False
                            #if waveKilled:
                            #   waveNumber += 1
                        if enemiesKilled == 3:
                            waveKilled = True
                            waveNumber += 1
                            enemyExists = False
                        if enemiesKilled == 6:
                            waveKilled = True
                            waveNumber += 1
                            enemyExists = False
                        if enemiesKilled == 10:
                            waveKilled = True
                            waveNumber += 1
                            enemyExists = False
                        if enemiesKilled == 15:
                            waveKilled = True
                            waveNumber = 1
                            enemyExists = False
                            boss = True
                            enemiesKilled = 0


        backgroundGroup.draw(gameDisplay)
        block_group.draw(gameDisplay)
        bulletGroup.draw(gameDisplay)
        enemyBulletGroup.draw(gameDisplay)
        enemyGroup.draw(gameDisplay)

        pygame.display.update()

        clock.tick(fps)


    #uninitilizes pygame
    pygame.quit()
    #exits out of python
    quit

main()