import pygame


pygame.font.init()

you_lost_font   = pygame.font.Font("assets/fonts/JANSINA.ttf", 60)
points_font     = pygame.font.Font("assets/fonts/JANSINA.ttf", 35)
main_title_font = pygame.font.Font("assets/fonts/JANSINA.ttf", 80)
press_key_font  = pygame.font.Font("assets/fonts/JANSINA.ttf", 30)

vegetable_images = ["assets/images/lettuce.png",
                    "assets/images/potato.png",
                    "assets/images/carrot.png",
                    "assets/images/garlic.png",
                    "assets/images/cucumber.png",
                    "assets/images/pumpkin.png",
                    "assets/images/corn.png",
                    "assets/images/cauliflower.png",
                    "assets/images/onion.png",
                    "assets/images/radish.png"]

object_images = ["assets/images/bomb.png",
                "assets/images/stone.png"]