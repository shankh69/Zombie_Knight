import pygame, random


class Portal(pygame.sprite.Sprite):
    def __init__(self,x, y, color, portal_group):
        super().__init__()

        self.animation_frames = []
        for i in range(22):
            if i < 10:
                i = "0" + str(i)
            self.animation_frames.append(pygame.transform.scale(pygame.image.load
                                            (f"zombie_knight_assets/images/portals/{color}/tile0{i}.png"), (72, 72)))

        self.frame_count = random.randint(0, len(self.animation_frames)-1)
        self.image = self.animation_frames[self.frame_count]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        portal_group.add(self)


    def update(self):
        self.animate(0.1)

    def animate(self, speed):
        if self.frame_count < len(self.animation_frames) - 1:
            self.frame_count += speed
        else:
            self.frame_count = 0

        self.image = self.animation_frames[int(self.frame_count)]

portal_group = pygame.sprite.Group()

Portal(-12, 20, "purple", portal_group)
Portal(-12, 18*32 + 20, "green", portal_group)
Portal(1220, 20, "green", portal_group)
Portal(1220, 18*32 + 20, "purple", portal_group)