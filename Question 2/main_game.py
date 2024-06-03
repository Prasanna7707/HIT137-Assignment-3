import random
import pygame

# ========== Pygame Config ================

WIDTH = 400
HEIGHT = 400
screen_size = [WIDTH, HEIGHT]

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize the game engine
pygame.init()

# Set the height and width of the screen
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Side Scrolling 2D game - HIT-137")


# ========== Functions ===================


def p5_map(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2


# ========== Classes =====================


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __invert__(self):
        return Vector(-self.x, -self.y)


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def coordinates(self):
        return self.x, self.y

    def is_clear(self, game_):
        for pos in game_.snake.positions:
            if pos.coordinates == self.coordinates():
                return False
        return True

    def update(self, vector):
        self.x += vector.x
        self.y += vector.y

    def __eq__(self, other):
        return abs(self.x - other.x) < game.object_padding and abs(self.y - other.y) < game.object_padding


VECTOR_SIZE = 5

RIGHT = Vector(VECTOR_SIZE, 0)
LEFT = Vector(-VECTOR_SIZE, 0)
UP = Vector(0, -VECTOR_SIZE)
DOWN = Vector(0, VECTOR_SIZE)


# ========== Game Objects ================


class Shot:

    def __init__(self, game_, init_pos):
        self.game = game_
        self.position = Position(init_pos.x, init_pos.y)
        self.speed = 2.5

    def update(self):
        pass

    def encounters(self, other):
        return self.position == other.position

    def show(self):
        pygame.draw.circle(self.game.screen, BLUE, self.position.coordinates(), 5)


class FriendlyShot(Shot):

    def __init__(self, game_, init_pos):
        Shot.__init__(self, game_, init_pos)

    def update(self):
        self.position.update(Vector(0, -self.speed*2))


class EnemyShot(Shot):

    def __init__(self, game_, init_pos):
        Shot.__init__(self, game_, init_pos)

    def update(self):
        self.position.update(Vector(0, self.speed))

    def show(self):
        pygame.draw.circle(self.game.screen, BLACK, self.position.coordinates(), 5)


class Spaceship:
    def __init__(self, game_):
        self.game = game_
        self.position = Position(WIDTH / 2, HEIGHT - 20)
        # Load the spaceship image
        original_image = pygame.image.load('space.png')
        # Resize the image to match the size of the original circle (diameter would be 20 pixels)
        self.image = pygame.transform.scale(original_image, (40, 40))  # Adjust width and height as needed
        # Initialize the rectangle
        self.rect = self.image.get_rect(center=self.position.coordinates())

    def shoot(self):
        # Ensure shots are fired from the correct position, possibly adjusting for the image size
        shot_position = Position(self.rect.centerx, self.rect.top)
        self.game.friendly_shots.append(FriendlyShot(self.game, shot_position))

    def show(self):
        # Update the rectangle's position before drawing
        self.rect.center = self.position.coordinates()
        self.game.screen.blit(self.image, self.rect)  # Draw the spaceship image at the updated position


class Enemy:
    def __init__(self, game_, position_, vibration_rate=1):
        self.game = game_
        self.position = position_
        self.vibration_rate = vibration_rate
        self.vibration_pattern = ['U', 'L', 'D', 'R']
        self.vibration_counter = 0
        # Load the enemy image
        original_image = pygame.image.load('hen.png')
        # Resize the image to match the size of the original circle (diameter would be 20 pixels)
        self.image = pygame.transform.scale(original_image, (20, 20))
        # Initialize the rectangle
        self.rect = self.image.get_rect(center=self.position.coordinates())

    def vibrate(self):
        vibration_move = self.vibration_pattern[self.vibration_counter]
        if vibration_move == 'U':
            self.position.y -= self.vibration_rate
        elif vibration_move == 'L':
            self.position.x -= self.vibration_rate
        elif vibration_move == 'D':
            self.position.y += self.vibration_rate
        elif vibration_move == 'R':
            self.position.x += self.vibration_rate
        self.vibration_counter += 1
        if self.vibration_counter == len(self.vibration_pattern):
            self.vibration_counter = 0
        # Update the rectangle position to match the position
        self.rect.center = self.position.coordinates()

    def kill(self):
        self.game.enemies.remove(self)

    def shoot(self):
        self.game.enemy_shots.append(EnemyShot(self.game, self.position))

    def show(self):
        self.vibrate()
        # Draw the enemy image at the updated position
        self.game.screen.blit(self.image, self.rect)


class Apple:
    def __init__(self, game_):
        self.game = game_
        self.spawn()

    def spawn(self):
        self.position = Position(random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 100))
        # Load the apple image
        original_image = pygame.image.load('apple.png')
        # Resize the image to match the size of the original circle (diameter would be 20 pixels)
        self.image = pygame.transform.scale(original_image, (20, 20))
        # Initialize the rectangle
        self.rect = self.image.get_rect(center=self.position.coordinates())

    def show(self):
        self.rect.center = self.position.coordinates()
        self.game.screen.blit(self.image, self.rect)


