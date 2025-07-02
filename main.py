"""
Authors: Eric Chen & Ryan Chen
Date: June 17 2024
Description: This is the main program file for METRO RUNNERS. This follows the IDEA/ALTER framework. 
"""

import pygame
import playerSprites
import movingSprites
import staticSprites
import homePageSprites
import random
import time

class MetroRunnersGame:
    """
    Description: Class representing the main game logic and interaction for Metro Runners.

    Attributes:
        SCREEN_WIDTH (int): Width of the game screen.
        SCREEN_HEIGHT (int): Height of the game screen.
        player (playerSprites.Player): Instance of the player character.
        sword (pygame.sprite.Group): Group for sword projectiles.
        obstacles (pygame.sprite.Group): Group for obstacles in the game.
        gems_group (pygame.sprite.Group): Group for gems collectibles.
        all_sprites (pygame.sprite.Group): Group containing all sprites for rendering.
        projectile_upgrade (int): Upgrade level for projectiles.
        sword_upgrade (int): Upgrade level for sword.
        dash_upgrade (int): Upgrade level for dash ability.
        cycle (int): Cycle count for upgrades.
        boss (movingSprites.Boss): Instance of the boss character.
        score (int): Current score in the game.
        start_time (float): Time when the game started.
        gems_collected (int): Number of gems collected.
        gem_icon (pygame.Surface): Icon representing collected gems.
        gem_icon_rect (pygame.Rect): Rectangle representing the position of the gem icon.
    """

    def __init__(self):
        """Initialize the game."""
        
        # Define screen dimensions and colors
        self.SCREEN_WIDTH = 923.72
        self.SCREEN_HEIGHT = 480
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)

        pygame.init()
        
        # Initialize sounds, game variables, and create the display
        self.sound()
        self.game_variables()

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Metro Runners")
        
        # Initialize background and sprite entities
        self.backgound_entities()
        self.sprite_entities()
        
    def alter(self):
        """Main game loop."""
        
        self.clock = pygame.time.Clock()
        
        while self.running:
            self.clock.tick(30)  # Cap the frame rate at 30 FPS

            self.handle_events()  # Handle user input events

            self.update_game()  # Update game state and logic
            
            # Draw home page when game is not active
            if not self.game_active:
                if not self.end_game:
                    self.home_menu()

            # Draw cooldown images and refresh display when game is active
            if self.game_active:
                self.screen.blit(self.player.brightened_cooldown_image, self.player.cooldown_image_rect)
                self.screen.blit(self.player.brightened_dash_cooldown_image, self.player.dash_cooldown_image_rect)
                self.screen.blit(self.player.brightened_slash_cooldown_image, self.player.slash_cooldown_image_rect)

            pygame.display.flip()  # Update the full display surface

        pygame.quit()  # Quit pygame when game loop ends

    def handle_events(self):
        """
        Description: Handle events (keyboard, mouse, etc.) during the game.
        Parameters: None
        Returns: None 
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False  # Exit the game loop when window is closed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the start button is clicked to begin the game
                if self.button.is_clicked(pygame.mouse.get_pos()):
                    self.end_game = False
                    self.button.kill()
                    self.logo.kill()
                    self.background_home.kill()
                    self.game_active = True
            elif event.type == pygame.KEYDOWN:
                # Handle key presses during gameplay
                current_time = pygame.time.get_ticks()
                if event.key == pygame.K_SPACE and self.gravity_switches < self.max_gravity_switches:
                    self.player.switch_gravity()
                    self.gravity_switches += 1
                    self.gravity_last_used = current_time
                if event.key == pygame.K_d and current_time - self.shoot_last_used >= self.shoot_cooldown_time and self.game_active == True:
                    self.player.shoot()
                    self.shoot_last_used = current_time
                if event.key == pygame.K_e and current_time - self.dash_last_used >= self.dash_cooldown_time and self.game_active == True:
                    self.player.dash()
                    self.dash_last_used = current_time
                if event.key == pygame.K_f and current_time - self.slash_last_used >= self.slash_cooldown_time and self.game_active == True:
                    self.player.slash()
                    self.sword.add(self.player.sword)
                    self.slash_last_used = current_time
                if self.end_game:
                    if event.key == pygame.K_RETURN:
                        self.end_game = False
                        self.home_menu()
                    if event.key == pygame.K_q:
                        self.running = False

    def update_game(self):
        """
        Description: Update game elements
        Parameters: None
        Returns: None
        """

        self.background_home.update()  # Update moving background
        
        if self.game_active:
            self.generate_obstacle()  # Generate obstacles
            self.generate_gems()  # Generate gems
            
            self.detect_collision()  # Check for collisions
            
            self.score += 1  # Increase score over time

            if self.score >= 2500:
                self.final_boss()  # Trigger final boss battle if score reaches threshold
            
            self.update_sprites()  # Update and draw all sprites
            
            self.check_off_map()
            self.check_death()
                    
            
            self.ScoreKeeper()  # Display current score and gems collected
            
    def check_off_map(self): 
        # Check if player is knocked off the map
        if self.player.rect.centerx <= 0:
            self.player.health -= 10
            if self.player.health <= -10:
                self.death_sound.play()
                self.game_active = False
                self.end_game = True
                if self.end_game == True:
                    staticSprites.End_Screen(self.screen, "You lost!")
                    self.reset_game()
                    
        if self.player.rect.centerx >= 650: 
            self.player.health -= 5

    def update_sprites(self):
        """
        Description: Update sprite positions and draw them on the screen.
        Parameters: None
        Returns: None
        """

        if not self.end_game:
            self.all_sprites.update()
            self.player.update(self.obstacles, self.on_ground, self.on_ceil)

            self.screen.fill(self.WHITE)

            self.all_sprites.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)

            self.gems_group.update()
            self.gems_group.draw(self.screen)

            self.player.projectiles.update()
            self.player.projectiles.draw(self.screen)

            self.sword.draw(self.screen)

            self.obstacles.update()

            self.player.draw_health_bar(self.screen, 650, 20, self.player.health, (124, 252, 0))

            if self.boss_spawned:
                self.boss.draw_health_bar(self.screen, 650, 40, self.boss.health, (138, 43, 226))

    def sound(self):
        """
        Description: Load and initialize game sounds and music
        Parameters: None
        Returns: None
        """

        self.death_sound = pygame.mixer.Sound("00. Sounds/death.mp3")
        self.death_sound.set_volume(0.3)

        self.car_kill = pygame.mixer.Sound("00. Sounds/car.mp3")
        self.car_kill.set_volume(0.5)

        self.player_hit = pygame.mixer.Sound("00. Sounds/hit.mp3")
        self.player_hit.set_volume(0.4)

        self.gem_sfx = pygame.mixer.Sound("00. Sounds/Gem Sound Effect 1.mp3")
        self.gem_sfx.set_volume(0.1)

        self.win = pygame.mixer.Sound("00. Sounds/Victory sound effects (no copyright).mp3")
        self.win.set_volume(0.3)
        
        self.hit = pygame.mixer.Sound("00. Sounds/hit.mp3")
        self.hit.set_volume(0.4)
        
        self.monster = pygame.mixer.Sound("00. Sounds/monster.mp3")
        self.monster.set_volume(0.1)

        self.dashu_sound = pygame.mixer.Sound("00. Sounds/Upgrade dash.mp3")
        self.dashu_sound.set_volume(1.5)
        self.swordu_sound = pygame.mixer.Sound("00. Sounds/upgrade sword.mp3")
        self.swordu_sound.set_volume(1.5)
        self.shurikenu_sound = pygame.mixer.Sound("00. Sounds/Upgrade shurikan.mp3")
        self.shurikenu_sound.set_volume(1.5)

        self.upgrade = pygame.mixer.Sound("00. Sounds/Upgrade Sound Effect.mp3")
        self.upgrade.set_volume(0.3)

        # Background Music
        pygame.mixer.music.load("00. Sounds/SongBG.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def game_variables(self):
        """
        Description: Initialize game control variables and settings.
        Parameters: None
        Returns: None
        """

        self.running = True
        self.game_active = False
        self.gravity_switch_allowed = True
        self.slash_allowed = True
        self.shoot_allowed = True
        self.dash_allowed = True
        self.on_ground = True
        self.on_ceil = False
        self.end_game = False
        self.boss_spawned = False

        self.gravity_switches = 0
        self.max_gravity_switches = 2

        self.gravity_cooldown_time = 3000
        self.slash_cooldown_time = 2000
        self.shoot_cooldown_time = 1000
        self.dash_cooldown_time = 1000
        
        # Add damage cooldown variables
        self.damage_cooldown_time = 1000  # 1 second cooldown
        self.last_damage_time = 0

        self.gravity_last_used = -self.gravity_cooldown_time
        self.slash_last_used = -self.slash_cooldown_time
        self.shoot_last_used = -self.shoot_cooldown_time
        self.dash_last_used = -self.dash_cooldown_time

        self.font = pygame.font.Font("Migae.otf", 25)

    def backgound_entities(self):
        """
        Description: Initialize background entities.
        Parameters: None
        Returns: None
        """

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.WHITE)
        self.screen.blit(self.background, (0, 0))

        self.boundary_top = staticSprites.Boundary(0, 0, self.SCREEN_WIDTH, 1)
        self.boundary_bottom = staticSprites.Boundary(0, self.SCREEN_HEIGHT - 5, self.SCREEN_WIDTH, 1)
        self.bg = staticSprites.Background(self.screen)

        self.all_sprites = pygame.sprite.OrderedUpdates(self.bg, self.boundary_top, self.boundary_bottom)

        # Create home menu sprites
        self.button = homePageSprites.ImageButton(310, 300)
        self.instructions = homePageSprites.Instructions(630, 120)
        self.logo = homePageSprites.MetroRunners(300, 10)
        self.background_home = homePageSprites.CityBackground(0, 0)
        
    def sprite_entities(self):
        """
        Description: Initialize various game sprites and entities.
        Parameters: None
        Returns: None
        """
        # E - ENTITIES

        # initiate player sprite
        self.player = playerSprites.Player(self.screen)
        self.sword = pygame.sprite.Group()

        # Add obstacles
        self.obstacles = pygame.sprite.Group()
        self.obstacle = movingSprites.Obstacle(self.SCREEN_WIDTH + random.randint(100, 500),
                                               random.randint(self.SCREEN_HEIGHT // 2, self.SCREEN_HEIGHT - 50),
                                               30, 30, 10)
        self.obstacles.add(self.obstacle)
        self.all_sprites.add(self.obstacle)

        # Add Gems
        self.gems_group = pygame.sprite.Group()
        self.gem = movingSprites.Gems(self.SCREEN_WIDTH + random.randint(100, 500),
                                      random.randint(self.SCREEN_HEIGHT // 2, self.SCREEN_HEIGHT - 50), 10,
                                      random.randrange(0, 4))
        self.gems_group.add(self.gem)
        self.all_sprites.add(self.gem)

        # Initialize upgrades and game cycle
        self.projectile_upgrade = 10
        self.sword_upgrade = 10
        self.dash_upgrade = 10
        self.cycle = 1

        # Boss
        self.boss = movingSprites.Boss()

        # Score and gem count
        self.score = 0
        self.start_time = time.time()
        self.gems_collected = 0

        # Load gem icon for display
        self.gem_icon = pygame.transform.scale(pygame.image.load("01. Visual Assets/04. Gem Sprites/gem1.png").convert_alpha(), (25, 25))
        self.gem_icon_rect = self.gem_icon.get_rect()
        self.gem_icon_rect.topleft = (10, 50)

    def generate_obstacle(self):
        """
        Description: Generate obstacles in the game if there are none currently on screen.
        Parameters: None
        Returns: None
        """
        # Check if there are any obstacles on the screen
        if not self.obstacles:
            # Generate a new obstacle

            self.obstacle = movingSprites.Obstacle(
                self.SCREEN_WIDTH + random.randint(100, 500),
                random.randint(self.SCREEN_HEIGHT // 2, self.SCREEN_HEIGHT - 50),
                30, 30, 10
            )
            
            if not pygame.sprite.spritecollideany(self.obstacle, self.obstacles):
                self.obstacles.add(self.obstacle)
                self.all_sprites.add(self.obstacle)

    def generate_gems(self):
        """
        Description: Generate gems in the game if there are none currently on screen.
        Parameters: None
        Returns: None
        """
        # Check if there are any gems on the screen
        if not self.gems_group and not self.boss_spawned:
            # Generate a new gem
            self.gem = movingSprites.Gems(
                self.SCREEN_WIDTH + random.randint(100, 500),
                random.randint(self.SCREEN_HEIGHT // 2, self.SCREEN_HEIGHT - 50), 10, random.randrange(0, 4))
            self.gems_group.add(self.gem)
            self.all_sprites.add(self.gem)

    def detect_collision(self):
        """
        Description: Detect collisions between game entities and handle interactions accordingly.
        Parameters: None
        Returns: None
        """
        # Check for collisions with the top and bottom boundaries
        if pygame.sprite.collide_rect(self.player, self.boundary_top):
            self.on_ceil = True
            self.on_ground = False
        elif pygame.sprite.collide_rect(self.player, self.boundary_bottom):
            self.on_ground = True
            self.on_ceil = False
        else:
            self.on_ground = False
            self.on_ceil = False

        # Reset gravity switches if the player touches the ground
        if self.on_ground or self.on_ceil:
            self.gravity_switches = 0
            
        # Check for player collision with obstacles
        current_time = pygame.time.get_ticks()
        if pygame.sprite.spritecollideany(self.player, self.obstacles):
            if self.player.rect.x < self.obstacle.rect.x:
                self.player.health -= 2
                if current_time - self.last_damage_time >= self.damage_cooldown_time:
                    
                    # Handle collision
                    self.hit.play()
                    self.last_damage_time = current_time
                    if self.player.health <= -10:
                        self.death_sound.play()
                        self.game_active = False
                        self.end_game = True
                        if self.end_game == True:
                            staticSprites.End_Screen(self.screen, "You lost!")
                            self.reset_game()

        # Check for collisions between player projectiles and obstacles
        for projectile in self.player.projectiles:
            obstacle_hit = pygame.sprite.spritecollideany(projectile, self.obstacles)
            if obstacle_hit:
                # Remove the obstacle and projectile when they collide
                self.score += 40
                obstacle_hit.kill()
                projectile.kill()
                self.car_kill.play()

        # Collision between projectile and boss
        obstacle_hit_boss = pygame.sprite.spritecollide(self.boss, self.player.projectiles, True)
        if obstacle_hit_boss:
            self.boss.health -= 4
            self.monster.play()
            if self.boss.health <= -4:
                self.boss_spawned = False
                self.boss.kill()
                self.game_active = False
                self.end_game = True
                self.reset_game()
                staticSprites.End_Screen(self.screen, "CONGRATS! YOU WON!")
                self.win.play()

        # Check for player collision with gems
        for gem in self.gems_group:
            gem_collect = pygame.sprite.spritecollideany(self.player, self.gems_group)
            if gem_collect:
                gem_collect.kill()
                self.gems_collected += 1
                self.gem_sfx.play()
            if self.cycle == 1 and self.gems_collected >= self.projectile_upgrade:
                self.gems_collected = 0
                self.projectile_upgrade += 5
                self.cycle += 1
                self.upgrade.play()
                self.shurikenu_sound.play()
                self.upgrade_projectiles()
            if self.cycle == 2 and self.gems_collected >= self.sword_upgrade:
                self.gems_collected = 0
                self.sword_upgrade += 5
                self.cycle += 1
                self.upgrade.play()
                self.swordu_sound.play()
                self.upgrade_sword()
            if self.cycle == 3 and self.gems_collected >= self.dash_upgrade:
                self.gems_collected = 0
                self.dash_upgrade += 5
                self.cycle = 1
                self.dashu_sound.play()
                self.upgrade_dash()

        # Check for sword collisions with obstacles
        for sword in self.sword:
            obstacle_hit = pygame.sprite.spritecollideany(sword, self.obstacles)
            if obstacle_hit:
                self.score += 40
                obstacle_hit.kill()
                self.car_kill.play()

    def ScoreKeeper(self):
        """
        Description: Display the current score and number of gems collected on the game screen.
        Parameters: None
        Returns: None
        """
        # Draw score and gems collected
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        gems_text = self.font.render(f"x{self.gems_collected}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(self.gem_icon, self.gem_icon_rect)
        self.screen.blit(gems_text, (self.gem_icon_rect.right + 10, self.gem_icon_rect.top))

    def check_death(self):
        """
        Description: Check if the player's health drops below zero, indicating game over.
        Parameters: None
        Returns: None
        """
        if self.player.health <= -10:
            self.death_sound.play()
            self.game_active = False
            self.end_game = True
            if self.end_game == True:
                staticSprites.End_Screen(self.screen, "You lost!")
                self.reset_game()

    def upgrade_projectiles(self):
        """
        Description: Upgrade the player's projectile abilities.
        Parameters: None
        Returns: None
        """
        self.player.total_shurikens += 1

    def upgrade_dash(self):
        """
        Description: Upgrade the player's dash ability.
        Parameters: None
        Returns: None
        """
        self.player.dash_cooldown -= 1.5
        self.player.dash_distance += 25

    def upgrade_sword(self):
        """
        Description: Upgrade the player's sword.
        Parameters: None
        Returns: None
        """
        self.player.size += 50

    def reset_game(self):
        """
        Description: Reset game parameters to their initial state after game over.
        Parameters: None
        Returns: None
        """
        self.score = 0
        self.gems_collected = 0
        self.gravity_switches = 0
        self.player.health = 100
        self.player.rect.centerx = self.SCREEN_WIDTH // 2
        self.player.rect.centery = self.SCREEN_HEIGHT // 2
        self.obstacles.empty()
        self.gems_group.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.bg, self.boundary_top, self.boundary_bottom)
        self.boss.rect.right = 1300
        self.boss.health = 100
        self.bg.normal()
        self.boss_spawned = False
        self.player.total_shurikens = 3
        self.player.dash_distance = 100
        self.player.dash_cooldown = 10
        self.player.size = 100
        self.projectile_upgrade = 10
        self.sword_upgrade = 10
        self.dash_upgrade = 10
                    
    def home_menu(self):
        """
        Description: Display the home menu page
        Parameters: None
        Returns: None
        """
        # Draw elements
        self.screen.blit(self.background_home.image, self.background_home.rect)
        self.screen.blit(self.button.image, self.button.rect)
        self.screen.blit(self.logo.image, self.logo.rect)
        self.screen.blit(self.instructions.image, self.instructions.rect)

    def final_boss(self): 
        """
        Description: Spawns the final boss
        Parameters: None
        Returns: None
        """
        self.all_sprites.add(self.boss)
        self.bg.boss_fight()
        self.boss_spawned = True
    
MetroRunnersGame().alter()