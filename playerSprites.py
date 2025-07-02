"""
Author: Eric Chen & Ryan Chen
Date: June 17 2024
Description: This program file contains the player sprite and its methods. This allows for the player to perform abilities. 
"""

import pygame
from movingSprites import Projectile
from movingSprites import Sword
import time

# Define gravity constants
GRAVITY_DOWN = 15
GRAVITY_UP = -15
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BAR_WIDTH = 200
BAR_HEIGHT = 20
        

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        """
        Initialize the Player sprite.

        Parameters:
            screen (pygame.Surface): The surface representing the game window.
        
        Returns: None
        """
        pygame.sprite.Sprite.__init__(self)
        
        # Load running animation images
        self.runningAnimation = [
            pygame.transform.scale(pygame.image.load("01. Visual Assets/00. Player Sprites/mainPlayer1.png"), (100, 100)),
            pygame.transform.scale(pygame.image.load("01. Visual Assets/00. Player Sprites/mainPlayer2.png"), (100, 100)),
            pygame.transform.scale(pygame.image.load("01. Visual Assets/00. Player Sprites/mainPlayer3.png"), (100, 100)),
            pygame.transform.scale(pygame.image.load("01. Visual Assets/00. Player Sprites/mainPlayer4.png"), (100, 100)),
            pygame.transform.scale(pygame.image.load("01. Visual Assets/00. Player Sprites/mainPlayer5.png"), (100, 100)),
            pygame.transform.scale(pygame.image.load("01. Visual Assets/00. Player Sprites/mainPlayer6.png"), (100, 100))
        ]

        # Start with the first image in the running animation
        self.imageNum = 0
        self.image = self.runningAnimation[self.imageNum]
       
        # Set player position
        self.rect = self.image.get_rect()
        self.rect.left = 350
        self.rect.top = 220

        self.screen = screen

        # Load sounds
        self.slashing = pygame.mixer.Sound("00. Sounds/slashing.wav")
        self.slashing.set_volume(0.2)

        self.dash_sound = pygame.mixer.Sound("00. Sounds/dash.wav")
        self.dash_sound.set_volume(0.2)

        self.shuriken_sound = pygame.mixer.Sound("00. Sounds/shurikens.mp3")
        self.shuriken_sound.set_volume(2)

        # Gravity settings
        self.gravity_direction = GRAVITY_DOWN
        self.gravity_force = GRAVITY_DOWN
        
        # Animation settings
        self.animation_counter = 0
        self.animation_delay = 2  # Number of frames to wait before changing the image

        # Shooting settings
        self.flipped = False  # Flag to indicate whether the image is flipped
        self.projectiles = pygame.sprite.Group()  # Group to hold projectiles

        self.size = 200

        # Initialize Sword
        self.sword = Sword(self, self.rect.left, self.rect.top, self.size)
        
        # Burst shooting variables
        self.burst_cooldown = 2  # Cooldown duration in seconds
        self.last_shot_time = 0  # Time of the last burst
        self.burst_active = False  # Flag to indicate if a burst is ongoing
        self.shots_fired_in_burst = 0  # Counter for shots fired in the current burst
        self.shot_interval = 100  # Interval in milliseconds between shots in a burst
        self.last_shot_in_burst_time = 0
        self.total_shurikens = 3  # Number of shurikens in a burst

        # Slash variables
        self.last_slash_time = 0
        self.slash_cooldown = 2
        self.slash_active = False
        
        # Dash variables
        self.dash_cooldown = 10
        self.last_dash_time = 0  # Time of the last dash
        self.dash_distance = 100

        # Cooldown images for shooting, dashing, and slashing
        self.cooldown_image = pygame.transform.scale(pygame.image.load("01. Visual Assets/01. Projectile Sprites/shuriken1.png").convert_alpha(), (50, 50))
        self.cooldown_image_rect = self.cooldown_image.get_rect()
        self.cooldown_image_rect.bottomright = (screen.get_width() - 100, screen.get_height() - 10)
        self.brightened_cooldown_image = self.cooldown_image  # Initialize the brightened image
        
        self.dash_cooldown_image = pygame.transform.scale(pygame.image.load("01. Visual Assets/05. Other Sprites/burst.png").convert_alpha(), (50, 50))
        self.dash_cooldown_image_rect = self.dash_cooldown_image.get_rect()
        self.dash_cooldown_image_rect.bottomright = (screen.get_width() - 30, screen.get_height() - 10)
        self.brightened_dash_cooldown_image = self.dash_cooldown_image  # Initialize the brightened image
        
        self.slash_cooldown_image = pygame.transform.scale(pygame.image.load("01. Visual Assets/02. Sword Sprites/sword1.gif").convert_alpha(), (75, 75))
        self.slash_cooldown_image_rect = self.slash_cooldown_image.get_rect()
        self.slash_cooldown_image_rect.bottomright = (screen.get_width() - 140, screen.get_height() - 4)
        self.brightened_slash_cooldown_image = self.slash_cooldown_image  # Initialize the brightened image
        
        # Health settings
        self.health = 100 

        # Font for health display
        self.font = pygame.font.Font("Migae.otf", 25)

    def adjust_brightness(self, image, factor):
        """
        Adjust the brightness of an image.

        Parameters:
            image (pygame.Surface): The image surface to adjust.
            factor (float): The brightness adjustment factor.

        Returns:
            pygame.Surface: The adjusted image surface.
        """
        width, height = image.get_size()
        new_image = pygame.Surface((width, height)).convert_alpha()
        for x in range(width):
            for y in range(height):
                r, g, b, a = image.get_at((x, y))
                r = min(255, max(0, int(r * factor)))
                g = min(255, max(0, int(g * factor)))
                b = min(255, max(0, int(b * factor)))
                new_image.set_at((x, y), (r, g, b, a))
        return new_image

    def switch_gravity(self):
        """
        Description: Switch the gravity direction and flip the player image.
        Parameters: None
        Returns: None
        """
        self.gravity_direction *= -1
        self.gravity_force *= -1
        self.flipped = not self.flipped
        self.runningAnimation = [pygame.transform.flip(image, False, True) for image in self.runningAnimation]
        self.sword.switch_gravity()

    def shoot(self):
        """
        Description: Initiate shooting projectiles.
        Parameters: None
        Returns: None
        """
        now = time.time()
        if now - self.last_shot_time > self.burst_cooldown:
            self.burst_active = True
            self.shuriken_sound.play()
            self.shots_fired_in_burst = 0
            self.last_shot_time = now  # Update last shot time
            self.last_shot_in_burst_time = pygame.time.get_ticks()  

    def dash(self):
        """
        Description: Initiate dashing.
        Parameters: None
        Returns: None
        """
        now = time.time()
        if now - self.last_dash_time > self.dash_cooldown:
            self.rect.x += self.dash_distance
            self.last_dash_time = now 
            self.dash_sound.play()

    def slash(self):
        """
        Description: Initiate slashing with sword.
        Parameters: None
        Returns: None
        """
        now = time.time()
        if now - self.last_slash_time > self.slash_cooldown:
            self.slash_active = True
            self.last_slash_time = now
            self.slashing.play()

    def update(self, collidable, on_ground, on_ceil):
        """
        Description: Update the player position, animation, projectiles, and cooldowns.

        Parameters:
            collidable (pygame.sprite.Group): Group of collidable sprites.
            on_ground (bool): Flag indicating if the player is on the ground.
            on_ceil (bool): Flag indicating if the player is on the ceiling.
            
        Returns: None
        """
        # Apply gravity
        if self.gravity_direction == GRAVITY_DOWN:
            if self.rect.bottom < self.screen.get_height():
                self.rect.top += self.gravity_force
        else:
            if self.rect.top > 0:
                self.rect.top += self.gravity_force

        # Update animation frame
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.imageNum = (self.imageNum + 1) % len(self.runningAnimation)
            self.image = self.runningAnimation[self.imageNum]
            self.animation_counter = 0  # Reset the counter
            
        collision_list = pygame.sprite.spritecollide(self, collidable, False)

        for obj in collision_list:
            # Calculate the overlap in each direction
            overlap_right = self.rect.right - obj.rect.left
            overlap_left = obj.rect.right - self.rect.left
            overlap_down = self.rect.bottom - obj.rect.top
            overlap_up = obj.rect.bottom - self.rect.top
            
            if on_ground == False and on_ceil == False: 

                # Determine the smallest overlap
                min_overlap = min(overlap_right, overlap_left, overlap_down, overlap_up)

                if min_overlap == overlap_right:
                    # Collision from the right
                    self.rect.right = obj.rect.left
                    
                elif min_overlap == overlap_left:
                    # Collision from the left
                    self.rect.left = obj.rect.right
                    
                elif min_overlap == overlap_down:
                    # Collision from above
                    if self.gravity_direction == GRAVITY_DOWN:
                        self.rect.bottom = obj.rect.top

                elif min_overlap == overlap_up:
                    # Collision from below
                    if self.gravity_direction == GRAVITY_UP:
                        self.rect.top = obj.rect.bottom

                # Check for collisions and correct position
                if overlap_right == min_overlap and self.rect.right > obj.rect.left:
                    self.rect.right = obj.rect.left
                if overlap_left == min_overlap and self.rect.left < obj.rect.right:
                    self.rect.left = obj.rect.right
                if overlap_down == min_overlap and self.rect.bottom > obj.rect.top:
                    self.rect.bottom = obj.rect.top
                if overlap_up == min_overlap and self.rect.top < obj.rect.bottom:
                    self.rect.top = obj.rect.bottom
                    
            else: 
                if self.rect.right >= obj.rect.left: 
                    self.rect.right = obj.rect.left

        # Handle burst shooting
        if self.burst_active:
            now = pygame.time.get_ticks()
            if now - self.last_shot_in_burst_time > self.shot_interval and self.shots_fired_in_burst < self.total_shurikens:
                projectile = Projectile(self.rect.right, self.rect.centery)
                self.projectiles.add(projectile)
                self.shots_fired_in_burst += 1
                self.last_shot_in_burst_time = now  # Update time of last shot within burst
            if self.shots_fired_in_burst >= self.total_shurikens:
                self.burst_active = False

        if self.slash_active:
            now = pygame.time.get_ticks()

            self.sword.swing()  # Trigger sword swing animation
            self.slash_active = False  # Reset slash flag after animation

        # Update projectiles and cooldown images
        self.sword.update(self.rect.left, self.rect.top)  # Update sword position
        self.projectiles.update()  # Update all projectiles

        # Update cooldown bar length based on time passed since last shot and dash
        time_elapsed_shoot = time.time() - self.last_shot_time
        time_elapsed_dash = time.time() - self.last_dash_time
        time_elapsed_slash = time.time() - self.last_slash_time

        # Adjust brightness of cooldown images based on cooldown progress
        cooldown_factor_shoot = min(1, time_elapsed_shoot / self.burst_cooldown)
        cooldown_factor_dash = min(1, time_elapsed_dash / self.dash_cooldown)
        cooldown_factor_slash = min(1, time_elapsed_slash / self.slash_cooldown)
        self.brightened_cooldown_image = self.adjust_brightness(self.cooldown_image, cooldown_factor_shoot)
        self.brightened_dash_cooldown_image = self.adjust_brightness(self.dash_cooldown_image, cooldown_factor_dash)
        self.brightened_slash_cooldown_image = self.adjust_brightness(self.slash_cooldown_image, cooldown_factor_slash)
        
    def draw_health_bar(self, surface, x, y, health, color):
        """
        Description: Draws a health bar on the specified surface.

        Parameters:
            surface (pygame.Surface): The surface to draw the health bar on.
            x (int): The x-coordinate of the top-left corner of the health bar.
            y (int): The y-coordinate of the top-left corner of the health bar.
            health (int): The current health value (0 to 100).
            color ((int, int, int)): The color tuple for the health bar.
            
        Returns: None
        """
        
        if health < 0:
            health = 0
        fill = (health / 100) * BAR_WIDTH
        border_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        
        # Draw bar
        pygame.draw.rect(surface, color, fill_rect)
        pygame.draw.rect(surface, WHITE, border_rect, 2)
        
        # Render Text
        health_text = self.font.render(f"{int(health)}%", True, WHITE)
        surface.blit(health_text, (x + BAR_WIDTH + 10, y))
