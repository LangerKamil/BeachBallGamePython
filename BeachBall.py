import pygame
import sys
import random
import math

score_reset = False  # New variable to track if score should be reset
all_items_collected = False  # New variable to track if all items are collected


# Constants for the screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Constants for the player
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5
PLAYER_JUMP_SPEED = 15
GRAVITY = 0.2
GROUND_HEIGHT = 50

# Constants for the background speed
BACKGROUND_SPEED = 0.4

# Ball dimensions
BALL_WIDTH = 50
BALL_HEIGHT = 50

# Enemies dimensions
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50

# Enemies count
num_enemies = 2
initial_num_enemies = num_enemies
enemy_speeds = [-2, -1, 1, 2]
initial_speeds = enemy_speeds

# Load the original ball image
original_image = pygame.image.load("Images\\beachball3.png")

ball_image = pygame.transform.scale(original_image, (BALL_WIDTH, BALL_HEIGHT))

# Collectables image
original_image = pygame.image.load("Images\\cloud.png")

item_image = pygame.transform.scale(original_image, (BALL_WIDTH, BALL_HEIGHT))

# Enemies image
original_image = pygame.image.load("Images\\birdie.png")

enemy_image = pygame.transform.scale(original_image, (ENEMY_WIDTH, ENEMY_HEIGHT))

# Load the background image


BACKGROUND_SPEED = 0.4

background_width = SCREEN_WIDTH + 200  # Make the background wider
background_position = 0
background_speed = random.uniform(0.1, 0.3)  # Random movement speed
background_direction = -1  # Initial direction

background_image = pygame.image.load("Images\\beach.jpg")
background_image = pygame.transform.scale(background_image, (background_width, 600))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ball_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT / 2))
        self.score = 0
        self.game_over = False
        self.is_jumping = False  # New variable to track jumping state
        self.invincible = False # New variable to track invincibility state
        self.score_reset = False  # New variable to track score reset

    def move(self, press_keys):
        if press_keys[pygame.K_LEFT]:
            self.rect.move_ip(-PLAYER_SPEED, 0)
        if press_keys[pygame.K_RIGHT]:
            self.rect.move_ip(PLAYER_SPEED, 0)

        if press_keys[pygame.K_UP] and not self.is_jumping:  # Check if up arrow key is pressed and not jumping
            self.is_jumping = True
            self.jump_speed = -PLAYER_JUMP_SPEED

        if press_keys[pygame.K_DOWN]:
            self.rect.height = PLAYER_HEIGHT // 2
        else:
            self.rect.height = PLAYER_HEIGHT

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def gravity(self):
        if self.is_jumping:
            self.rect.move_ip(0, self.jump_speed)
            self.jump_speed += GRAVITY

            if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
                self.is_jumping = False  # Reset jumping state
                self.jump_speed = 0
        else:
            self.rect.move_ip(0, GRAVITY)

            if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT

    def collect_item(self, items):
        if self.invincible:  # Check if character is invincible
            return

        collided_items = pygame.sprite.spritecollide(self, items, True)
        self.score += len(collided_items)

        if len(items) == 0:
            self.invincible = True  # Set character to invincible state
            self.score_reset = False  # Reset score reset flag

    def collide_enemy(self, enemies):
        if self.invincible:  # Check if character is invincible
            return

        if pygame.sprite.spritecollideany(self, enemies):
            self.game_over = True  # Set the game_over flag to True on collision
    
    def reset(self):
        self.jumping = False
        self.jump_speed = 0

class Item(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = item_image
        self.rect = self.image.get_rect(center=pos)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.direction = 1  # 1 for moving right, -1 for moving left
        self.vertical_speed = 2
        self.vertical_range = 20
        self.original_y = self.rect.y

    def update(self):
        self.rect.move_ip(self.speed * self.direction, 0)

        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction = -1

        if self.rect.left == 0 or self.rect.right == SCREEN_WIDTH:
            self.speed *= -1  # Reverse the speed to bounce off the wall
            self.image = pygame.transform.flip(self.image, True, False)  # Flip the image horizontally

        # Vertical movement
        self.rect.y = self.original_y + self.vertical_range * math.sin(pygame.time.get_ticks() / 200)  # Adjust the amplitude and frequency as desired

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


background_position = 0

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

items = pygame.sprite.Group()

def generate_items():
    num_items = random.randint(15, 20)

    for _ in range(num_items):
        item_pos = (random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - 100))
        item = Item(item_pos)
        all_sprites.add(item)
        items.add(item)

