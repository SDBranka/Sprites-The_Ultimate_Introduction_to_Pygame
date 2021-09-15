import pygame
from sys import exit
import math
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # animating the player
        player_walk_1 = pygame.image.load("img/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("img/player/player_walk_2.png").convert_alpha()
        # list containing the two walk animation pics controlled by player_index
        self.player_index = 0
        self.player_jump = pygame.image.load("img/player/jump.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        # if player is on the ground and space bar is pressed player jump
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

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
            if self.player_index >= len(player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


# function to consistantly update and redraw score_surface
def display_score():
    current_time = (pygame.time.get_ticks() - start_time) / 1000
    score_surface = test_font.render(f"Score: {math.floor(current_time)}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(midtop = (400, 27))
    screen.blit(score_surface, score_rect)
    return current_time

# determines obstacle type, moves obstacles, and deletes obstacles that have left the screen
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5            
            # determine which type of obstacle to draw and then draw
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        # delete obstacles that have left the screen
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    return []

# determines if collision between obstacle and play occurs
def collisions(player, obstacles):
    if obstacles:
        for obst_rect in obstacles:
            if player.colliderect(obst_rect):
                return False
    return True

# player animation; determine which image to draw to surface
def player_animation():
    global player_surface, player_index

    # display jump surface when player is in the air
    if player_rect.bottom < 300:
        player_surface = player_jump
    # play walking animation if the player is on the floor    
    else:
        # increasing the index by small increments extends how many frames an index position is displayed for
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


# initialize pygame
pygame.init()

# setup display surface
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
# rename screen title
pygame.display.set_caption('Runner')

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

player = pygame.sprite.GroupSingle()
player.add(Player())


# create a surface with an image
sky_surface = pygame.image.load('img/Sky.png').convert()

# create a ground surface with an image
ground_surface = pygame.image.load('img/ground.png').convert()

# obstacles
# animating snail
snail_frame_1 = pygame.image.load("img/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("img/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

# animating fly
fly_frame_1 = pygame.image.load("img/fly/fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("img/fly/fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

# create player character(surface)
# animating the player
player_walk_1 = pygame.image.load("img/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("img/player/player_walk_2.png").convert_alpha()
# list containing the two walk animation pics controlled by player_index
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("img/player/jump.png").convert_alpha()
# sets the default player image to player_walk_1
player_surface = player_walk[player_index]
# create player rectangle that is same size as player_surface
player_pos_x = 80
player_pos_y = 300
player_rect = player_surface.get_rect(midbottom = (player_pos_x, player_pos_y))
# create gravity physics for player
player_gravity = 0
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

# controls obstacle animation
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


# game loop
while True:
    # event loop
    for event in pygame.event.get():
        # if user clicks the window close button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:      
            # keystrikes   
            # make player jump using space bar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -27
            # make player jump if player is clicked (1:43:15)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            # timers
            # enemy/obstacle deployment timer 
            if event.type == obstacle_timer:
                # build random obstacle type generator; randint 0/1, if 1 snail, if 0 fly
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900, 1100), 210)))
            # obstacle animaton timers
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]
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
        ground_pos_x = 0
        ground_pos_y = 300
        screen.blit(ground_surface, (ground_pos_x, ground_pos_y))

        # store score and display
        score = display_score()

        # obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # apply player gravity physics
        player_gravity +=1 
        player_rect.y += player_gravity
        # create floor as barrier
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        # run player_animation to determine which image to show
        player_animation()
        # display player
        screen.blit(player_surface, player_rect)
        player.draw(screen)
        player.update()



        # collisions
        game_active = collisions(player_rect, obstacle_rect_list)
    else:
        # clear all existing enemies
        obstacle_rect_list.clear()
        # return player_rect to start position
        player_rect.midbottom = (80, 300)
        player_gravity = 0
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

    pygame.display.update()
    # sets so that while True loop should not run faster than framerate_ceiling times per second
    framerate_ceiling = 60
    clock.tick(framerate_ceiling)












