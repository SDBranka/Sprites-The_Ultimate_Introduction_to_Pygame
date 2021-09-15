import pygame
from sys import exit
import math
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # animating the player
        player_walk_1 = pygame.image.load("img/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("img/player/player_walk_2.png").convert_alpha()
        # list containing the two walk animation pics controlled by player_index
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("img/player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        path_to_sound = "audio/jump.mp3"
        self.jump_sound = pygame.mixer.Sound(path_to_sound)
        # set sound volume. Between 0(silent) and 1(full volume)
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        # if player is on the ground and space bar is pressed player jump
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -21
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        # creates appearance of solid floor
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        # display jump surface when player is in the air
        if self.rect.bottom < 300:
            self.image = self.player_jump
        # play walking animation if the player is on the floor    
        else:
            # increasing the index by small increments extends how many frames an index position is displayed for
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly":
            fly_frame_1 = pygame.image.load("img/fly/fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("img/fly/fly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load("img/snail/snail1.png").convert_alpha()
            snail_frame_2 = pygame.image.load("img/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    # determines and sets image to display
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    # if obstacle instance moves offscreen, destroy it
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    # updates image display and position
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()


# function to consistantly update and redraw score_surface
def display_score():
    current_time = (pygame.time.get_ticks() - start_time) / 1000
    score_surface = test_font.render(f"Score: {math.floor(current_time)}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(midtop = (400, 27))
    screen.blit(score_surface, score_rect)
    return current_time

# checks to see if a collision has occured between sprites, returns boolean value (to game_active)
    # spritecollide(sprite_to_check, group_to_check, dokill) returns list of collided sprites
        # if dokill is set to true on contact the group sprite would be deleted
def collision_sprite():
    sprite_to_check = player.sprite
    group_to_check = obstacle_group
    dokill = False
    if pygame.sprite.spritecollide(sprite_to_check, group_to_check, dokill):
        obstacle_group.empty()
        return False
    else:
        return True


# initialize pygame
pygame.init()

# setup display surface
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
# rename screen title
pygame.display.set_caption("Pixel Runner")

# controlling the framerate
clock = pygame.time.Clock()

# creating a font
font_type = "font/Pixeltype.ttf"
font_size = 50
test_font = pygame.font.Font(font_type, font_size)

# Setting up game states
    # setting to false starts game from intro/game over screen
game_active = False

# building to be able to reset the score/timer count to zero with new game
start_time = 0

# store the score for global use
score = 0

# create a GroupSingle instance of Player 
player = pygame.sprite.GroupSingle()
player.add(Player())

# create a sprite group for obstacles
obstacle_group = pygame.sprite.Group()

# create a surface with an image
sky_surface = pygame.image.load('img/Sky.png').convert()

# create a ground surface with an image
ground_surface = pygame.image.load('img/ground.png').convert()

# creating player surface for game over/intro screen
player_stand = pygame.image.load("img/player/player_stand.png").convert_alpha()
pss_surface_to_use = player_stand
pss_rotation_angle = 0
pss_scale = 2
player_stand = pygame.transform.rotozoom(pss_surface_to_use, pss_rotation_angle, pss_scale)
player_stand_rect = player_stand.get_rect(center = (400, 200))

# game name
game_name = test_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_msg = test_font.render("Press space to run", False, (111, 196, 169))
game_msg_rect = game_msg.get_rect(center = (400, 330))

# timers
# controls when new obstacles are generated
obstacle_timer = pygame.USEREVENT + 1
event_to_trigger = obstacle_timer
how_often_to_trigger = 1500
pygame.time.set_timer(event_to_trigger, how_often_to_trigger)


# game loop
while True:
    # event loop
    for event in pygame.event.get():
        # if user clicks the window close button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:      
            # timers
            # enemy/obstacle deployment timer 
            if event.type == obstacle_timer:
                # add an instance of Obstacle to obstacle_group, the type is random 25%chance fly 75% chance snail
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))
        else:
            # user presses space bar to restart game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    # snail_rect.left = 800
                    start_time = pygame.time.get_ticks()
        
    # game display
    if game_active:
        # display sky_surface
        sky_pos_x = 0
        sky_pos_y = 0
        screen.blit(sky_surface, (sky_pos_x, sky_pos_y))
        # display ground_surface
        screen.blit(ground_surface, (0, 300))
        # store score and display
        score = display_score()
        # display player
        player.draw(screen)
        player.update()
        # display obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # checks to see if collision has occured, if collision game_active is turned to False ending the game
        game_active = collision_sprite()

    # if game_active is false(new game/player death) display intro/game over screen
    else:
        # draw screen
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        score_msg = test_font.render(f"Your score: {math.floor(score)}", False, (111, 196, 169))
        score_msg_rect = score_msg.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)
        # if no score prompt to start game, if score display score
        if score == 0:
            screen.blit(game_msg, game_msg_rect)
        else:
            screen.blit(score_msg, score_msg_rect)

    # update what is displayed on screen
    pygame.display.update()
    # sets so that while True loop should not run faster than framerate_ceiling times per second
    framerate_ceiling = 60
    clock.tick(framerate_ceiling)












