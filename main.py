import random
import pygame
from random import randint
from pygame.locals import *
import math


# Constantes
FPS = 60
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
IMAGE_SIZE = 75
GRAVITY = 0.5
NUMBER_OF_VEGETABLES = 3


# Inicializar jogo e configurar
pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
bg = pygame.transform.scale(pygame.image.load("assets/images/background_image.jpg").convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Veggie Ninja")

game_lost = False
points = 0

# Carregar fontes
you_lost_font = pygame.font.Font("assets/fonts/JANSINA.ttf", 60)
points_font = pygame.font.Font("assets/fonts/JANSINA.ttf", 35)
main_title_font = pygame.font.Font("assets/fonts/JANSINA.ttf", 80)
press_key_font = pygame.font.Font("assets/fonts/JANSINA.ttf", 30)


class Vegetable(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = self.random_image()
        self.rect = self.image.get_rect()
        self.rect.center = (randint(IMAGE_SIZE, SCREEN_WIDTH - IMAGE_SIZE), SCREEN_HEIGHT)
        self.velocity = randint(-29, -22)

    def random_image(self):
        images = ["assets/images/lettuce.png",
                  "assets/images/potato.png",
                  "assets/images/carrot.png",
                  "assets/images/garlic.png",
                  "assets/images/cucumber.png",
                  "assets/images/pumpkin.png",
                  "assets/images/corn.png",
                  "assets/images/cauliflower.png",
                  "assets/images/onion.png",
                  "assets/images/radish.png"]
        random_img = random.choice(images)
        return pygame.transform.rotate(pygame.transform.scale(pygame.image.load(random_img), (IMAGE_SIZE, IMAGE_SIZE)), float(randint(0, 360)))

    def update(self):
        global game_lost
        self.velocity += GRAVITY
        self.rect.y = self.rect.y + self.velocity

        if self.rect.bottom > SCREEN_HEIGHT + IMAGE_SIZE:
            game_lost = True

    def destroy(self):
        self.velocity = randint(-29, -22)
        self.rect.center = (randint(IMAGE_SIZE, SCREEN_WIDTH - IMAGE_SIZE), SCREEN_HEIGHT)
        self.image = self.random_image()

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
    global points
    global game_lost

    points = 0
    game_lost = False  

    def draw_screen(pts):
        screen.blit(bg, (0, 0))

        points = points_font.render(f"Points: {pts}", True, (255, 255, 255))
        screen.blit(points, (10, 10))

        for veggie in vegetable_array:
            veggie.redraw(screen)

    is_game_running = True
    is_holding_mouse_down = False
    vegetable_array = [Vegetable() for i in range(NUMBER_OF_VEGETABLES)]

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
            for veggie in vegetable_array:
                if veggie.has_been_clicked(mouse_pos):
                    veggie.destroy()
                    points += 1

        for veggie in vegetable_array:
            veggie.update()

        draw_screen(points)

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

    if game_lost:
        menu_screen(True, points)
    else:
        # Não quero fechar o jogo, quero ir para a tela inicial, por isso nao faço pygame.quit()
        menu_screen(False)


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


menu_screen(False)
