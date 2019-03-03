import os
import sys
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import *
import pygame

FPS = 30
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


def sort():
    file = open('nicknames.txt').read().strip().split('\n')
    st = ''
    for z, k in sorted([(int(s.split()[1]), s.split()[0]) for s in file if len(s.split()) == 2],
                       reverse=True):
        st += k + ' ' + str(z) + '\n'
    open('nicknames_top.txt', 'w').write(st)


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
            open('nicknames.txt', 'a').write(i)
        self.close()


class Help_win:
    def show(self):
        os.system('start {}'.format('C:/Users/VV/Documents/Pacman/Pacman_game/help.txt'))


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


class Help(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(sprite_button)
        self.image = load_image("Справка.png", 'кнопки')
        self.rect = self.image.get_rect()
        self.rect.x = Width - 90
        self.rect.y = 240


class Animation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(sprite_button)
        self.image = load_image("animation 009.jpg", "data/animation")
        self.rect = self.image.get_rect()
        self.rect.x = 25
        self.rect.y = 500


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
animation = Animation()
help = Help()
running = True
app = QApplication(sys.argv)
def_win = Input_nick()
def_win2 = Help_win()
temp = -1
while running:
    temp = (temp + 1) % 870 + 1
    animation.image = load_image("animation " + "0" * (3 - len(str(temp))) + str(temp) + ".jpg",
                                 "data/animation")
    sort()
    top = open('nicknames_top.txt').read().strip('\n').split('\n')
    if len(top) < 3:
        for i in range(3 - len(top)):
            top.append(' ')
    if len(top) > 3:
        top = top[:3]
    f1 = pygame.font.SysFont('serif', 50)
    text1 = f1.render('1. ' + top[0], 0, (255, 0, 0))
    screen.blit(text1, (150, 180))
    sprite_logotipe.draw(screen)
    f2 = pygame.font.SysFont(None, 30)
    text2 = f2.render('2. ' + top[1], 0, (0, 0, 255))
    screen.blit(text2, (250, 250))
    sprite_logotipe.draw(screen)
    f3 = pygame.font.SysFont(None, 30)
    text3 = f3.render('3. ' + top[2], 0, (0, 0, 255))
    screen.blit(text3, (250, 300))
    sprite_logotipe.draw(screen)
    sprite_button.draw(screen)
    sprite_animation.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if Width - 90 < event.pos[0] < Width - 56 and 160 < event.pos[1] < 225:
                def_win.show()
                def_win.input()
            if Width - 90 < event.pos[0] < Width - 50 and 240 < event.pos[1] < 280:
                def_win2.show()
            else:
                pygame.quit()
                os.system('python {}'.format('Game.py'))
                running = False
        if event.type == pygame.KEYDOWN:
            pygame.quit()
            os.system('python {}'.format('Game.py'))
            running = False
pygame.quit()
