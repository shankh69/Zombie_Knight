import random

import pygame
vector = pygame.math.Vector2


class Zombie(pygame.sprite.Sprite):
    def __init__(self, platform_group, portal_group, min_speed, max_speed):
        super().__init__()
        # set constant variables
        self.platform_group = platform_group
        self.portal_group = portal_group

        self.GRAVITY = 0.8
        self.rise_time = 0

        self.walk_right = [None]*20
        self.walk_left = []

        self.die_right = [None]*20
        self.die_left = []

        self.rise_right = []
        self.rise_left = []

        self.gen_choice = ['boy', 'girl']
        self.gender = random.choice(self.gen_choice)

        for i in range(1, 11):
            self.walk_right[i - 1] = (pygame.transform.scale(pygame.image.load
                                                             (f"zombie_knight_assets/images/zombie/{self.gender}/walk/Walk ({i}).png"),
                                                             (64, 64)))
            self.walk_right[i + 9] = pygame.transform.smoothscale(pygame.image.load
                                                                  (f"zombie_knight_assets/images/zombie/{self.gender}/walk/Walk ({i}).png"),
                                                                  (64, 64))

        for image in self.walk_right:
            self.walk_left.append(pygame.transform.flip(image, True, False))

        for i in range(1, 11):
            self.die_right[i - 1] = (pygame.transform.scale(pygame.image.load
                                                             (f"zombie_knight_assets/images/zombie/{self.gender}/dead/Dead ({i}).png"),
                                                             (64, 64)))
            self.die_right[i + 9] = pygame.transform.smoothscale(pygame.image.load
                                                                  (f"zombie_knight_assets/images/zombie/{self.gender}/dead/Dead ({i}).png"),
                                                                  (64, 64))

        for image in self.die_right:
            self.die_left.append(pygame.transform.flip(image, True, False))

        self.rise_right = self.die_right[9::-1] + self.die_right[:9:-1]
        self.rise_left = self.die_left[9::-1] + self.die_left[:9:-1]

        self.frame_count = 0
        self.direction = random.choice([1, -1])

        if self.direction == 1:
            self.image = self.walk_right[10]
            self.mask_image = self.walk_right[0]
        if self.direction == -1:
            self.image = self.walk_left[10]
            self.mask_image = self.walk_left[0]
        self.mask = pygame.mask.from_surface(self.mask_image)


        self.rect = self.image.get_rect()

        self.rect.midbottom = (random.randint(100, 1200), -100)


        # set sprite groups:
        self.platform_group = platform_group
        self.portal_group = portal_group

        # animation booleans
        self.die_bool = False
        self.rise_bool = False

        # load sounds
        self.hit_sound = pygame.mixer.Sound('zombie_knight_assets/sounds/zombie_hit.wav')
        self.kick_sound = pygame.mixer.Sound('zombie_knight_assets/sounds/zombie_kick.wav')
        self.portal_sound = pygame.mixer.Sound('zombie_knight_assets/sounds/portal_sound.wav')
        self.portal_sound.set_volume(0.1)


        self.position = vector(self.rect.centerx, self.rect.bottom)
        self.velocity = vector(self.direction*random.randint(min_speed, max_speed), 0)
        self.acceleration = vector(0, self.GRAVITY)


        self.is_dead = False
        self.round_time = 0


    def update(self):
        self.move()
        self.check_animation()
        self.check_collision()

        if self.is_dead:
            self.rise_time += 1
            if self.rise_time > 300:
                self.rise_time = 0
                self.rise_bool = True
                self.frame_count = 0



    def move(self):
        if not self.is_dead:
            self.velocity += self.acceleration
            self.position += self.velocity + self.acceleration/2

            if self.velocity.x < 0:
                self.animate(self.walk_left, 0.5)
            else:
                self.animate(self.walk_right, 0.5)

            if self.rect.right < 10:
                self.position.x = 1280
            if self.rect.left > 1270:
                self.position.x = 0

            self.rect.midbottom = self.position

    def check_collision(self):

        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            if self.rect.bottom - 20 <= collided_platforms[0].rect.top:
                self.position.y = collided_platforms[0].rect.top + 1
                self.velocity.y = 0

        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            if self.position.x < 600:
                self.position.x = 1188
            else:
                self.position.x = 92
            if self.position.y < 350:
                self.position.y = 18 * 32 + 97
            else:
                self.position.y = 97

    def check_animation(self):
        if self.die_bool:
            if self.velocity.x > 0:
                self.animate(self.die_right, 0.1)
            elif self.velocity.x < 0:
                self.animate(self.die_left, 0.1)

        if self.rise_bool:
            if self.velocity.x > 0:
                self.animate(self.rise_right, 0.1)
            elif self.velocity.x < 0:
                self.animate(self.rise_left, 0.1)

    def animate(self, frame_list, speed):
        if self.frame_count < len(frame_list) / 2 - 1:
            self.frame_count += speed

        else:
            self.frame_count = 0

            if self.die_bool:
                self.die_bool = False
                self.frame_count = 9
                self.position.y += 5
                self.rect.midbottom = self.position
            if self.rise_bool:
                self.rise_bool = False
                self.velocity.x *= -1
                self.frame_count = 9
                self.is_dead = False

        self.image = frame_list[int(self.frame_count) + 10]

    