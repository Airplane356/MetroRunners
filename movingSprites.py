"""
Author: Eric Chen & Ryan Chen
Date: June 17 2024
Description: This program file contains all of the moving sprites in the main game such as the obstacles, gems, & projectiles. 
"""

import pygame
import random

SCREEN_WIDTH = 923.72
SCREEN_HEIGHT = 480
WHITE = (255, 255, 255)
BAR_WIDTH = 200
BAR_HEIGHT = 20

class Obstacle(pygame.sprite.Sprite):
    """
    A class to represent obstacles in the game.

    Attributes:
        x (float): The x-coordinate of the obstacle.
        y (float): The y-coordinate of the obstacle.
        width (float): The width of the obstacle.
        height (float): The height of the obstacle.
        speed (int): The speed at which the obstacle moves.
        imgpath (str): The file path to the image of the obstacle.
    """
    def __init__(self, x, y, width, height, speed, imgpath="01. Visual Assets/05. Other Sprites/flying car.png"):
        """
        Initialize an Obstacle instance.

        Parameters:
            x (float): The x-coordinate of the obstacle.
            y (float): The y-coordinate of the obstacle.
            width (float): The width of the obstacle.
            height (float): The height of the obstacle.
            speed (int): The speed at which the obstacle moves.
            imgpath (str): The file path to the image of the obstacle.
            
        Returns: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(imgpath).convert_alpha(), (100, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        """
        Description: Update the obstacle's position.

        Move the obstacle to the left based on its speed.
        If the obstacle moves off the screen, reset its position to the right
        and randomize its height for variation.
        
        Parameters: None
        Returns: None
        """
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
            self.rect.bottom = random.randint(50, SCREEN_HEIGHT - 50)
            
class Gems(pygame.sprite.Sprite): 
    """
    A class to represent gems in the game.

    Attributes:
        x (float): The x-coordinate of the gem.
        y (float): The y-coordinate of the gem.
        speed (int): The speed at which the gem moves.
        image_index (int): The index to choose the gem image.
        img1 (str): The file path to the first gem image.
        img2 (str): The file path to the second gem image.
        img3 (str): The file path to the third gem image.
        img4 (str): The file path to the fourth gem image.
    """
    def __init__(self, x, y, speed, image_index, img1="01. Visual Assets/04. Gem Sprites/gem1.png", 
                 img2="01. Visual Assets/04. Gem Sprites/gem2.png", 
                 img3="01. Visual Assets/04. Gem Sprites/gem3.png",
                 img4="01. Visual Assets/04. Gem Sprites/gem4.png"):
        """
        Description: Initialize a Gems instance.

        Parameters:
            x (float): The x-coordinate of the gem.
            y (float): The y-coordinate of the gem.
            speed (int): The speed at which the gem moves.
            image_index (int): The index to choose the gem image.
            img1 (str): The file path to the first gem image. 
            img2 (str): The file path to the second gem image. 
            img3 (str): The file path to the third gem image. 
            img4 (str): The file path to the fourth gem image. 
        
        Parameters: None
        Returns: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(img1).convert_alpha(), pygame.image.load(img2).convert_alpha(), 
                       pygame.image.load(img3).convert_alpha(), pygame.image.load(img4).convert_alpha()]
        self.image = pygame.transform.scale(self.images[image_index], (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        
    def update(self): 
        """
        Description: Update the gem's position.

        Move the gem to the left based on its speed.
        If the gem moves off the screen, remove it from all sprite groups.
        
        Parameters: None
        Returns: None
        """
        self.rect.x -= self.speed
        if self.rect.right < 0: 
            self.kill() 

            
class Projectile(pygame.sprite.Sprite):
    """
    A class to represent projectiles in the game.

    Attributes:
        x (float): The x-coordinate of the projectile.
        y (float): The y-coordinate of the projectile.
        images (list): A list of images for the projectile animation.
        image_index (int): The current index of the image being displayed.
        speed (int): The speed at which the projectile moves.
        last_update (int): The time of the last update.
        animation_delay (int): The delay between animation frames in milliseconds.
    """
    def __init__(self, x, y, image1="01. Visual Assets/01. Projectile Sprites/shuriken1.png", 
                 image2="01. Visual Assets/01. Projectile Sprites/shuriken2.png",
                 image3 = "01. Visual Assets/01. Projectile Sprites/shuriken3.png", 
                 image4="01. Visual Assets/01. Projectile Sprites/shuriken4.png"):
        """
        Description: Initialize a Projectile instance.

        Parameters:
            x (float): The x-coordinate of the projectile.
            y (float): The y-coordinate of the projectile.
            image1 (str): The file path to the first image of the projectile. 
            image2 (str): The file path to the second image of the projectile. 
            image3 (str): The file path to the third image of the projectile. 
            image4 (str): The file path to the fourth image of the projectile. 
            
        Returns: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(image1).convert_alpha(), pygame.image.load(image2).convert_alpha(), 
                       pygame.image.load(image3).convert_alpha(), pygame.image.load(image4).convert_alpha()]
        self.image_index = 0
        self.image = pygame.transform.scale(self.images[self.image_index], (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 15
        self.last_update = pygame.time.get_ticks()  # Track the time of the last update
        self.animation_delay = 2  # Milliseconds between frame updates
        self.animation_count = 0 
        self.imageNum = 0 

    def update(self):
        """
        Description: Update the projectile's position and animate its image.

        Move the projectile to the right based on its speed.
        Alternate between the images for animation.
        If the projectile moves off the screen, remove it from all sprite groups.
        
        Parameters: None
        Returns: None
        """
        now = pygame.time.get_ticks()
        # Check if it's time to update the frame
        if now - self.last_update > self.animation_delay:
            self.last_update = now
            # Alternate between the two images
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = pygame.transform.scale(self.images[self.image_index], (25,25)) 
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class Sword(pygame.sprite.Sprite):
    """
    A class to represent a sword in the game.

    Attributes:
        player (object): The player object.
        images (list): A list of images for the sword animation.
        image (Surface): The current image of the sword.
        size (int): The size of the sword.
        rect (Rect): The rectangle representing the sword's position.
        is_swinging (bool): A flag indicating whether the sword is swinging.
        frame_index (int): The current frame index in the animation.
        animation_speed (float): The speed of the animation.
        current_time (int): The current time.
        last_update (int): The time of the last update.
        flipped (bool): A flag indicating whether the sword is flipped.
    """
    def __init__(self, player, y, x, size, 
                 image1 = "01. Visual Assets/02. Sword Sprites/sword1.gif", 
                 image2 = "01. Visual Assets/02. Sword Sprites/sword2.gif", 
                 image3 = "01. Visual Assets/02. Sword Sprites/sword3.gif", 
                 image4 = "01. Visual Assets/02. Sword Sprites/sword4.gif",
                 image5 = "01. Visual Assets/02. Sword Sprites/sword5.gif"):
        """
        Description: Initialize a Sword instance.

        Parameters:
            player (object): The player object.
            y (float): The y-coordinate of the sword.
            x (float): The x-coordinate of the sword.
            size (int): The size of the sword.
            image1 (str): The file path to the first image of the sword. 
            image2 (str): The file path to the second image of the sword. 
            image3 (str): The file path to the third image of the sword. 
            image4 (str): The file path to the fourth image of the sword. 
            image5 (str): The file path to the fifth image of the sword.
            
        Returns: None 
        """
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.images = [pygame.image.load(image1).convert_alpha(), pygame.image.load(image2).convert_alpha(), 
                       pygame.image.load(image3).convert_alpha(), pygame.image.load(image4).convert_alpha(), 
                       pygame.image.load(image5).convert_alpha()]
        
        self.image = self.images[0]
        self.size = size
        self.rect = self.image.get_rect()
        self.rect.left = (y-50)
        self.rect.top = (x-60)
        
        # Some control variables
        self.is_swinging = False
        self.frame_index = 0
        self.animation_speed = 0.4
        self.current_time = 0
        self.last_update = 0
        self.flipped = False

    def update(self, y, x):
        """
        Description: Update the sword's position and animation.

        Parameters:
            y (float): The y-coordinate of the sword.
            x (float): The x-coordinate of the sword.
            
        Returns: None
        """
        self.rect.left = (y-50)
        self.rect.top = (x-60)

        # Flip the sword animation if player is flipped
        if self.flipped:
            self.images = [pygame.transform.flip(image, False, True) for image in self.images]
            
        # Animate the sword
        if self.is_swinging:
            self.current_time += pygame.time.get_ticks()
            if self.current_time - self.last_update > self.animation_speed:
                self.last_update = self.current_time
                self.images[self.frame_index] = pygame.transform.scale(self.images[self.frame_index], (self.size, self.size))
                self.frame_index += 1
                if self.frame_index >= 5:
                    self.frame_index = 0
                    self.is_swinging = False
                    self.kill()
                self.image = self.images[self.frame_index]
    
    def swing(self):
        """
        Description: Initiate the swinging animation for the sword.
        Parameters: None
        Returns: None
        """
        if not self.is_swinging:
            self.is_swinging = True
            self.frame_index = 0
            self.current_time = 0
            self.last_update = 0

    def switch_gravity(self):
        """
        Description: Switch the gravity for the sword, flipping its orientation.
        Parameters: None
        Returns: None
        """
        self.flipped = not self.flipped

class Boss(pygame.sprite.Sprite):
    """
    A class to represent the boss in the game.

    Attributes:
        images (list): A list of images for the boss animation.
        image_index (int): The current index of the image being displayed.
        image (Surface): The current image of the boss.
        is_animated (bool): A flag indicating whether the boss is animated.
        animation_speed (float): The speed of the animation.
        current_time (int): The current time.
        last_update (int): The time of the last update.
        rect (Rect): The rectangle representing the boss's position.
        health (int): The health of the boss.
        font (Font): The font used for rendering text.
    """
    def __init__(self, 
                 image1="01. Visual Assets/03. Monster Sprites/monster1.gif", 
                 image2="01. Visual Assets/03. Monster Sprites/monster2.gif", 
                 image3="01. Visual Assets/03. Monster Sprites/monster3.gif", 
                 image4="01. Visual Assets/03. Monster Sprites/monster4.gif", 
                 image5="01. Visual Assets/03. Monster Sprites/monster5.gif"):
        """
        Description: Initialize a Boss instance.

        Parameters:
            image1 (str): The file path to the first image of the boss. 
            image2 (str): The file path to the second image of the boss. 
            image3 (str): The file path to the third image of the boss. 
            image4 (str): The file path to the fourth image of the boss. 
            image5 (str): The file path to the fifth image of the boss. 
        
        Returns: None
        """
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load(image1).convert_alpha(), pygame.image.load(image2).convert_alpha(), 
                       pygame.image.load(image3).convert_alpha(), pygame.image.load(image4).convert_alpha(),
                       pygame.image.load(image5).convert_alpha()]
        self.image_index = 0
        self.image = pygame.transform.scale(self.images[self.image_index], (300,300))  # Adjust size as needed

        self.is_animated = False
        self.animation_speed = 0.4
        self.current_time = 0
        self.last_update = 0

        # Set boss position
        self.rect = self.image.get_rect()
        self.rect.left = 1300
        self.rect.y = 80

        self.health = 100

        # font 
        self.font = pygame.font.Font("Migae.otf", 25)

    def update(self):
        """
        Description: Update the boss's position and animate its image.

        Move the boss left until it reaches a certain position.
        Alternate between the images for animation.
        
        Parameters: None
        Returns: None
        """
        if self.rect.right >= SCREEN_WIDTH + 100: 
            self.rect.left -= 50

        # Animate 
        self.current_time += pygame.time.get_ticks()
        if self.current_time - self.last_update > self.animation_speed:
            self.last_update = self.current_time
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = pygame.transform.scale(self.images[self.image_index], (300,300)) 

    def draw_health_bar(self, surface, x, y, health, color):
        """
        Draw the health bar on the screen.

        Parameters:
            surface (Surface): The surface on which to draw the health bar.
            x (float): The x-coordinate of the health bar.
            y (float): The y-coordinate of the health bar.
            health (int): The current health of the boss.
            color (tuple): The color of the health bar.
            
        Returns: None
        """
        if self.health < 0:
            self.health = 0
        self.color = color
        fill = (self.health / 100) * BAR_WIDTH
        border_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, self.color, fill_rect)
        pygame.draw.rect(surface, WHITE, border_rect, 2)
        health_text = self.font.render(f"{int(self.health)}%", True, WHITE)
        surface.blit(health_text, (x + BAR_WIDTH + 10, y))
