import os
import pygame
import random
from input_box import InputBox

NICKNAMES_PATH = "nicknames.txt"



class StartWindow:
    def __init__(self):
        self.state = False

    def start(self):
        self.state = True
        pygame.init()
        clock = pygame.time.Clock()
        size = width, height = 500, 500
        screen = pygame.display.set_mode(size)
        running = True
        all_sprites = pygame.sprite.Group()
        pygame.display.flip()
        screen.fill((255, 255, 255))
        nickname_input = InputBox(300, 20, 180, 50, text="set_nickname", text_limit=10,
                                  action="nickname_adding")
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                nickname_input.handle_event(event)
            screen.fill((30, 30, 30))
            nickname_input.draw(screen)

            pygame.display.flip()
            clock.tick(30)
        pygame.quit()

    def stop(self):
        self.state = False


start_window = StartWindow()
start_window.start()
