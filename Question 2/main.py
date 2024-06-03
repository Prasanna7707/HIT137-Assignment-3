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
pygame.display.set_caption("Chicken Invaders")


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
        self.position.update(Vector(0, -self.speed * 2))


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
        self.restart_button_rect = None  # Initialize the restart button rect
        self.play_again_button_rect = None  # Initialize the play again button rect

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
        self.restart_button_rect = None  # Reset the restart button rect
        self.play_again_button_rect = None  # Reset the play again button rect

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


# ========== Main Code ===================

# This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

game = Game(screen)

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.ship.position.update(Vector(-10, 0))
            elif event.key == pygame.K_RIGHT:
                game.ship.position.update(Vector(10, 0))
            elif event.key == pygame.K_SPACE:
                game.ship.shoot()
        elif event.type == pygame.MOUSEBUTTONDOWN and (game.game_over or game.congratulations_screen):
            if (game.restart_button_rect and game.restart_button_rect.collidepoint(event.pos)) or \
               (game.play_again_button_rect and game.play_again_button_rect.collidepoint(event.pos)):
                game.reset_game()

    if not game.game_over and not game.congratulations_screen:
        game.enemies_shoot()
        for shot in game.friendly_shots:
            shot.update()
            for enemy in game.enemies:
                if shot.encounters(enemy):
                    game.friendly_shots.remove(shot)
                    enemy.kill()
                    game.score += 1
                    game.enemy_deaths += 1
                    if game.enemy_deaths >= len(game.enemies):
                        game.increment_level()
                        game.spawn_enemies()
                    break

        for shot in game.enemy_shots:
            shot.update()
            if shot.encounters(game.ship):
                game.enemy_shots.remove(shot)
                game.lose_life()
                if game.lives <= 0:
                    game.game_over = True
                break

    screen.fill(WHITE)
    game.apple.show()
    game.ship.show()
    for enemy in game.enemies:
        enemy.show()
    for shot in game.friendly_shots + game.enemy_shots:
        shot.show()
    game.draw_score()
    game.draw_level()
    game.draw_lives()

    if game.game_over:
        game.draw_restart_button()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
