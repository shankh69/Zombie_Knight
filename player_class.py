import pygame
vector = pygame.math.Vector2
from slash_class import Slash

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, platform_group, portal_group, slash_group):
        super().__init__()
        # set constant variables
        self.HORIZONTAL_ACCELERATION = 2
        self.HORIZONTAL_FRICTION = 0.2
        self.GRAVITY = 0.8
        self.JUMP_SPEED = -18
        self.STARTING_HEALTH = 100
        self.STARTING_POSITION = vector(x, y)
        self.single_fire = True
        self.on_ground = False

        # animation frames

        self.move_right = [None]*20
        self.move_left = []

        self.idle_right = [None]*20
        self.idle_left = []

        self.jump_right = [None]*20
        self.jump_left = []

        self.slash_right = [None]*20
        self.slash_left = []

        for i in range(1, 11):
            self.move_right[i-1] = (pygame.transform.scale(pygame.image.load
                                            (f"zombie_knight_assets/images/player/run/Run ({i}).png"), (64, 64)))
            self.move_right[i + 9] = pygame.transform.smoothscale(pygame.image.load
                                            (f"zombie_knight_assets/images/player/run/Run ({i}).png"), (64, 64))

        for image in self.move_right:
            self.move_left.append(pygame.transform.flip(image, True, False))

        for i in range(1, 11):
            self.idle_right[i-1] = (pygame.transform.scale(pygame.image.load
                                            (f"zombie_knight_assets/images/player/idle/Idle ({i}).png"), (64, 64)))
            self.idle_right[i + 9] = pygame.transform.smoothscale(pygame.image.load
                                                                  (f"zombie_knight_assets/images/player/idle/Idle ({i}).png"),
                                                                  (64, 64))

        for image in self.idle_right:
            self.idle_left.append(pygame.transform.flip(image, True, False))

        for i in range(1, 11):
            self.jump_right[i-1] = (pygame.transform.scale(pygame.image.load
                                            (f"zombie_knight_assets/images/player/jump/Jump ({i}).png"), (64, 64)))
            self.jump_right[i + 9] = pygame.transform.smoothscale(pygame.image.load
                                                                  (f"zombie_knight_assets/images/player/jump/Jump ({i}).png"),
                                                                  (64, 64))

        for image in self.jump_right:
            self.jump_left.append(pygame.transform.flip(image, True, False))

        for i in range(1, 11):
            self.slash_right[i-1] = (pygame.transform.scale(pygame.image.load
                                        (f"zombie_knight_assets/images/player/attack/Attack ({i}).png"), (64, 64)))
            self.slash_right[i + 9] = pygame.transform.smoothscale(pygame.image.load
                                                                  (f"zombie_knight_assets/images/player/attack/Attack ({i}).png"),
                                                                  (64, 64))

        for image in self.slash_right:
            self.slash_left.append(pygame.transform.flip(image, True, False))

        self.mask_image = self.idle_right[0]
        self.image = self.idle_right[10]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

        self.mask = pygame.mask.from_surface(self.mask_image)

        self.frame_count = 0

        # attach sprite groups
        self.platform_group = platform_group
        self.portal_group = portal_group
        self.slash_group = slash_group

        # animate bools
        self.animate_jump = False
        self.animate_slash = False

        # load sounds
        self.jump_sound = pygame.mixer.Sound("zombie_knight_assets/sounds/jump_sound.wav")
        self.portal_sound = pygame.mixer.Sound("zombie_knight_assets/sounds/portal_sound.wav")
        self.slash_sound = pygame.mixer.Sound("zombie_knight_assets/sounds/slash_sound.wav")
        self.hit_sound = pygame.mixer.Sound("zombie_knight_assets/sounds/player_hit.wav")

        # kinematics vectors
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, self.GRAVITY)

        # set initial player values
        self.health = self.STARTING_HEALTH
        self.starting_rect = (x, y)

    def update(self):
        self.on_ground = False
        self.move()
        self.check_animation()
        self.check_collision()

    def move(self):
        # set acceleration vectors
        self.acceleration = vector(0, self.GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acceleration.x = -self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left, 0.5)
        elif keys[pygame.K_d]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right, 0.5)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right, 0.25)
            elif self.velocity.x <= 0:
                self.animate(self.idle_left, 0.25)

        # calculate velocity
        self.acceleration.x -= self.velocity.x*self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + self.acceleration/2

        # update rect and wrap around movement
        if self.rect.right < 10:
            self.position.x = 1280
        if self.rect.left > 1270:
            self.position.x = 0

        self.rect.midbottom = self.position

    def check_collision(self):
        if self.velocity.y > 0:
            hits = pygame.sprite.spritecollide(
                self, self.platform_group, False, pygame.sprite.collide_mask
            )

            for platform in hits:
                # move up until no overlap
                if self.position.y - 27 <= platform.rect.top:
                    self.velocity.y = 0
                    self.on_ground =True
                    while pygame.sprite.collide_mask(self, platform):
                        self.position.y -= 1
                        self.rect.midbottom = self.position

                    break
                else:
                    self.velocity.x = (self.velocity.x - int(self.velocity.x))/100



        if self.velocity.y < 0:
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False, pygame.sprite.collide_mask)

            if collided_platforms:
                self.position.y += 23
                self.velocity.y = 0


        # collision with portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            if self.position.x < 600:
                self.position.x = 1188
            else:
                self.position.x = 92
            if self.position.y < 350:
                self.position.y = 18*32 + 97
            else:
                self.position.y = 97


    def check_animation(self):
        if self.animate_jump:
            if self.velocity.y == 0:
                self.animate_jump = False
            if self.velocity.x > 0:
                self.animate(self.jump_right, 0.01)
            elif self.velocity.x < 0:
                self.animate(self.jump_left, 0.01)

        if self.animate_slash:
            if int(self.frame_count) == 6 and self.single_fire:
                self.slash_group.add(Slash(self.position.x, self.position.y, self.velocity.x))
                self.slash_sound.play()
                self.single_fire = False
            if self.velocity.x > 0:
                self.animate(self.slash_right, 0)
            else:
                self.animate(self.slash_left, 0)

    def jump(self):
        if self.on_ground:
            self.jump_sound.play()
            self.velocity.y = self.JUMP_SPEED
            self.animate_jump = True
            self.frame_count = 0

    def fire(self):
        if self.single_fire:
            self.animate_slash = True
            self.frame_count = 0

    def reset(self):
        self.position = self.STARTING_POSITION
        self.rect.midbottom = self.position
        self.velocity = vector(0, 0)
        self.image = self.idle_right[10]
        self.animate_jump = False
        self.animate_slash = False
        self.frame_count = 0
        self.acceleration.x = 0

    def animate(self, frame_list, speed):
        if self.frame_count < len(frame_list)/2 - 1:
            self.frame_count += speed

        else:
            self.frame_count = 0

            if self.animate_jump:
                self.animate_jump = False
            if self.animate_slash:
                self.animate_slash = False
                self.single_fire = True

        self.image = frame_list[int(self.frame_count) + 10]



