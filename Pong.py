import pygame
import sys
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
        FONT_SCORE =  pygame.font.SysFont("Arial", 50, italic=True)
        Text = FONT_SCORE.render("Score: ", True, WHITE)
        

    def Move(self, keys):
        self.velocity_y = 0

        if keys[K_w]:
            self.velocity_y -= self.init_velocity
        if keys[K_s]:
            self.velocity_y += self.init_velocity

        self.y += self.velocity_y
        self.rect.y = self.y

        #Border
        if self.y <= 3:
            self.y = 0
        elif self.y >= 500:
            self.y = 490

        

class Paddle_2(Paddle):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self.color = color

    def Draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=14)
        FONT_SCORE =  pygame.font.SysFont("Arial", 50, italic=True)
        Text = FONT_SCORE.render('Score: '+ str(Score_A), True, WHITE)

    def Move(self, keys):
        self.velocity_y = 0  # Reset velocity to 0 each time the method is called

        if keys[K_UP]:
            self.velocity_y -= self.init_velocity
        if keys[K_DOWN]:
            self.velocity_y += self.init_velocity

        self.y += self.velocity_y
        self.rect.y = self.y


             #Border
        if self.y <= 3:
            self.y = 0
        elif self.y >= 500:
            self.y = 490

class Ball(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.velocity_x = 6.5
        self.velocity_y = 6.5
        self.color = color
    def Draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), 15, 0)
#
        
       

    def Move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y < 0 + 15 or self.y > HEIGHT - 15:
            self.velocity_y = -self.velocity_y

        if self.x < 0 + 15:
            self.velocity_x = -self.velocity_x
            # Increase Score_B by 10 when the ball hits the left edge
            global Score_B
            Score_B += 10
            print("Score B:", Score_B)

        elif self.x > WIDTH - 15:
            self.velocity_x = -self.velocity_x
            # Increase Score_A by 10 when the ball hits the right edge
            global Score_A
            Score_A += 10
            print("Score A:", Score_A)

        if paddle2.rect.colliderect(self.x - 20, self.y - 20, 40, 40):
            self.velocity_x = -self.velocity_x

        if paddle1.rect.colliderect(self.x - 20, self.y - 20, 40, 40):
            self.velocity_x = -self.velocity_x

        


# Game Variables
clock = pygame.time.Clock()
paddle1 = Paddle(50, HEIGHT // 2, 25, 100)
paddle2 = Paddle_2(WIDTH-75, HEIGHT // 2, 25, 100, GREEN)
ball = Ball(WIDTH//2, HEIGHT//2, RED)
Score_A = 0
Score_B = 0



def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        WINDOW.fill(BLACK)

        # Paddle 1
        paddle1.Draw(WINDOW)
        paddle1.Move(keys)

        # Paddle 2
        paddle2.Draw(WINDOW)
        paddle2.Move(keys)

        # Ball
        ball.Move()
        ball.Draw(WINDOW)

        # Display Scores
        FONT_SCORE = pygame.font.SysFont("Arial", 50, italic=True)
        Text_A = FONT_SCORE.render('Score A: ' + str(Score_A), True, WHITE)
        Text_B = FONT_SCORE.render('Score B: ' + str(Score_B), True, WHITE)
        WINDOW.blit(Text_A, (150, 0))
        WINDOW.blit(Text_B, (500, 0))

        # Line
        pygame.draw.line(WINDOW, WHITE, (WIDTH / 2, 0), (WIDTH / 2, 600), 8)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
