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


def sort():
    file = open('nicknames.txt').read().strip().split('\n')
    st = ''
    for z, k in sorted([(int(s.split()[1]), s.split()[0]) for s in file if len(s.split()) == 2], reverse=True):
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

class Moving_object(pygame.sprite.Sprite):
    def __init__(self, sprite_group, photo, x, y):
        super().__init__(sprite_group)
        self.image = load_image(photo, "data/1/")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        

pygame.init()
clock = pygame.time.Clock()
size = 770, 890
screen = pygame.display.set_mode(size)
sprite_button = pygame.sprite.Group()
sprite_logotipe = pygame.sprite.Group()
sprite_animation = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()

sprite_heroes = pygame.sprite.Group()
player = Moving_object(sprite_heroes, 'pac-man1.png', -10+300, 720)
Blinky = Moving_object(sprite_heroes, 'Blinky.png', -60+300, 720)
Pinky = Moving_object(sprite_heroes, 'Pinky.png', -110+300, 720)
Clyde = Moving_object(sprite_heroes, 'Clyde.png', -160+300, 720)
Inky = Moving_object(sprite_heroes, 'Inky.png', -210+300, 720)

sprite.image = load_image("logo3.jpg", 'анимация')
sprite.rect = sprite.image.get_rect()
sprite.rect.topleft = ((Width - 500) // 2, 20)
sprite_logotipe.add(sprite)
start = Start_Button()
accout = Personal_account()
running = True
app = QApplication(sys.argv)
def_win = Input_nick()
ticks = 0
sprite_heroes.draw(screen)
direction = True
while running:
    
    if direction:
        player.update(1, 0)
        Blinky.update(1, 0)
        Pinky.update(1, 0)
        Clyde.update(1, 0)
        Inky.update(1, 0)

        if player.rect.x > 410:
            direction = False
        
    else:
        player.update(-1, 0)
        Blinky.update(-1, 0)
        Pinky.update(-1, 0)
        Clyde.update(-1, 0)
        Inky.update(-1, 0)
    
        if player.rect.x < 210:
            direction = True
    
        
    
    sprite_heroes.draw(screen)
    pygame.display.flip()
    
    if ticks % 4 <= 1:
        player.image = load_image('pac-man1.png', "data/1/")
    elif ticks % 4 > 1:
        player.image = load_image('pac-man2.png', "data/1/")
        
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
            else:
                pygame.quit()
                os.system('python {}'.format('Game.py'))
                running = False
        if event.type == pygame.KEYDOWN:
            pygame.quit()
            os.system('python {}'.format('Game.py'))
            running = False
    ticks += 1
    if ticks == FPS:
        ticks = 0
pygame.quit()