class Game:

    def __init__(self, screen_, object_padding=10):
        self.screen = screen_
        self.object_padding = object_padding
        self.reset_game()
        self.congratulations_screen = False

    def reset_game(self):
        self.ship = Spaceship(self)
        self.friendly_shots = []
        self.enemy_shots = []
        self.enemies = []
        self.apple = Apple(self)
        self.spawn_enemies()
        self.score = 0  # Initialize the score
        self.level = 1  # Initialize the level
        self.lives = 3  # Initialize the lives
        self.enemy_deaths = 0  # Track the number of enemy deaths
        self.game_over = False  # Flag to indicate if the game is over
        self.congratulations_screen = False

    def spawn_enemies(self):
        positions_ = [Position(x, 20) for x in range(20, WIDTH - 10, 50)]
        for pos in positions_:
            self.enemies.append(Enemy(self, pos))

    def enemies_shoot(self):
        shooting_chance = 0.08
        if random.random() < shooting_chance:
            random.choice(self.enemies).shoot()

    def draw_restart_button(self):
        self.restart_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
        pygame.draw.rect(self.screen, RED, self.restart_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render('Restart', True, BLACK)
        text_rect = text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(text, text_rect)

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, BLACK)
        self.screen.blit(score_text, (WIDTH - 120, 30))

    def draw_level(self):
        font = pygame.font.Font(None, 36)
        level_text = font.render(f'Level: {self.level}', True, BLACK)
        self.screen.blit(level_text, (WIDTH - 120, 70))

    def draw_lives(self):
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f'Lives: {self.lives}', True, BLACK)
        self.screen.blit(lives_text, (WIDTH - 120, 110))

    def increment_level(self):
        self.level += 1
        self.enemy_deaths = 0  # Reset the enemy deaths count for the new level

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True  # End the game if no lives are left


if __name__ == '__main__':

    game = Game(screen)

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    # Mainloop
    # Mainloop
    while not done:

        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(50)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game.game_over:
                    game.ship.shoot()
            if event.type == pygame.MOUSEBUTTONDOWN and (game.game_over or game.congratulations_screen):
                if game.restart_button_rect.collidepoint(event.pos) or game.play_again_button_rect.collidepoint(event.pos):
                    game.reset_game()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RIGHT] and not game.game_over and not game.congratulations_screen:
            if not game.ship.position.x + RIGHT.x >= WIDTH:
                game.ship.position.update(RIGHT)
        elif pressed_keys[pygame.K_LEFT] and not game.game_over and not game.congratulations_screen:
            if not game.ship.position.x - LEFT.x <= 0:
                game.ship.position.update(LEFT)

        # Clear the screen and set the screen background
        screen.fill(WHITE)

        # ===========> UPDATE POSITIONS HERE <========

        if not game.game_over and not game.congratulations_screen:
            game.enemies_shoot()

            for shot in game.friendly_shots:
                shot.update()
                for enemy in game.enemies:
                    if shot.encounters(enemy):
                        enemy.kill()
                        game.score += 1  # Increment the score when an enemy is killed
                        game.enemy_deaths += 1  # Increment the enemy deaths count
                        if game.enemy_deaths % 3 == 0:
                            game.increment_level()  # Increment the level after every 3 enemy deaths
                        break
                if shot.encounters(game.apple):
                    game.score += 2  # Increment the score by 2 when the apple is hit
                    game.apple.spawn()  # Respawn the apple at a new position

            for shot in game.enemy_shots:
                shot.update()
                if shot.encounters(game.ship):
                    game.lose_life()  # Decrease a life when the ship is hit
                    if game.lives > 0:
                        game.enemy_shots.remove(shot)  # Remove the shot that hit the ship
                    break

            # Check if all enemies are defeated
            if len(game.enemies) == 0:
                game.congratulations_screen = True

        # ===========> START DRAWING HERE <===========

        game.ship.show()
        game.draw_score()  # Draw the score at the top right
        game.draw_level()  # Draw the level below the score
        game.draw_lives()  # Draw the lives below the level
        game.apple.show()  # Draw the apple

        for shot in game.friendly_shots:
            shot.show()

        for shot in game.enemy_shots:
            shot.show()

        for enemy in game.enemies:
            enemy.show()

        if game.game_over:
            game.draw_restart_button()  # Draw the restart button when the game is over

        if game.congratulations_screen:
            # Display congratulations screen
            font = pygame.font.Font(None, 36)
            congratulations_text = font.render("Congratulations!", True, BLACK)
            screen.blit(congratulations_text, (WIDTH // 2 - 120, HEIGHT // 2 - 50))
            score_text = font.render(f"Score: {game.score}", True, BLACK)
            screen.blit(score_text, (WIDTH // 2 - 60, HEIGHT // 2))
            # Draw play again button
            game.play_again_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
            pygame.draw.rect(screen, GREEN, game.play_again_button_rect)
            play_again_text = font.render("Play Again", True, BLACK)
            play_again_text_rect = play_again_text.get_rect(center=game.play_again_button_rect.center)
            screen.blit(play_again_text, play_again_text_rect)

        # ===========> END DRAWING HERE <=============

        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()
