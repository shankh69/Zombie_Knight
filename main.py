import pygame
import random

from player_class import Player
from zombie_class import Zombie

vector = pygame.math.Vector2

from tile_class import main_tile_group, platform_group
from Ruby_maker import RubyMaker, Ruby
from portal_class import portal_group
from game_class import Game

import config

pygame.init()

# setup display surface 40 * 23 tiles
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zombie Knight")

# set fps and clock
FPS = 60
clock = pygame.time.Clock()

# create sprite groups
player_group = pygame.sprite.Group()

slash_group = pygame.sprite.Group()

zombie_group = pygame.sprite.Group()

ruby_group = pygame.sprite.Group()


# create player object
my_player = Player(WINDOW_WIDTH//2, WINDOW_HEIGHT - 160, platform_group, portal_group, slash_group)
player_group.add(my_player)

# game class
game = Game(display_surface, my_player, zombie_group, slash_group, ruby_group, platform_group, portal_group)
game.pause_game("Zombie Knight", "press enter to begin")


# instructions

# load ruby maker
RubyMaker(main_tile_group)

# load background
background_image = pygame.image.load("zombie_knight_assets/images/background.png")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)
# game loop

while config.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            config.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()
            if event.key == pygame.K_ESCAPE:
                game.pause_game("Zombie Knight", "press enter to resume")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                my_player.fire()


    # blit the background
    display_surface.blit(background_image, background_rect)

    # blit the tiles
    main_tile_group.update()
    main_tile_group.draw(display_surface)

    # update player
    player_group.update()
    player_group.draw(display_surface)

    zombie_group.draw(display_surface)
    zombie_group.update()


    # update slashes
    slash_group.update()
    slash_group.draw(display_surface)

    # update ruby
    ruby_group.update()
    ruby_group.draw(display_surface)

    #update portal
    portal_group.update()
    portal_group.draw(display_surface)

    # update game
    game.update()


    # update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()