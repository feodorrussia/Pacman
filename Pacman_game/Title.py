import os
import sys
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import *
import pygame

FPS = 16
Width = 770
Height = 890


def load_image(name, catal, color_key=None):
    fullname = os.path.join(catal, name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

class Input_nick(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(800, 470, 5, 5)
        self.setWindowTitle('def')
    def input(self):
        i, okBtnPressed = QInputDialog.getText(self,
                                               "Введите Ваш nickname",
                                               "Nickname:")
        if okBtnPressed:
            open('nicknames.txt', 'a').write(i + '\n')
        self.close()

class Start_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(sprite_button)
        self.image = load_image("start.jpg", 'кнопки')
        self.rect = self.image.get_rect()
        self.rect.x = (Width - 200) // 2
        self.rect.y = 2 * Height // 5


class Personal_account(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(sprite_button)
        self.image = load_image("личный кабинет.png", 'кнопки')
        self.rect = self.image.get_rect()
        self.rect.x = Width - 90
        self.rect.y = 160


pygame.init()
clock = pygame.time.Clock()
size = 770, 890
screen = pygame.display.set_mode(size)
sprite_button = pygame.sprite.Group()
sprite_logotipe = pygame.sprite.Group()
sprite_animation = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("logo3.jpg", 'анимация')
sprite.rect = sprite.image.get_rect()
sprite.rect.topleft = ((Width - 500) // 2, 20)
sprite_logotipe.add(sprite)
start = Start_Button()
accout = Personal_account()
running = True
app = QApplication(sys.argv)
def_win= Input_nick()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if Width - 90 < event.pos[0] < Width - 56 and 160 < event.pos[1] < 225:
                def_win.show()
                def_win.input()
                sys.exit(app.exec_())
            else:
                os.system('python {}'.format('Game.py'))
    sprite_logotipe.draw(screen)
    sprite_button.draw(screen)
    sprite_animation.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