def generate_enemies(num_enemies):
    for _ in range(num_enemies):
        enemy_pos = (random.randint(0, SCREEN_WIDTH), random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - 100))
        enemy_speed = random.choice(enemy_speeds)
        enemy = Enemy(enemy_pos, enemy_speed)
        all_sprites.add(enemy)
        enemies.add(enemy)
        num_enemies += 1  # Increment the total number of enemies

def reset_game():
    all_sprites.empty()  # Clear all sprites
    items.empty()  # Clear items group
    enemies.empty()  # Clear enemies group
    player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT / 2)
    player.is_jumping = False
    player.jump_speed = 0
    if score_reset:  # Reset score only if score_reset is True
        player.score = 0
    generate_items()
    generate_enemies(num_enemies)
    player.game_over = False
    all_sprites.add(player)


generate_items()
enemies = pygame.sprite.Group()
generate_enemies(num_enemies)
player.reset()

clock = pygame.time.Clock()

score_font = pygame.font.Font(None, 36)
enemy_count_font = pygame.font.Font(None, 24)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                all_sprites.empty()  # Clear all sprites
                items.empty()  # Clear items group
                enemies.empty()  # Clear enemies group
                player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT / 2)
                player.jumping = False
                player.jump_speed = 0
                player.score = 0
                enemy_speeds = [-2, -1, 1, 2]
                generate_items()  # Generate new items
                generate_enemies(initial_num_enemies)  # Generate new enemies
                player.game_over = False  # Reset game over state
                all_sprites.add(player)  # Add player character back to sprite group
                num_enemies = initial_num_enemies



    press_keys = pygame.key.get_pressed()

    if player.game_over:  # Check if game over
        continue  # Skip the rest of the loop if it's game over

    player.move(press_keys)
    player.gravity()
    player.collect_item(items)
    #player.collide_enemy(enemies)

    background_position += background_speed * background_direction
    if background_position >= 20 or background_position <= -20:
        background_direction *= -1

    background_rect = background_image.get_rect(topleft=(background_position - 100, 0))
    screen.blit(background_image, background_rect)

    for entity in all_sprites:
        if entity.image is not None:  # Check if the entity has a valid image
            screen.blit(entity.image, entity.rect)

    for enemy in enemies:
        enemy.update()  # Update enemy movement

    if len(items) == 0 and not player.game_over:  # Check if all items have been collected and game over state is False
        font = pygame.font.Font(None, 36)
        got_it_text = font.render("You've got it! Press Enter to continue", True, (0, 0, 0))
        got_it_rect = got_it_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(got_it_text, got_it_rect)

        if press_keys[pygame.K_RETURN]:
            num_enemies += 1
            reset_game()
            all_items_collected = False
            if player.score_reset:  # Check if score reset flag is True
                player.score = 0  # Reset the score
            player.score_reset = True  # Set the score reset flag to True
            player.invincible = False  # Set invincibility to False when restarting game
            if num_enemies % 2 == 0:
                enemy_speeds.append(enemy_speeds[-1] + 1)

    if player.collide_enemy(enemies) and not all_items_collected and not player.invincible:
        num_enemies = initial_num_enemies
        reset_game()


    if player.game_over:  # Check if game over
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over", True, (0, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)

    # Update score text
    score_text = score_font.render("Score: " + str(player.score), True, (0, 0, 0))
    score_rect = score_text.get_rect(bottomleft=(10, SCREEN_HEIGHT - 50))

    # Draw score text
    screen.blit(score_text, score_rect)
    
    enemy_count_text = enemy_count_font.render("Birds: " + str(num_enemies), True, (0, 0, 0))
    enemy_count_rect = enemy_count_text.get_rect(bottomleft=(10, SCREEN_HEIGHT - 30))
    screen.blit(enemy_count_text, enemy_count_rect)
    
    enemy_count_text = enemy_count_font.render("Birds max speed: " + str(enemy_speeds[-1]), True, (0, 0, 0))
    enemy_count_rect = enemy_count_text.get_rect(bottomleft=(10, SCREEN_HEIGHT - 10))
    screen.blit(enemy_count_text, enemy_count_rect)

    # Automatically trigger jump when player reaches ground
    if not player.jumping and player.rect.bottom == SCREEN_HEIGHT - GROUND_HEIGHT:
        player.jumping = True
        player.jump_speed = -PLAYER_JUMP_SPEED

    pygame.display.flip()
    clock.tick(60)