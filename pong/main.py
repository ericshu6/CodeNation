import pygame
import random

pygame.init()
pygame.display.set_caption('Pong')

# Feel free to change width/height
width = 800
height = 500
screen = pygame.display.set_mode((width, height))

background_color = (0, 0, 0)

# Make sure your game operates on same speed, regardless of fps.
fps = 60
clock = pygame.time.Clock()

font_size = 72
font = pygame.font.SysFont("arial", font_size)

small_font_size = 50
small_font = pygame.font.SysFont("arial", small_font_size)

def main_menu():
    centerwidth = screen.get_width() / 2
    centerheight = screen.get_height() / 2

    titleobj = font.render("Pong", True, "white")
    titlerect = titleobj.get_rect(center=(centerwidth, centerheight))

    playobj = small_font.render("Press space to play", True, "white")
    playrect = playobj.get_rect(center=(centerwidth, centerheight * 1.5))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_loop(3)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(background_color)
        screen.blit(titleobj, titlerect)
        screen.blit(playobj, playrect)
        pygame.display.update()

def end_screen(player_won):
    centerwidth = screen.get_width() / 2
    centerheight = screen.get_height() / 2

    winobj = font.render(f"Player {player_won} won!", True, "white")
    winrect = winobj.get_rect(center=(centerwidth, centerheight))

    playobj = small_font.render("Press space to play again", True, "white")
    playrect = playobj.get_rect(center=(centerwidth, centerheight * 1.5))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    game_loop(3)
                    break

        screen.fill(background_color)
        screen.blit(winobj, winrect)
        screen.blit(playobj, playrect)
        pygame.display.update()

def game_loop(score_required_to_win):
    paddle_1 = Paddle(x=50, y=height / 2, paddle_width=5, paddle_height=60, speed=400, up_key=pygame.K_w,
                      down_key=pygame.K_s, color=(255, 100, 100))
    paddle_2 = Paddle(x=width - 50, y=height / 2, paddle_width=5, paddle_height=60, speed=400, up_key=pygame.K_UP,
                      down_key=pygame.K_DOWN, color=(100, 255, 100))

    ball = Ball(x=width / 2, y=height / 2, radius=10, speed_x=400, color=(0, 255, 255))

    while True:
        # Exits game if pressed space or tries to quit.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

        # Draw background
        draw_background()

        # Draw scoreboard
        draw_scoreboard(paddle_1.score, paddle_2.score)

        # Update the two paddles.
        paddle_1.update(1/fps)
        paddle_2.update(1/fps)

        # Update the ball
        ball.update(1/fps, paddle_left=paddle_1, paddle_right=paddle_2)

        # Check if a player has won, and if so print which player won, and exit the game (return).
        #   This should take <10 lines of code (assuming you don't make it more fancy)
        if paddle_1.score == score_required_to_win:
            end_screen(1)
        elif paddle_1.score == score_required_to_win:
            end_screen(2)

        # This is neccessary code to see screen updated.
        pygame.display.update()

        # This is so your game is run at a certain speed.
        # See: https://www.youtube.com/watch?v=rWtfClpWSb8 for how to achieve true framerate independence.
        # (Only watch it after you're done with rest of code)
        clock.tick(fps)


