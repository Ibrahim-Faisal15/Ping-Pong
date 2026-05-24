import pygame
import sys
import os
from pygame.locals import *

pygame.init()

# Display
WIDTH = 800
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong By @Ibrahim")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (142, 68, 173)

# Load background image (optional)
bg = None
bg_path = os.path.join(os.path.dirname(__file__), "bg.png")
try:
    bg = pygame.image.load(bg_path).convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
except Exception as e:
    bg = None
    print("Warning: couldn't load bg.png:", e)

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_y = 0
        self.init_velocity = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def Draw(self, surface):
        global Text, FONT_SCORE
        pygame.draw.rect(surface, PURPLE, self.rect, border_radius=14)
        FONT_SCORE =  pygame.font.SysFont("Arial", 25)
        Text = FONT_SCORE.render("Score: ", True, WHITE)
        

    def Move(self, keys):
        self.velocity_y = 0

        if keys[K_w]:
            self.velocity_y -= self.init_velocity
        if keys[K_s]:
            self.velocity_y += self.init_velocity

        self.y += self.velocity_y

        if self.y < 32:
            self.y = 32
        elif self.y > 476:
            self.y = 476

        self.rect.y = self.y

        

class Paddle_2(Paddle):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self.color = color

    def Draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=14)
        FONT_SCORE =  pygame.font.SysFont("Arial", 25)
        Text = FONT_SCORE.render('Score: '+ str(Score_A), True, WHITE)

    def Move(self, keys):
        self.velocity_y = 0  # Reset velocity to 0 each time the method is called

        if keys[K_UP]:
            self.velocity_y -= self.init_velocity
        if keys[K_DOWN]:
            self.velocity_y += self.init_velocity

        self.y += self.velocity_y

        if self.y < 32:
            self.y = 32
        elif self.y > 476:
            self.y = 476

        self.rect.y = self.y

class Ball(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.velocity_x = 6.5
        self.velocity_y = 6.5
        self.color = color
    def Draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), 15, 0)

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.velocity_x = -self.velocity_x

    def Move(self):
        global game_started
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y < 38:
            self.y = 38
            self.velocity_y = -self.velocity_y
        elif self.y > 569:
            self.y = 569
            self.velocity_y = -self.velocity_y

        if self.x < 22:
            global Score_B
            Score_B += 10
            print("Score B:", Score_B)
            self.reset()
            paddle1.y = HEIGHT // 2 - 50
            paddle1.rect.y = paddle1.y
            paddle2.y = HEIGHT // 2 - 50
            paddle2.rect.y = paddle2.y
            game_started = False

        elif self.x > 778:
            global Score_A
            Score_A += 10
            print("Score A:", Score_A)
            self.reset()
            paddle1.y = HEIGHT // 2 - 50
            paddle1.rect.y = paddle1.y
            paddle2.y = HEIGHT // 2 - 50
            paddle2.rect.y = paddle2.y
            game_started = False

        if paddle2.rect.colliderect(self.x - 20, self.y - 20, 40, 40):
            self.velocity_x = -self.velocity_x

        if paddle1.rect.colliderect(self.x - 20, self.y - 20, 40, 40):
            self.velocity_x = -self.velocity_x

        


# Game Variables
clock = pygame.time.Clock()
paddle1 = Paddle(50, HEIGHT // 2 - 50, 25, 100)
paddle2 = Paddle_2(WIDTH-75, HEIGHT // 2 - 50, 25, 100, GREEN)
ball = Ball(WIDTH//2, HEIGHT//2, RED)
Score_A = 0
Score_B = 0
game_started = False



def main():
    global Score_A, Score_B, game_started
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    game_started = True
                elif event.key == K_SPACE:
                    Score_A = 0
                    Score_B = 0
                    ball.reset()
                    paddle1.y = HEIGHT // 2 - 50
                    paddle1.rect.y = paddle1.y
                    paddle2.y = HEIGHT // 2 - 50
                    paddle2.rect.y = paddle2.y
                    game_started = False

        keys = pygame.key.get_pressed()

        # Draw background (image if available)
        if bg:
            WINDOW.blit(bg, (0, 0))
        else:
            WINDOW.fill(BLACK)

        # Line & Center Circle
        pygame.draw.line(WINDOW, WHITE, (WIDTH / 2, 0), (WIDTH / 2, 600), 8)
        pygame.draw.circle(WINDOW, WHITE, (WIDTH // 2, HEIGHT // 2), 60, 6)

        # Paddle 1
        paddle1.Draw(WINDOW)
        if game_started:
            paddle1.Move(keys)

        # Paddle 2
        paddle2.Draw(WINDOW)
        if game_started:
            paddle2.Move(keys)

        # Display Scores
        FONT_SCORE = pygame.font.SysFont("Arial", 25)
        Text_A = FONT_SCORE.render('Score A: ' + str(Score_A), True, WHITE)
        Text_B = FONT_SCORE.render('Score B: ' + str(Score_B), True, WHITE)
        WINDOW.blit(Text_A, (200 - Text_A.get_width() // 2, 35))
        WINDOW.blit(Text_B, (600 - Text_B.get_width() // 2, 35))

        # Display Controls
        FONT_CONTROLS = pygame.font.SysFont("Arial", 16)
        Text_Controls_A = FONT_CONTROLS.render('Controls: W / S  |  SPACE to Restart', True, (200, 200, 200))
        Text_Controls_B = FONT_CONTROLS.render('Controls: UP / DOWN  |  ENTER to Start', True, (200, 200, 200))
        WINDOW.blit(Text_Controls_A, (200 - Text_Controls_A.get_width() // 2, 550))
        WINDOW.blit(Text_Controls_B, (600 - Text_Controls_B.get_width() // 2, 550))

        # Ball (drawn in front of lines)
        if game_started:
            ball.Move()
        ball.Draw(WINDOW)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
