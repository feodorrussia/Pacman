import os
import sys
import pygame
from random import choice as rand

pygame.init()

FPS = 16
step_p = 10
step_g = 5
score = 0
pound_score = 15
level_n = 0
Width = 770
Height = 890
d_w = 40
d_h = 40

screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def randomase(vectors):
    vectors1 = []
    for i in range(4):
        vectors1.append(rand(vectors))
    vectors = vectors1


def cor_pos(self, vector):
    if vector == 0:
        if level[self.y][self.x + 1] != '/':
            return True
        else:
            return False
    if vector == 90:
        if level[self.y - 1][self.x] != '/':
            return True
        else:
            return False
    if vector == 180:
        if level[self.y][self.x - 1] != '/':
            return True
        else:
            return False
    if vector == 270:
        if level[self.y + 1][self.x] != '/':
            return True
        else:
            return False


def time():
    global ticks, secund, minute
    ticks += 1
    if ticks == FPS:
        secund += 1
        ticks = 0
    if secund == 60:
        minute += 1
        secund = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = 17

    return list(map(lambda x: x.ljust(max_width, ' '), level_map))


screen_sprite = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("pac-man_screen_n.png")
sprite.rect = sprite.image.get_rect()
sprite.rect.topleft = (40, 120)
screen_sprite.add(sprite)
wall_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
goosts_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(tiles_group, all_sprites)
        self.type = tile_type
        if tile_type == 'pound':
            image = pygame.Surface((40, 40), pygame.SRCALPHA, 32)
            r = 4
            pygame.draw.circle(image, pygame.Color("yellow"), (4, 4), 4)
            self.rect = pygame.Rect(x, y, 10, 10)
            self.rect.x = d_w * x + 20 - r
            self.rect.y = d_h * y + 20 - r
        if tile_type == 'energizer':
            image = pygame.Surface((40, 40), pygame.SRCALPHA, 32)
            r = 9
            pygame.draw.circle(image, pygame.Color("white"), (9, 9), 9)
            self.rect = pygame.Rect(x, y, 20, 20)
            self.rect.x = d_w * x + 20 - r
            self.rect.y = d_h * y + 20 - r
        self.image = image


