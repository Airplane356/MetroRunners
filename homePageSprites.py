"""
Author: Eric Chen & Ryan Chen
Date: June 17 2024
Description: This file contains the sprites on the home menu screen, such as the Play button and background. 
"""

import pygame

class ImageButton(pygame.sprite.Sprite):
    """
    A class to represent an image button in the game.

    Attributes:
        x (float): The x-coordinate of the image button.
        y (float): The y-coordinate of the image button.
        image_path (str): The file path to the image of the button.
    """

    def __init__(self, x, y, image_path="01. Visual Assets/05. Other Sprites/gamestart.png"):
        """
        Initialize the image button.

        Parameters:
            x (float): The x-coordinate of the image button.
            y (float): The y-coordinate of the image button.
            image_path (str, optional): The file path to the image of the button.

        Returns: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (287, 62))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def is_clicked(self, mouse_pos):
        """
        Check if the button is clicked.

        Parameters:
            mouse_pos (tuple): The position of the mouse cursor (x, y).

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        return self.rect.collidepoint(mouse_pos)

class Instructions(pygame.sprite.Sprite):
    """
    A class to represent an instructions image in the game.

    Attributes:
        x (float): The x-coordinate of the instructions image.
        y (float): The y-coordinate of the instructions image.
        image_path (str): The file path to the image of the instructions.
    """

    def __init__(self, x, y, image_path="01. Visual Assets/05. Other Sprites/instruction.png"):
        """
        Initialize the instructions image.

        Parameters:
            x (float): The x-coordinate of the instructions image.
            y (float): The y-coordinate of the instructions image.
            image_path (str, optional): The file path to the image of the instructions.
            
        Returns: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (250, 250))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class MetroRunners(pygame.sprite.Sprite):
    """
    Description: A class to represent the Metro Runners logo in the game.

    Attributes:
        x (float): The x-coordinate of the Metro Runners logo.
        y (float): The y-coordinate of the Metro Runners logo.
        image_path (str): The file path to the image of the Metro Runners logo.
    """

    def __init__(self, x, y, image_path="01. Visual Assets/05. Other Sprites/Metro Runners.png"):
        """
        Description: Initialize the Metro Runners logo.

        Parameters:
            x (float): The x-coordinate of the Metro Runners logo.
            y (float): The y-coordinate of the Metro Runners logo.
            image_path (str, optional): The file path to the image of the Metro Runners logo. Defaults to "Metro Runners.png".
        
        Returns: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (300, 300))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class CityBackground(pygame.sprite.Sprite):
    """
    Description: A class to represent the city background in the game.

    Attributes:
        x (float): The x-coordinate of the city background.
        y (float): The y-coordinate of the city background.
        image_path (str): The file path to the image of the background.
    """

    def __init__(self, x, y, image_path="01. Visual Assets/05. Other Sprites/city background.png"):
        """
        Initialize the city background.

        Parameters:
            x (float): The x-coordinate of the city background.
            y (float): The y-coordinate of the city background.
            image_path (str, optional): The file path to the image of the background. Defaults to "city background.png".
        
        Returns: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (2400, 500))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 1  # Background movement speed

    def update(self):
        """
        Description: Update the city background's position.

        Move the background horizontally.
        When it reaches the end, reset its position to continue the loop.
        
        Returns: None
        """
        # Move 1 pixel to the left on each frame
        self.rect.left -= 1

        # If we run out of image on the right, reset the left side again
        if self.rect.right <= 923:
            self.rect.left = 0 
