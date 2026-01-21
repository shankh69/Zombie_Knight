import pygame.font

from Ruby_maker import Ruby
from zombie_class import Zombie

import config



class Game:
    def __init__(self, display_surface, player, zombie_group, slash_group, ruby_group, platform_group, portal_group):
        # set constant variables
        self.STARTING_ROUND_TIME = 60
        self.display_surface = display_surface
        self.ZOMBIE_SPAWN_TIME = 5

        # set game values
        self.score = 0
        self.round = 1
        self.frame_counter = 0
        self.round_time = self.STARTING_ROUND_TIME
        self.zombie_spawn_time = self.ZOMBIE_SPAWN_TIME

        # load font
        self.title_font = pygame.font.Font("zombie_knight_assets/fonts/Poultrygeist.ttf", 48)
        self.font = pygame.font.Font("zombie_knight_assets/fonts/Pixel.ttf", 24)

        # loading sprites
        self.player = player
        self.zombie_group = zombie_group
        self.slash_group = slash_group
        self.ruby_group = ruby_group
        self.platform_group = platform_group
        self.portal_group = portal_group

        self.deduct_player_health = False
        self.damage_countdown = 0

        #load sounds
        self.ruby_pickup_sound = pygame.mixer.Sound("zombie_knight_assets/sounds/ruby_pickup.wav")
        self.ruby_miss_sound = pygame.mixer.Sound("zombie_knight_assets/sounds/lost_ruby.wav")
        self.ruby_miss_sound.set_volume(0.2)

        pygame.mixer.music.load("zombie_knight_assets/sounds/level_music.wav")
        pygame.mixer.music.play(-1, 0.0)

    def update(self):
        self.frame_counter += 1
        if self.frame_counter == 60:
            self.frame_counter = 0
            self.round_time -= 1

        if self.damage_countdown > 0:
            self.damage_countdown -= 1

        self.draw()
        self.check_collision()
        self.add_zombie()
        self.check_round_completed()
        self.check_game_over()

    def draw(self):
        # set colors
        WHITE = (255, 255, 255)
        GREEN = (25, 200, 25)

        # set text
        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, 674)

        health_text = self.font.render("Health: " + str(self.player.health), True, WHITE)
        health_rect = health_text.get_rect()
        health_rect.topleft = (10, 699)

        title_text = self.title_font.render("Zombie Knight", True, GREEN)
        title_rect = title_text.get_rect()
        title_rect.center = (640, 699)

        round_text = self.font.render("Night: " + str(self.round), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topright = (1270, 674)

        round_time_text = self.font.render("Night ends in: " + str(self.round_time), True, WHITE)
        round_time_rect = round_time_text.get_rect()
        round_time_rect.topright = (1270, 699)

        # blit the hud
        self.display_surface.blit(score_text, score_rect)
        self.display_surface.blit(health_text, health_rect)
        self.display_surface.blit(title_text, title_rect)
        self.display_surface.blit(round_text, round_rect)
        self.display_surface.blit(round_time_text, round_time_rect)

    def add_zombie(self):
        if self.STARTING_ROUND_TIME == self.round_time and self.frame_counter == 1:
            self.zombie_group.add(Zombie(self.platform_group, self.portal_group, self.round, self.round + 4))
        if (self.STARTING_ROUND_TIME -self.round_time) % int(self.zombie_spawn_time) == 0:
            if self.zombie_spawn_time%1 == 50*self.frame_counter/3:
                self.zombie_group.add(Zombie(self.platform_group, self.portal_group, self.round, self.round + 4))

    def check_collision(self):
        zombie_slash = pygame.sprite.groupcollide(self.slash_group, self.zombie_group, False, False)
        if zombie_slash:
            for zombies in zombie_slash.values():
                for zombie in zombies:
                    if not zombie.is_dead:
                        zombie.hit_sound.play()
                        zombie.is_dead = True
                        zombie.die_bool = True
                        zombie.frame_count = 0
                        pygame.sprite.spritecollide(zombie, self.slash_group, True)
                        self.score += 1

        zombie_player = pygame.sprite.spritecollide(self.player, self.zombie_group, False, pygame.sprite.collide_mask)
        if zombie_player:
            for zombie in zombie_player:
                if zombie.is_dead:
                    if self.player.velocity.y >= 1:
                        self.score += self.round*10
                        zombie.kick_sound.play()
                        zombie.kill()
                        self.ruby_group.add(Ruby(self.ruby_group, self.platform_group, self.portal_group))

                else:
                    if self.player.animate_slash:
                        zombie.hit_sound.play()
                        zombie.is_dead = True
                        zombie.die_bool = True
                        zombie.frame_count = 0
                        self.score += 2
                        self.player.single_fire = False
                    else:
                        self.deduct_player_health = True

            if self.deduct_player_health and self.damage_countdown ==0:
                self.damage_countdown = 60
                self.player.health -= self.round*10
                self.deduct_player_health = False
                self.player.hit_sound.play()

        ruby_player = pygame.sprite.spritecollide(self.player, self.ruby_group, True)
        if ruby_player:
            self.ruby_pickup_sound.play()
            self.score += self.round*20
            if self.player.health < 100:
                self.player.health += 10
            if self.player.health > 100:
                self.player.health = 100

        for zombie in self.zombie_group:
            if not zombie.is_dead:
                if pygame.sprite.spritecollide(zombie, self.ruby_group, True):
                    self.ruby_miss_sound.play()
                    self.zombie_group.add(Zombie(self.platform_group, self.portal_group, self.round, self.round + 4))

    def check_round_completed(self):
        if self.round_time == 0:
            self.pause_game("you passed the night", "press enter to continue")
            self.start_new_round()

    def check_game_over(self):
        if self.player.health <= 0:
            self.pause_game("gameover! final score: " + str(self.score), 'press enter to restart')
            self.reset_game()

    def start_new_round(self):
        self.round += 1
        self.round_time = self.STARTING_ROUND_TIME
        self.frame_counter = 0
        self.zombie_group.empty()
        self.slash_group.empty()
        self.ruby_group.empty()
        self.player.reset()

    def pause_game(self, main_text, sub_text):
        main_text = self.title_font.render(main_text, True, (25, 200, 25))
        main_rect = main_text.get_rect()
        main_rect.center = (640, 368)

        sub_text = self.title_font.render(sub_text, True, (200, 200, 200))
        sub_rect = sub_text.get_rect()
        sub_rect.center = (640, 430)

        control_text = self.font.render("Press A and D to move, space to jump, left mouse to attack and escape to pause", True, (200, 200, 200))
        control_rect = control_text.get_rect()
        control_rect.midtop = (640, 10)

        tip_text = self.font.render("Stomp on zombies before they regenerate!", True, (200, 200, 200))
        tip_rect = tip_text.get_rect()
        tip_rect.midbottom = (640, 692)

        tip2_text = self.font.render("Collect rubies before them or face the consequences", True, (200, 200, 200))
        tip2_rect = tip2_text.get_rect()
        tip2_rect.midbottom = (640, 726)

        self.display_surface.fill((0, 0, 0))
        self.display_surface.blit(main_text, main_rect)
        self.display_surface.blit(sub_text, sub_rect)
        self.display_surface.blit(tip_text, tip_rect)
        self.display_surface.blit(control_text, control_rect)
        self.display_surface.blit(tip2_text, tip2_rect)

        pygame.display.update()
        pygame.mixer.music.stop()
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    config.game_over()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        paused = False
                        pygame.mixer.music.play(-1, 0.0)

    def reset_game(self):
        self.round = 1
        self.round_time = self.STARTING_ROUND_TIME
        self.frame_counter = 0
        self.zombie_group.empty()
        self.slash_group.empty()
        self.ruby_group.empty()
        self.player.reset()
        self.player.health = 100
        self.score = 0