def draw_scoreboard(score_1, score_2):
    amount_offset_x = 50
    amount_offset_y = 50
    for (dx, score) in [(-amount_offset_x, score_1), (amount_offset_x, score_2)]:
        text_surface = font.render(str(score), True, "white")
        text_rect = text_surface.get_rect(center=(width // 2 + dx, amount_offset_y))
        screen.blit(text_surface, text_rect)


def draw_background():
    # Fill in the background color, with background_color.
    #   Do this code first.
    screen.fill(background_color)

    # Draw some gray dotted line in the (vertical) middle
    #   You will want to use a loop for this, and draw lines/rectangles to do so.
    #   Do this step after getting rest of code done.
    dot_rect = pygame.Rect(0, 0, 5, 5)
    dot_x = screen.get_width() / 2
    dot_y = 0
    while True:
        dot_rect.center = (dot_x, dot_y)
        pygame.draw.rect(screen, (255,255,255), dot_rect)
        dot_y += 20
        if dot_y > screen.get_height():
            break


class Paddle:
    def __init__(self, *, x, y, paddle_width, paddle_height, speed, up_key, down_key, color=(255, 255, 255),
                 border_width=0):
        self.score = 0

        # Later on, we will use pygame objects to handle position.
        self.x = x
        self.y = y
        self.width = paddle_width
        self.height = paddle_height

        self.speed = abs(speed)

        self.up_key = up_key
        self.down_key = down_key

        self.color = color
        self.border_width = border_width
        self.rect = pygame.draw.rect(screen, self.color, [self.get_x_low(), self.get_y_low(), self.width, self.height],
                         self.border_width)

    def update(self, dt):
        self.move_on_input(dt)
        self.draw()

    def move_on_input(self, dt):
        keys = pygame.key.get_pressed()
        # Get user input (make use of self.up_key, self.down_key)
        #   then move self.y based on it (remember to multiply by self.speed*dt)
        if keys[self.down_key]:
            if self.rect.bottom < screen.get_height():
                self.y += self.speed * dt
        elif keys[self.up_key]:
            if self.rect.top > 0:
                self.y -= self.speed * dt


    def draw(self):
        self.rect = pygame.draw.rect(screen, self.color, [self.get_x_low(), self.get_y_low(), self.width, self.height],
                                     self.border_width)

    # Later on, we will learn the Pythonic way to do it, but for now we will use more Java-style ones.

    def get_x_low(self):
        return self.x - self.width / 2

    def get_x_high(self):
        return self.x - self.width / 2

    def get_y_low(self):
        # This is actually the top of the figure (vertically inverted display)
        return self.y - self.height / 2

    def get_y_high(self):
        return self.y + self.height / 2


class Ball:
    def __init__(self, *, x, y, radius, speed_x, color=(255, 255, 255), border_width=0):
        # Later on, we will use pygame objects to handle position (and velocity).
        self.x = x
        self.y = y

        # This is so that when the paddle gets destroyed, the ball can reset to original pos.
        self.x_value_to_reset_to = x
        self.y_value_to_reset_to = y

        # Initialize some velocity variables (one for x velocity, one for y)
        #   set the y velocity to be some multiple of the x velocity.
        #   use sensible naming
        self.vx = 200
        self.vy = random.uniform(0.5, 2) * self.vx

        # Initialize radius, speed_x, color, and border_width class variables.
        self.radius = radius
        self.speed_x = speed_x
        self.color = color
        self.border_width = border_width
        self.rect = pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.border_width)

    def update(self, dt, *, paddle_left, paddle_right):
        # Call the functions needed for updating.
        #   Hint: There are 6 functions total to be called (including repeated calls)
        self.move(dt)
        self.draw()
        self.account_score_increases(paddle_left, paddle_right)
        self.account_for_paddle_collision(paddle_left)
        self.account_for_paddle_collision(paddle_right)
        self.account_for_vertical_screen_collision()

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self):
        # Draw a pygame circle, with the self.color, self.x, self.y, self.radius, and self.border_width
        #   use the (global) screen variable.
        self.rect = pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.border_width)

    def account_for_paddle_collision(self, paddle: Paddle) -> None:
        """
        Assumes the ball is relatively slow (i.e. won't clip through)
        Also does not use i-frames (i.e. collision could occur multiple times for a collision)
        Simply negates ball
        """

        if not self.does_collide(paddle):
            return

        # Negates x velocity, if collides with a paddle
        self.vx = -self.vx

    def account_for_vertical_screen_collision(self):
        if self.get_y_low() < 0:
            # We do this, so that it doesn't get potentially stuck out of bounds
            self.set_y_low(0)

            # Modify velocity variable.
            self.vy = -self.vy
        if self.get_y_high() > height:
            self.set_y_high(height)
            self.vy = -self.vy

    def account_score_increases(self, left_paddle: Paddle, right_paddle: Paddle):
        if self.get_x_low() < 0:
            # Reset ball, increment the left paddle's score.
            left_paddle.score += 1
            self.reset_ball()
        elif self.get_x_high() > width:
            right_paddle.score += 1
            self.reset_ball()

    def reset_ball(self):
        """
        Flips ball direction, resets position of ball.
        """

        # Flip the x velocity (so the person who scored, has ball sent their way)
        self.vx = -self.vx
        # Set vy to some random multiple of vx.
        self.vy = random.uniform(0.5, 2) * self.vx

        # This is why we initialized x_value_to_reset_to and y_value_to_reset_to!
        self.x = self.x_value_to_reset_to
        self.y = self.y_value_to_reset_to

    def does_collide(self, paddle):
        return self.rect.colliderect(paddle.rect)

    # Later on, we will learn the Pythonic way to do it, but for now we will use more Java-style ones.

    # These will have slightly different implementations than paddle.
    def get_x_low(self):
        return self.x - self.radius

    def get_x_high(self):
        return self.x + self.radius

    def get_y_low(self):
        return self.y - self.radius

    def get_y_high(self):
        return self.y + self.radius

    def set_x_low(self, num):
        self.x = num + self.radius

    def set_x_high(self, num):
        self.x = num - self.radius

    def set_y_low(self, num):
        self.y = num + self.radius

    def set_y_high(self, num):
        self.y = num - self.radius

# Call the main menu
main_menu()