from random import randint
from pygame.locals import *

from config import *
from assets import *

import random
import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, game_lost_callback):
        super().__init__()
        self.is_vegetable = random.choice([True, True, True, False])
        self.image = self.random_image()
        self.rect = self.image.get_rect()
        self.rect.center = (randint(IMAGE_SIZE, SCREEN_WIDTH - IMAGE_SIZE), SCREEN_HEIGHT)
        self.velocity_y = randint(-29, -22)
        self.velocity_x = self.get_velocity_x()
        self.game_lost_callback = game_lost_callback

    def random_image(self):
        if self.is_vegetable:
            random_img = random.choice(vegetable_images)
        else:
            random_img = random.choice(object_images)

        return pygame.transform.rotate(pygame.transform.scale(pygame.image.load(random_img), (IMAGE_SIZE, IMAGE_SIZE)), float(randint(0, 360)))

    def update(self):
        self.velocity_y += GRAVITY

        if self.velocity_x > 0:
            self.velocity_x -= HORIZONTAL_FORCE
        else:
            self.velocity_x += HORIZONTAL_FORCE

        self.rect.y = self.rect.y + self.velocity_y
        self.rect.x = self.rect.x + self.velocity_x

        if self.rect.bottom > SCREEN_HEIGHT + IMAGE_SIZE:
            if self.is_vegetable:
                if self.rect.left + IMAGE_SIZE >= 0 and self.rect.right - IMAGE_SIZE < SCREEN_WIDTH:
                    self.game_lost_callback(True)
                else:
                    self.reset()
            else:
                self.reset()

    def get_velocity_x(self):
        if self.rect.x < SCREEN_WIDTH // 2:
            vel_x = randint(1, 3)
        else:
            vel_x = randint(-3, -1)
        return vel_x

    def reset(self):
        self.velocity_y = randint(-29, -22)
        self.velocity_x = self.get_velocity_x()
        self.rect.center = (
            randint(IMAGE_SIZE, SCREEN_WIDTH - IMAGE_SIZE), SCREEN_HEIGHT)
        self.is_vegetable = random.choice([True, True, True, False])
        self.image = self.random_image()

    def destroy(self):
        if not self.is_vegetable:
            self.game_lost_callback(True)
        self.reset()

    def redraw(self, surface):
        surface.blit(self.image, self.rect)

    def has_been_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
