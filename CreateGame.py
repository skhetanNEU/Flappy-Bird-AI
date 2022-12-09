import os
import pygame

# random is imported to randomly set the height of the pipes
import random

pygame.font.init()

HEIGHT = 800
WIDTH = 500

# scale2x is used to increase the size of the bird so that it looks good
BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("res", "background.png")))
GROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("res", "ground.png")))
PIPES = pygame.transform.scale2x(pygame.image.load(os.path.join("res", "pipe.png")))
BIRDS = [pygame.transform.scale2x(pygame.image.load(os.path.join("res", "bird1.png"))),
         pygame.transform.scale2x(pygame.image.load(os.path.join("res", "bird2.png"))),
         pygame.transform.scale2x(pygame.image.load(os.path.join("res", "bird3.png")))]
SCORE = pygame.font.SysFont("comicsans", 50)


class Bird:
    # Tilt degree on up and down
    ROTATION = 25
    ROTATION_VEL = 20
    # Increase or decrease this to fasten and slow down the flapping of the bird
    FLAPPING_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = BIRDS[0]
        self.terminalVelocity = 16

    def jump(self):
        # Top left is 0,0 so to start the bird in the center, we need -ve value here
        self.velocity = -10.5
        # Keep track of when we made the last jump
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        displacement = (self.velocity * self.tick_count) + (1.5 * self.tick_count ** 2)
        if displacement >= self.terminalVelocity:
            displacement = self.terminalVelocity
        if displacement < 0:
            # Makes the bird jump higher in each jump
            displacement -= 2

        self.y = self.y + displacement

        # displacement < 0 checks for if we are moving upwards or
        # we have to tilt the bird downwards
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.ROTATION:
                self.tilt = self.ROTATION
        else:
            # We are moving downwards
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VEL

    def draw(self, window):
        # Keeps track of number of times the image is shown via the while loop in main
        self.img_count += 1

        # Animating the bird flapping
        if self.img_count < self.FLAPPING_TIME:
            self.img = BIRDS[0]
        elif self.img_count < self.FLAPPING_TIME * 2:
            self.img = BIRDS[1]
        elif self.img_count < self.FLAPPING_TIME * 3:
            self.img = BIRDS[2]
        elif self.img_count < self.FLAPPING_TIME * 4:
            self.img = BIRDS[1]
        elif self.img_count < self.FLAPPING_TIME * 4 + 1:
            self.img = BIRDS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = BIRDS[1]
            self.img_count = self.FLAPPING_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    # Distance between pipes
    GAP = 200
    # Since pipes moves from right to left
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPES, False, True)
        self.PIPE_BOTTOM = PIPES
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()  # To figure out the top point of the pipe
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        # Using pixel perfect collision logic to get mask of bird and both the pipes and
        # then checking if there is a collision comparing the lists (masks)
        birdMask = bird.get_mask()
        topPipeMask = pygame.mask.from_surface(self.PIPE_TOP)
        bottomPipeMask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        topOffset = (self.x - bird.x, self.top - round(bird.y))
        bottomOffset = (self.x - bird.x, self.bottom - round(bird.y))

        bottomPoint = birdMask.overlap(bottomPipeMask, bottomOffset)
        topPoint = birdMask.overlap(topPipeMask, topOffset)

        if bottomPoint or topPoint:
            return True
        return False


class Ground:
    VELOCITY = 5
    WIDTH = GROUND.get_width()
    IMG = GROUND

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))


def draw_window(window, birds, pipes, base, score):
    window.blit(BACKGROUND, (0, 0))  # Draw on the window
    for pipe in pipes:
        pipe.draw(window)
    text = SCORE.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(text, (WIDTH - 10 - text.get_width(), 10))
    base.draw(window)

    for bird in birds:
        bird.draw(window)

    pygame.display.update()
