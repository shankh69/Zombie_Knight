import random

import pygame
vector = pygame.math.Vector2


class RubyMaker(pygame.sprite.Sprite):
    def __init__(self, tile_group):
        super().__init__()

        self.ruby_frames = []
        for i in range(7):
            self.ruby_frames.append(pygame.transform.scale(pygame.image.load
                                                (f"zombie_knight_assets/images/ruby/tile00{i}.png"), (64, 64)))

        self.image = self.ruby_frames[0]

        self.rect = self.image.get_rect()
        self.rect.midtop = (640, 10)

        self.frame_count = 0
        tile_group.add(self)

    def update(self):
        self.animate(0.25)

    def animate(self, speed):
        if self.frame_count < len(self.ruby_frames) - 1:
            self.frame_count += speed
        else:
            self.frame_count = 0

        self.image = self.ruby_frames[int(self.frame_count)]


class Ruby(pygame.sprite.Sprite):
    def __init__(self, tile_group, platform_group, portal_group):
        super().__init__()

        self.platform_group = platform_group
        self.portal_group = portal_group

        self.ruby_frames = []
        for i in range(7):
            self.ruby_frames.append(pygame.transform.scale(pygame.image.load
                                                           (f"zombie_knight_assets/images/ruby/tile00{i}.png"),
                                                           (64, 64)))

        self.image = self.ruby_frames[0]

        self.rect = self.image.get_rect()
        self.rect.midtop = (640, 10)

        self.frame_count = 0
        tile_group.add(self)

        # set kinematics
        self.position = vector(640, 10)
        self.velocity = vector((random.choice([1, -1])*3), 0)
        self.acceleration = vector(0, 0.8)

    def update(self):
        self.move()
        self.animate(0.25)
        self.check_collision()

    def check_collision(self):
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            if self.rect.bottom - 20 <= collided_platforms[0].rect.top:
                self.position.y = collided_platforms[0].rect.top + 1
                self.velocity.y = 0

        if pygame.sprite.spritecollide(self, self.portal_group, False):
            if self.position.x < 600:
                self.position.x = 1188
            else:
                self.position.x = 92
            if self.position.y < 350:
                self.position.y = 18 * 32 + 97
            else:
                self.position.y = 97

    def move(self):
        self.velocity += self.acceleration
        self.position += self.velocity + self.acceleration / 2

        if self.rect.right < 10:
            self.position.x = 1280
        if self.rect.left > 1270:
            self.position.x = 0

        self.rect.midbottom = self.position

    def animate(self, speed):
        if self.frame_count < len(self.ruby_frames) - 1:
            self.frame_count += speed
        else:
            self.frame_count = 0

        self.image = self.ruby_frames[int(self.frame_count)]