class Blinky(pygame.sprite.Sprite):
    def __init__(self, ticks):
        super().__init__(goosts_group)
        self.image = load_image('Blinky.png')
        self.rect = pygame.Rect(0, 0, 38, 38)
        self.vector = 180
        self.vectors = list(range(2, -3, -1))
        self.ticks = ticks
        self.x = 9
        self.y = 9
        self.fl = True
        self.rect.x = d_w * self.x + 1
        self.rect.y = d_h * self.y + 1

    def update(self):
        if self.vector == 180:
            self.rect.x -= step_g
        if self.vector == 0:
            self.rect.x += step_g
        if self.vector == 90:
            self.rect.y -= step_g
        if self.vector == 270:
            self.rect.y += step_g

    def uppdate_pos(self):
        if self.vector == 0:
            if level[self.y][self.rect.x // d_w + 1] == 'P':
                self.x = 1
            else:
                self.x = self.rect.x // d_w
            if level[self.y][self.rect.x // d_w + 1] == '/':
                self.fl = False
        elif self.vector == 90:
            self.y = self.rect.y // d_w
            if level[self.rect.y // d_w - 1][self.x] == '/':
                self.fl = False
        elif self.vector == 180:
            if level[self.y][self.rect.x // d_w - 1] == 'P':
                self.x = 17
            else:
                self.x = self.rect.x // d_w
            if level[self.y][self.rect.x // d_w - 1] == '/':
                self.fl = False
        elif self.vector == 270:
            self.y = self.rect.y // d_w
            if level[self.rect.y // d_w + 1][self.x] == '/':
                self.fl = False
        self.rect.topleft = (self.x * d_w + 1, self.y * d_h + 1)

    def uppdate_vector(self, vector1=None):
        if self.vector == 90 or self.vector == 270:
            if self.fl:
                vector = rand([0, self.vector, 180])
                while not cor_pos(self, vector):
                    vector = rand([0, self.vector, 180])
                self.vector = vector
            else:
                vector = rand([0, 180])
                while not cor_pos(self, vector):
                    vector = rand([0, 180])
                self.vector = vector
                self.fl = True
        elif self.vector == 0 or self.vector == 180:
            if self.fl:
                vector = rand([90, 270, self.vector])
                while not cor_pos(self, vector):
                    vector = rand([90, self.vector, 270])
                self.vector = vector
            else:
                vector = rand([90, 270])
                while not cor_pos(self, vector):
                    vector = rand([90, 270])
                self.vector = vector
                self.fl = True


class Pinky(pygame.sprite.Sprite):
    def __init__(self, ticks, start_score=0):
        super().__init__(goosts_group)
        self.image = load_image('Pinky.png')
        self.rect = pygame.Rect(9, 11, 38, 38)
        self.vector = 180
        self.run = False
        self.vectors = list(range(2, -3, -1))
        self.ticks = ticks
        self.start_score = start_score
        self.x = 8
        self.y = 11
        self.fl = True
        self.rect.x = d_w * self.x + 1
        self.rect.y = d_h * self.y + 1

    def update(self):
        if self.vector == 180:
            self.rect.x -= step_g
        if self.vector == 0:
            self.rect.x += step_g
        if self.vector == 90:
            self.rect.y -= step_g
        if self.vector == 270:
            self.rect.y += step_g

    def uppdate_pos(self):
        if self.vector == 0:
            if level[self.y][self.rect.x // d_w + 1] == 'P':
                self.x = 1
            else:
                self.x = self.rect.x // d_w
            if level[self.y][self.rect.x // d_w + 1] == '/':
                self.fl = False
        elif self.vector == 90:
            self.y = self.rect.y // d_w
            if level[self.rect.y // d_w - 1][self.x] == '/':
                self.fl = False
        elif self.vector == 180:
            if level[self.y][self.rect.x // d_w - 1] == 'P':
                self.x = 17
            else:
                self.x = self.rect.x // d_w
            if level[self.y][self.rect.x // d_w - 1] == '/':
                self.fl = False
        elif self.vector == 270:
            self.y = self.rect.y // d_w
            if level[self.rect.y // d_w + 1][self.x] == '/':
                self.fl = False
        self.rect.topleft = (self.x * d_w + 1, self.y * d_h + 1)

    def uppdate_vector(self):
        if score - self.start_score < 5 * pound_score and not self.run:
            if not self.fl:
                self.vector = (180 + self.vector) % 360
                self.fl = True
        if score - self.start_score >= 5 * pound_score and not self.run:
            self.y = 9
            self.rect.y = 9 * d_h + 1
            self.run = True
        if self.run:
            if self.vector == 90 or self.vector == 270:
                if self.fl:
                    vector = rand([0, 180, self.vector])
                    while not cor_pos(self, vector):
                        vector = rand([0, self.vector, 180])
                    self.vector = vector
                else:
                    vector = rand([0, 180])
                    while not cor_pos(self, vector):
                        vector = rand([0, 180])
                    self.vector = vector
                    self.fl = True
            elif self.vector == 0 or self.vector == 180:
                if self.fl:
                    vector = rand([90, 270, self.vector])
                    while not cor_pos(self, vector):
                        vector = rand([90, self.vector, 270])
                    self.vector = vector
                else:
                    vector = rand([90, 270])
                    while not cor_pos(self, vector):
                        vector = rand([90, 270])
                    self.vector = vector
                    self.fl = True


class Inky(pygame.sprite.Sprite):
    def __init__(self, ticks, start_score=0):
        super().__init__(goosts_group)
        self.image = load_image('Inky.png')
        self.rect = pygame.Rect(9, 11, 38, 38)
        self.vector = 0
        self.run = False
        self.vectors = list(range(2, -3, -1))
        self.ticks = ticks
        self.start_score = start_score
        self.x = 10
        self.y = 11
        self.fl = True
        self.rect.x = d_w * self.x + 1
        self.rect.y = d_h * self.y + 1

    def update(self):
        if self.vector == 180:
            self.rect.x -= step_g
        if self.vector == 0:
            self.rect.x += step_g
        if self.vector == 90:
            self.rect.y -= step_g
        if self.vector == 270:
            self.rect.y += step_g

    def uppdate_pos(self):
        if self.vector == 0:
            if level[self.y][self.rect.x // d_w + 1] == 'P':
                self.x = 1
            else:
                self.x = self.rect.x // d_w
            if level[self.y][self.rect.x // d_w + 1] == '/':
                self.fl = False
        elif self.vector == 90:
            self.y = self.rect.y // d_w
            if level[self.rect.y // d_w - 1][self.x] == '/':
                self.fl = False
        elif self.vector == 180:
            if level[self.y][self.rect.x // d_w - 1] == 'P':
                self.x = 17
            else:
                self.x = self.rect.x // d_w
            if level[self.y][self.rect.x // d_w - 1] == '/':
                self.fl = False
        elif self.vector == 270:
            self.y = self.rect.y // d_w
            if level[self.rect.y // d_w + 1][self.x] == '/':
                self.fl = False
        self.rect.topleft = (self.x * d_w + 1, self.y * d_h + 1)

    def uppdate_vector(self):
        if score - self.start_score < 10 * pound_score and not self.run:
            if not self.fl:
                self.vector = (180 + self.vector) % 360
                self.fl = True
        if score - self.start_score >= 10 * pound_score and not self.run:
            self.y = 9
            self.rect.y = 9 * d_h + 1
            self.run = True
        if self.run:
            if self.vector == 90 or self.vector == 270:
                if self.fl:
                    vector = rand([0, 180, self.vector])
                    while not cor_pos(self, vector):
                        vector = rand([0, self.vector, 180])
                    self.vector = vector
                else:
                    vector = rand([0, 180])
                    while not cor_pos(self, vector):
                        vector = rand([0, 180])
                    self.vector = vector
                    self.fl = True
            elif self.vector == 0 or self.vector == 180:
                if self.fl:
                    vector = rand([90, 270, self.vector])
                    while not cor_pos(self, vector):
                        vector = rand([90, self.vector, 270])
                    self.vector = vector
                else:
                    vector = rand([90, 270])
                    while not cor_pos(self, vector):
                        vector = rand([90, 270])
                    self.vector = vector
                    self.fl = True


class Clyde(pygame.sprite.Sprite):
    def __init__(self, ticks, start_score=0):
        super().__init__(goosts_group)
        self.image = load_image('Clyde.png')
        self.rect = pygame.Rect(9, 11, 38, 38)
        self.vector = 180
        self.run = False
        self.vectors = list(range(2, -3, -1))
        self.ticks = ticks
        self.start_score = start_score
        self.x = 9
        self.y = 11
        self.fl = True
        self.rect.x = d_w * self.x + 1
        self.rect.y = d_h * self.y + 1

    def update(self):
        if self.vector == 180:
            self.rect.x -= step_g
        if self.vector == 0:
            self.rect.x += step_g
        if self.vector == 90:
            self.rect.y -= step_g
        if self.vector == 270:
            self.rect.y += step_g

    def uppdate_pos(self):
        if self.vector == 0:
            if level[self.y][self.rect.x // d_w + 1] == 'P':
                self.x = 1
            else:
                self.x = self.rect.x // d_w
            if level[self.y][self.rect.x // d_w + 1] == '/':
                self.fl = False
        elif self.vector == 90:
            self.y = self.rect.y // d_w
            if level[self.rect.y // d_w - 1][self.x] == '/':
                self.fl = False
        elif self.vector == 180:
            if level[self.y][self.rect.x // d_w - 1] == 'P':
                self.x = 17
            else:
                self.x = self.rect.x // d_w
            if level[self.y][self.rect.x // d_w - 1] == '/':
                self.fl = False
        elif self.vector == 270:
            self.y = self.rect.y // d_w
            if level[self.rect.y // d_w + 1][self.x] == '/':
                self.fl = False
        self.rect.topleft = (self.x * d_w + 1, self.y * d_h + 1)

    def uppdate_vector(self):
        if score - self.start_score < 15 * pound_score and not self.run:
            if not self.fl:
                self.vector = (180 + self.vector) % 360
                self.fl = True
        if score - self.start_score >= 15 * pound_score and not self.run:
            self.y = 9
            self.rect.y = 9 * d_h + 1
            self.run = True
        if self.run:
            if self.vector == 90 or self.vector == 270:
                if self.fl:
                    vector = rand([0, 180, self.vector])
                    while not cor_pos(self, vector):
                        vector = rand([0, self.vector, 180])
                    self.vector = vector
                else:
                    vector = rand([0, 180])
                    while not cor_pos(self, vector):
                        vector = rand([0, 180])
                    self.vector = vector
                    self.fl = True
            elif self.vector == 0 or self.vector == 180:
                if self.fl:
                    vector = rand([90, 270, self.vector])
                    while not cor_pos(self, vector):
                        vector = rand([90, self.vector, 270])
                    self.vector = vector
                else:
                    vector = rand([90, 270])
                    while not cor_pos(self, vector):
                        vector = rand([90, 270])
                    self.vector = vector
                    self.fl = True


class Player(pygame.sprite.Sprite):
    def __init__(self, x=9, y=17):
        super().__init__(player_group)
        self.image = load_image('pac-man1.png')
        self.rect = pygame.Rect(x, y, 38, 38)
        self.vector = 180
        self.vector1 = self.vector
        self.ticks = 0
        self.k = 1
        self.x = x
        self.y = y
        self.fl = True
        self.rect.x = d_w * x + 1
        self.rect.y = d_h * y + 1

    def update(self):
        if self.vector == 180:
            self.rect.x -= step_p
        if self.vector == 0:
            self.rect.x += step_p
        if self.vector == 90:
            self.rect.y -= step_p
        if self.vector == 270:
            self.rect.y += step_p
        if pygame.sprite.spritecollideany(self, all_sprites):
            food = pygame.sprite.spritecollide(self, tiles_group, True)
            for i in food:
                if i.type == 'pound':
                    global score
                    score += pound_score
                elif i.type == 'energizer':
                    global mode
                    score += pound_score * 5
                    mode = ['rush', 'scare', 10 * FPS]
        if mode[0] == 'rush' and pygame.sprite.spritecollideany(self, goosts_group):
            die_goost = pygame.sprite.spritecollide(self, goosts_group, True)
            for i in die_goost:
                score += self.k * 200
                self.k += 1

    def uppdate_pos(self):
        if self.vector == 0:
            if level[self.y][self.rect.x // d_w + 1] == 'P':
                self.x = 1
            else:
                self.x = self.rect.x // d_w
            if level[self.y][self.rect.x // d_w + 1] == '/':
                self.fl = False
        elif self.vector == 90:
            self.y = self.rect.y // d_w
            if level[self.rect.y // d_w - 1][self.x] == '/':
                self.fl = False
        elif self.vector == 180:
            if level[self.y][self.rect.x // d_w - 1] == 'P':
                self.x = 17
            else:
                self.x = self.rect.x // d_w
            if level[self.y][self.rect.x // d_w - 1] == '/':
                self.fl = False
        elif self.vector == 270:
            self.y = self.rect.y // d_w
            if level[self.rect.y // d_w + 1][self.x] == '/':
                self.fl = False
        self.rect.topleft = (self.x * d_w + 1, self.y * d_h + 1)

    def uppdate_vector(self, vector1=None):
        fl = False
        if vector1 == None:
            fl = True
            vector1 = self.vector1
        self.vector1 = vector1
        if self.vector1 != self.vector and (fl or not self.fl):
            if self.vector1 == 0 and level[self.y][self.x + 1] != '/':
                self.fl = True
                self.ticks = ticks
                self.vector = self.vector1
            elif self.vector1 == 90 and level[self.y - 1][self.x] != '/':
                self.fl = True
                self.ticks = ticks
                self.vector = self.vector1
            elif self.vector1 == 180 and level[self.y][self.x - 1] != '/':
                self.fl = True
                self.ticks = ticks
                self.vector = self.vector1
            elif self.vector1 == 270 and level[self.y + 1][self.x] != '/':
                self.fl = True
                self.ticks = ticks
                self.vector = self.vector1


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('pound', x, y)
            if level[y][x] == 'e':
                Tile('energizer', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    return new_player, x, y


lives = ['pac-man2.png', 'pac-man2.png', 'pac-man2.png']
mode = ['stabil', 'go']
ticks = 0
secund = 0
minute = 0
wait = 0
level = load_level('test_level.txt')
running = True
running_bonus = False
pygame.display.flip()
all_sprites.draw(screen)
deith = False
while running:
    player, width, height = generate_level(level)
    blinky = Blinky(ticks)
    pinky = Pinky(ticks, score)
    inky = Inky(ticks, score)
    clyde = Clyde(ticks, score)
    running_level = True
    kill_event = False
    if wait != 0:
        clock.tick(FPS)
        wait -= 1
        continue
    if deith:
        running_level = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    else:
        level_n += 1
    if level_n == 4:
        f3 = pygame.font.SysFont('serif', 80)
        text3 = f3.render("You win!!!", 0, (255, 0, 0))
        screen.blit(text3, (200, 450))
        f4 = pygame.font.SysFont('serif', 50)
        text4 = f4.render("Your score: " + str(score), 0, (255, 255, 0))
        screen.blit(text4, (250, 540))
        pygame.display.flip()
        running_level = False
        wait = 3 * FPS
        running_bonus = True
    if level_n == 2:
        step_g = 10
    if level_n == 3:
        step_p = 5
    while running_level:
        if wait != 0:
            clock.tick(FPS)
            wait -= 1
            continue
        if len(lives) > 1 and kill_event:
            kill_event = False
            player_group = pygame.sprite.Group()
            goosts_group = pygame.sprite.Group()
            blinky = Blinky(ticks)
            pinky = Pinky(ticks, score)
            inky = Inky(ticks, score)
            clyde = Clyde(ticks, score)
            player = Player()
            del lives[-1]
            wait = 2 * FPS
            continue
        elif len(lives) == 1 and kill_event:
            f3 = pygame.font.SysFont('serif', 80)
            text3 = f3.render("Game over", 0, (255, 0, 0))
            screen.blit(text3, (200, 450))
            f4 = pygame.font.SysFont('serif', 50)
            text4 = f4.render("Your score: " + str(score), 0, (255, 255, 0))
            screen.blit(text4, (250, 540))
            pygame.display.flip()
            deith = True
            break
        if len(tiles_group) == 0:
            wait = 2 * FPS
            player.k = 1
            mode = ['stabil', 'go']
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                running_level = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.uppdate_vector(180)
                if event.key == pygame.K_RIGHT:
                    player.uppdate_vector(0)
                if event.key == pygame.K_UP:
                    player.uppdate_vector(90)
                if event.key == pygame.K_DOWN:
                    player.uppdate_vector(270)
        if (ticks + secund * FPS + minute * 60 * FPS) % (40 // step_p) == player.ticks % (
                40 // step_p):
            player.uppdate_pos()
            player.uppdate_vector()
            player.uppdate_pos()
        if (ticks + secund * FPS + minute * 60 * FPS) % (40 // step_g) == blinky.ticks % (
                40 // step_g):
            blinky.uppdate_pos()
            blinky.uppdate_vector()
            blinky.uppdate_pos()
        if (ticks + secund * FPS + minute * 60 * FPS) % (40 // step_g) == pinky.ticks % (
                40 // step_g):
            pinky.uppdate_pos()
            pinky.uppdate_vector()
            pinky.uppdate_pos()
        if (ticks + secund * FPS + minute * 60 * FPS) % (40 // step_g) == inky.ticks % (
                40 // step_g):
            inky.uppdate_pos()
            inky.uppdate_vector()
            inky.uppdate_pos()
        if (ticks + secund * FPS + minute * 60 * FPS) % (40 // step_g) == clyde.ticks % (
                40 // step_g):
            clyde.uppdate_pos()
            clyde.uppdate_vector()
            clyde.uppdate_pos()
        if ticks % 4 <= 1:
            player.image = load_image('pac-man1.png')
        elif ticks % 4 > 1:
            player.image = load_image('pac-man2.png')
        if player.vector != 180:
            player.image = pygame.transform.rotate(player.image, player.vector)
        else:
            player.image = pygame.transform.flip(player.image, True, False)
        screen.fill((0, 0, 0))
        screen_sprite.draw(screen)
        all_sprites.draw(screen)
        if player.fl:
            player.update()
        if mode[0] == 'rush' and mode[2] == 0:
            mode = ['stabil', 'go']
            player.k = 1
        if mode[1] == 'scare':
            mode[2] -= 1
            f0 = pygame.font.SysFont(None, 20)
            text0 = f0.render(str(mode[2] // FPS), 0, (255, 0, 0))
            screen.blit(text0, (740, 50))
            blinky.image = load_image('rush1.png')
            pinky.image = load_image('rush1.png')
            inky.image = load_image('rush1.png')
            clyde.image = load_image('rush1.png')
        if mode[0] == 'rush':
            step_p = 10
        if mode[0] == 'stabil' and level_n == 3:
            step_p = 5
        if mode[1] == 'go':
            blinky.image = load_image('Blinky.png')
            pinky.image = load_image('Pinky.png')
            inky.image = load_image('Inky.png')
            clyde.image = load_image('Clyde.png')
        if blinky.fl:
            blinky.update()
        if pinky.fl:
            pinky.update()
        if inky.fl:
            inky.update()
        if clyde.fl:
            clyde.update()
        if mode[0] == 'stabil' and pygame.sprite.spritecollideany(player, goosts_group):
            kill_event = True
            mode = ['stabil', 'go']
        player_group.draw(screen)
        goosts_group.draw(screen)

        f1 = pygame.font.SysFont('serif', 30)
        text1 = f1.render("Score: " + str(score), 0, (255, 255, 0))
        screen.blit(text1, (50, 20))

        f2 = pygame.font.SysFont('serif', 75)
        text2 = f2.render("LEVEL " + str(level_n), 0, (255, 255, 0))
        screen.blit(text2, (250, 30))

        lives_group = pygame.sprite.Group()
        for x in range(len(lives)):
            sprite = pygame.sprite.Sprite()
            sprite.image = load_image(lives[x])
            sprite.rect = sprite.image.get_rect()
            sprite.rect.topleft = (600 + x * 40, 20)
            lives_group.add(sprite)

        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.Surface((40, 5), pygame.SRCALPHA, 32)
        pygame.draw.rect(sprite.image, pygame.Color("blue"), (0, 0, 40, 5))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.topleft = (600 + x * 40, 60)
        lives_group.add(sprite)

        lives_group.draw(screen)

        time()
        clock.tick(FPS)
        pygame.display.flip()

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    goosts_group = pygame.sprite.Group()
    clock.tick(FPS)
while running_bonus:
    all_sprites.draw(screen)
    player, width, height = generate_level(level)
    blinky = Blinky(ticks)
    pinky = Pinky(ticks, score)
    inky = Inky(ticks, score)
    clyde = Clyde(ticks, score)
    running_level = True
    kill_event = False
    if wait != 0:
        clock.tick(FPS)
        wait -= 1
        continue
    if deith:
        running_level = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_bonus = False
    elif len(tiles_group) == 0:
        f3 = pygame.font.SysFont('serif', 80)
        text3 = f3.render("You're the best!!!", 0, (255, 0, 0))
        screen.blit(text3, (120, 450))
        f4 = pygame.font.SysFont('serif', 50)
        text4 = f4.render("Your score: " + str(score), 0, (255, 255, 0))
        screen.blit(text4, (250, 540))
        pygame.display.flip()
        running_level = False
    step_p = 5
    step_g = 10
    while running_level:
        if wait != 0:
            clock.tick(FPS)
            wait -= 1
            continue
        if len(lives) > 1 and kill_event:
            kill_event = False
            player_group = pygame.sprite.Group()
            goosts_group = pygame.sprite.Group()
            blinky = Blinky(ticks)
            pinky = Pinky(ticks, score)
            inky = Inky(ticks, score)
            clyde = Clyde(ticks, score)
            player = Player()
            del lives[-1]
            wait = 2 * FPS
            continue
        elif len(lives) == 1 and kill_event:
            f3 = pygame.font.SysFont('serif', 80)
            text3 = f3.render("Game over", 0, (255, 0, 0))
            screen.blit(text3, (200, 450))
            f4 = pygame.font.SysFont('serif', 50)
            text4 = f4.render("Your score: " + str(score), 0, (255, 255, 0))
            screen.blit(text4, (250, 540))
            pygame.display.flip()
            deith = True
            break
        if len(tiles_group) == 0:
            wait = 2 * FPS
            player.k = 1
            mode = ['stabil', 'go']
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_bonus = False
                running_level = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.uppdate_vector(180)
                if event.key == pygame.K_RIGHT:
                    player.uppdate_vector(0)
                if event.key == pygame.K_UP:
                    player.uppdate_vector(90)
                if event.key == pygame.K_DOWN:
                    player.uppdate_vector(270)
        if (ticks + secund * FPS + minute * 60 * FPS) % (40 // step_p) == player.ticks % (
                40 // step_p):
            player.uppdate_pos()
            player.uppdate_vector()
            player.uppdate_pos()
        if (ticks + secund * FPS + minute * 60 * FPS) % (40 // step_g) == blinky.ticks % (
                40 // step_g):
            blinky.uppdate_pos()
            blinky.uppdate_vector()
            blinky.uppdate_pos()
        if (ticks + secund * FPS + minute * 60 * FPS) % (40 // step_g) == pinky.ticks % (
                40 // step_g):
            pinky.uppdate_pos()
            pinky.uppdate_vector()
            pinky.uppdate_pos()
        if (ticks + secund * FPS + minute * 60 * FPS) % (40 // step_g) == inky.ticks % (
                40 // step_g):
            inky.uppdate_pos()
            inky.uppdate_vector()
            inky.uppdate_pos()
        if (ticks + secund * FPS + minute * 60 * FPS) % (40 // step_g) == clyde.ticks % (
                40 // step_g):
            clyde.uppdate_pos()
            clyde.uppdate_vector()
            clyde.uppdate_pos()
        if ticks % 4 <= 1:
            player.image = load_image('pac-man1.png')
        elif ticks % 4 > 1:
            player.image = load_image('pac-man2.png')
        if player.vector != 180:
            player.image = pygame.transform.rotate(player.image, player.vector)
        else:
            player.image = pygame.transform.flip(player.image, True, False)
        screen.fill((0, 0, 0))
        screen_sprite.draw(screen)
        all_sprites.draw(screen)
        if player.fl:
            player.update()
        if blinky.fl:
            blinky.update()
        if pinky.fl:
            pinky.update()
        if inky.fl:
            inky.update()
        if clyde.fl:
            clyde.update()
        if pygame.sprite.spritecollideany(player, goosts_group):
            kill_event = True
        player_group.draw(screen)
        goosts_group.draw(screen)

        f1 = pygame.font.SysFont('serif', 30)
        text1 = f1.render("Score: " + str(score), 0, (255, 255, 0))
        screen.blit(text1, (50, 20))

        f2 = pygame.font.SysFont('serif', 60)
        text2 = f2.render("BONUS LEVEL", 0, (255, 0, 0))
        screen.blit(text2, (185, 50))

        lives_group = pygame.sprite.Group()
        for x in range(len(lives)):
            sprite = pygame.sprite.Sprite()
            sprite.image = load_image(lives[x])
            sprite.rect = sprite.image.get_rect()
            sprite.rect.topleft = (600 + x * 40, 20)
            lives_group.add(sprite)

        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.Surface((40, 5), pygame.SRCALPHA, 32)
        pygame.draw.rect(sprite.image, pygame.Color("blue"), (0, 0, 40, 5))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.topleft = (600 + x * 40, 60)
        lives_group.add(sprite)

        lives_group.draw(screen)

        time()
        clock.tick(FPS)
        pygame.display.flip()

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    goosts_group = pygame.sprite.Group()
    clock.tick(FPS)
