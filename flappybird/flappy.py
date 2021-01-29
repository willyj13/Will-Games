import pygame
import os
import time
import random
pygame.font.init()
score = 0
highscore = 0
groundLevel = 600

WIDTH, HEIGHT = 800, 800
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(os.path.join("flappyimg", "Flappy Bird"))

#Load image for the bird
flappybird = pygame.transform.scale(pygame.image.load(os.path.join("flappyimg", "flappy.png")), (70, 40))

#Load image for the Pipes
uppipe = pygame.transform.scale(pygame.image.load(os.path.join("flappyimg", "uppipe.png")), ( 50 ,800))
downpipe = pygame.transform.scale(pygame.image.load(os.path.join("flappyimg", "downpipe.png")), ( 50 ,800))

#Load images of the background and ground
ground = pygame.transform.scale(pygame.image.load(os.path.join("flappyimg", "ground.png")), (WIDTH, 200))
bg = pygame.transform.scale(pygame.image.load(os.path.join("flappyimg", "background.png")), (WIDTH, HEIGHT))



class Bird: #abstract class, won't use this class but will inherit from it
# we just make class instances

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.birdimg = flappybird
        self.coolDown = 0
        self.mask = pygame.mask.from_surface(flappybird)

    def draw(self, window):
        window.blit(self.birdimg, (self.x, self.y)) #draws bird to the window

    def getWidth(self): #width of the bird image
        return self.birdimg.get_width()

    def getHeight(self): #height of the bird image
        return self.birdimg.get_height()

    def gravity(self, grav = 4): #the gravity acting on the bird at all times
        self.y += grav

class Pipes:
    def __init__(self, x):
        self.x = x
        self.ypos = random.randrange(200, groundLevel - 100) #random height generation for the upward pipe
        self.downPipeY = self.ypos - uppipe.get_height() -150 #pairs the downwards pipe's height with the upward one
        self.vel = 2
        self.mask = pygame.mask.from_surface(downpipe)
        self.mask2 = pygame.mask.from_surface(uppipe)

    def newPipes(self, window): #draw function
        window.blit(uppipe, (self.x , self.ypos))
        window.blit(downpipe, (self.x, self.ypos - uppipe.get_height() -150))

    def move(self):
        self.x -= self.vel

    def collisionUp(self, obj):
        return collideUp(obj, self)

    def collisionDown(self, obj):
        return collideDown(obj, self)

class Ground:

    def __init__(self, x):
        self.x = x
        self.y = groundLevel
        self.groundimg = ground
        self.bg_x = 2


    def draw(self, window):
        window.blit(ground, ((self.x % ground.get_width()) - ground.get_width(), self.y))
        if (self.x % ground.get_width()) < WIDTH:
            window.blit(ground, ((self.x % ground.get_width()), self.y))

    def getWidth(self):
        return self.groundimg.get_width()

    def getX(self):
        return self.x

    def move(self):
        self.x -= self.bg_x


def collideUp(obj1, obj2): #we only want our collision to involve the pixels of each object
    offsetX = obj2.x - obj1.x
    offsetY = obj2.ypos - obj1.y
    return obj1.mask.overlap(obj2.mask, (offsetX, offsetY)) != None

def collideDown(obj1, obj2):
    offsetX = obj2.x - obj1.x
    offsetY = obj2.downPipeY - obj1.y
    return obj1.mask.overlap(obj2.mask, (offsetX, offsetY)) != None

def main():
    run = True
    mainFont = pygame.font.SysFont("Arial", 50)
    lostFont = pygame.font.SysFont("Arial", 60)
    lives = 1

    g = Ground(0)

    FPS = 60
    clock = pygame.time.Clock()
    lost = False
    lostCount = 0

    birdVel = 12

    bird = Bird(300, 300)
    backgrounds = []

    pipeList = []

    counter = 0


    def redrawWindow():
        global score
        for p in pipeList:
            p.newPipes(wn)
            p.move()

        g.draw(wn)
        g.move()

        if not lost:
            for p in range(len(pipeList)):
                if (bird.x > pipeList[p].x + uppipe.get_width()):
                    score = p + 1



        scoreLabel = mainFont.render(f"Score: {score}", 1, (255,255,255))

        wn.blit(scoreLabel, (WIDTH - scoreLabel.get_width() - 10, 10))


        bird.draw(wn)

        if lost:
            lostLabel = lostFont.render("You Lost!", 1, (255,255,255))
            wn.blit(lostLabel, (WIDTH/2 - lostLabel.get_width()/2, 200))


        pygame.display.update()


    while run:
        clock.tick(FPS)
        wn.blit(bg,(0,-100))

        counter += 1
        if (counter % 120) == 0:
            pipes = Pipes(WIDTH + 100)
            pipeList.append(pipes)

        redrawWindow()

        for event in pygame.event.get(): #check if ANY event has occurred
            if event.type == pygame.QUIT: #IF you quit the screen stop running pygame,
            #if you dont do this then the window will not shutdown when you try to close it
                run = False

        if (bird.y + bird.getHeight() > groundLevel):
            bird.gravity(0)
            lost = True
            lostCount += 1

        if (bird.y - bird.getHeight() < -50):
            lost = True
            lostCount +=1



        for p in pipeList:

            if p.collisionUp(bird):
                lost = True
                bird.x -= 2
                lostCount += 1

                break

            if p.collisionDown(bird):
                lost = True
                bird.x -= 2
                lostCount += 1
                break


        if lost:
            if lostCount > FPS * 3: #we show the message for 3 seconds
                run = False
            else:
                continue


        bird.gravity()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and bird.y < groundLevel: #keys is a dict and K_ is a prefix for all keyboard buttons
            bird.y -= birdVel
            bird.gravity(grav = 0)



def mainMenu():
    global highscore, score
    titleFont = pygame.font.SysFont("Arial", 30)
    mainFont = pygame.font.SysFont("Arial", 50)
    run = True
    while run:
        wn.blit(bg,(0,-100))
        g = Ground(0)
        g.draw(wn)

        highscoreLabel = mainFont.render(f"Highscore: {highscore}", 1, (255,255,255))
        wn.blit(highscoreLabel, (WIDTH - highscoreLabel.get_width() - 10, 70))
        scoreLabel = mainFont.render(f"Score: {score}", 1, (255,255,255))
        wn.blit(scoreLabel, (WIDTH - scoreLabel.get_width() - 10, 10))
        titleLabel = titleFont.render("Press spacebar to begin, use spacebar to jump...", 1, (255,255,255))
        exitLabel = titleFont.render("Click the exit button to quit", 1, (255,255,255))
        wn.blit(titleLabel, (WIDTH/2 - titleLabel.get_width()/2, 250))
        wn.blit(exitLabel, (WIDTH/2 - titleLabel.get_width()/2, 280))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

                    highscore = max(highscore, score)
                    score = 0


    pygame.quit()

mainMenu()
