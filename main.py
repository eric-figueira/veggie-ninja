from random import randint
from pygame.locals import *

from config import *
from assets import *

import math
import random
import pygame

# Inicializar jogo e configurar
pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
bg = pygame.transform.scale(pygame.image.load("assets/images/background_image.jpg").convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Veggie Ninja")


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
                self.game_lost_callback(True)
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
        self.rect.center = (randint(IMAGE_SIZE, SCREEN_WIDTH - IMAGE_SIZE), SCREEN_HEIGHT)
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


def sine_wave(speed, time, how_far, overallY):
    t = pygame.time.get_ticks() / 2 % time
    x = t
    y = math.sin(t / speed) * how_far + overallY
    y = int(y)
    return y


def game_screen():

    points = 0
    game_lost = False  

    def draw_screen(pts):
        screen.blit(bg, (0, 0))

        points = points_font.render(f"Points: {pts}", True, (255, 255, 255))
        screen.blit(points, (10, 10))

        for entity in entities_sprite_groups:
            entity.redraw(screen)
    
    def game_lost_callback(set_lost):
        nonlocal game_lost
        game_lost = set_lost

    is_game_running = True
    is_holding_mouse_down = False
    entities_sprite_groups = pygame.sprite.Group()

    for _ in range(NUMBER_OF_VEGETABLES):
        entities_sprite_groups.add(Entity(game_lost_callback))

    while is_game_running and not game_lost:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                is_holding_mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                is_holding_mouse_down = False

        if is_holding_mouse_down:
            mouse_pos = pygame.mouse.get_pos()
            for entity in entities_sprite_groups:
                if entity.has_been_clicked(mouse_pos):
                    entity.destroy()
                    points += 1

        entities_sprite_groups.update()

        draw_screen(points)

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

    menu_screen(game_lost, points)


def redraw_menu_screen(has_lost_message, points):
    screen.blit(bg, (0, 0))

    if has_lost_message:
        lost_message = you_lost_font.render("You LOST", True, (230, 0, 0))
        points_msg = points_font.render(f"You destroyed {points} veggies!", True, (255, 255, 255))

        screen.blit(lost_message, (SCREEN_WIDTH / 2 - lost_message.get_width() / 2, 50))
        screen.blit(points_msg, (SCREEN_WIDTH / 2 - points_msg.get_width() / 2, 115))

    y = sine_wave(200.0, 1280, 10.0, 450)

    title = main_title_font.render("Veggie NINJA", True, (87, 230, 48))
    # 120px above "Press key to start"
    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, y - 120))

    press_key = press_key_font.render("Press any key to start", True, (255, 255, 255))
    screen.blit(press_key, (SCREEN_WIDTH / 2 - press_key.get_width() / 2, y))


def menu_screen(show_lost_message, points=0):
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                run = False

        redraw_menu_screen(show_lost_message, points)

    game_screen()


if __name__ == "__main__":
    menu_screen(False)
