"""
Author: Eric Chen & Ryan Chen
Date: June 17 2024
Description: This program file contains the other basic static sprites that don't move, such as the upper/lower boundaries and the background. 
"""

import pygame

WHITE = ((255, 255, 255))
SCREEN_WIDTH = 923.72
SCREEN_HEIGHT = 480

class Boundary(pygame.sprite.Sprite):
    """
    Description: A class to represent boundaries in the game.

    Attributes:
        x (float): The x-coordinate of the boundary.
        y (float): The y-coordinate of the boundary.
        width (float): The width of the boundary.
        height (float): The height of the boundary.
    """
    def __init__(self, x, y, width, height):
        """
        Description: Initialize the boundary sprite.

        Paramters:
            x (float): X-coordinate of the boundary's top-left corner.
            y (float): Y-coordinate of the boundary's top-left corner.
            width (float): Width of the boundary.
            height (float): Height of the boundary.
            
        Returns: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0))  # Fills the boundary with black color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Background(pygame.sprite.Sprite):
    """
    A class to represent the background of the game.

    Attributes:
        screen (pygame.Surface): The surface representing the game window.
    """
    def __init__(self, screen):
        """
        Description: Initialize the background sprite.

        Parameters:
            screen (pygame.Surface): The game window surface.
        
        Returns: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.window = screen
        self.image = pygame.image.load("01. Visual Assets/05. Other Sprites/repeating city bg.png").convert()  # Load and convert background image
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0

        self.boss_image = pygame.image.load("01. Visual Assets/05. Other Sprites/bosscity.png").convert()  # Load boss background image
        self.boss_rect = self.boss_image.get_rect()
        self.boss_rect.left = 0
        self.boss_rect.top = 0

    def update(self):
        """
        Description: Update the background's position and handle fade-in effect.
        Parameters: None
        Returns: None
        """
        self.rect.left -= 10  # Move the background to the left
        if self.rect.right <= self.window.get_width():
            self.rect.left = 0  # Reset background position when it moves off-screen

    def boss_fight(self):
        """
        Description: Switch to boss fight mode by displaying the boss background.
        Parameters: None
        Returns: None
        """
        self.image = self.boss_image  # Set the background image to the boss image

    def normal(self):
        """
        Description: Switch back to normal mode by displaying the regular background.
        Parameters: None
        Returns: None
        """
        self.image = pygame.image.load("01. Visual Assets/05. Other Sprites/repeating city bg.png").convert()  # Set background to regular image

    def draw(self):
        """
        Description: Draw the current background image to the window.
        Parameters: None
        Returns: None
        """
        self.window.blit(self.image, self.rect)  # Draw the main background image
        if self.fade_in_progress or self.boss_alpha > 0:
            self.boss_image.set_alpha(self.boss_alpha)  # Set alpha transparency for boss image
            self.window.blit(self.boss_image, self.boss_rect)  # Draw boss image with transparency

class End_Screen(pygame.sprite.Sprite):
    """
    A class to represent the end screen of the game.

    Attributes:
        screen (pygame.Surface): The surface representing the game window.
    """
    def __init__(self, screen, txt1):
        """
        Description: Initialize the end screen with game over text and instructions.

        Parameters:
            screen (pygame.Surface): The game window surface.
            txt1 (str): Text to display on the end screen.
        
        Returns: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("Migae.otf", 25)  # Load a custom font for the end screen

        self.screen = screen

        game_over_text = self.font.render(txt1, True, WHITE)  
        restart_text = self.font.render("Press RETURN to play again", True, WHITE)  
        quit_text = self.font.render("Press Q to quit", True, WHITE)  

        # Display texts on the screen
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
        # Update the display to show the end screen
        pygame.display.flip()  
