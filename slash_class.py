import pygame


class Slash(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("zombie_knight_assets/images/player/"
                                                                 "slash.png"), (32, 32)), True, False)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y-5)
        self.VElOCITY = -15
        if direction > 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.VElOCITY = 15


    def update(self):
        if self.rect.left > self.x + 480 or self.x - 480 > self.rect.left:
            self.kill()

        self.rect.x += self.VElOCITY
