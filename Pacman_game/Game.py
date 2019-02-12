import os
import sys
import pygame

pygame.init()

FPS = 8
step = 10
score = 0
level_n = 0
Width = 770
Height = 890
d_w = 40
d_h = 40
print()

screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


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


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group)
        self.image = load_image('pac-man1.png')
        self.rect = pygame.Rect(x, y, 38, 38)
        self.vector = 180
        self.vector1 = self.vector
        self.ticks = 0
        self.x = x
        self.y = y
        self.fl = True
        self.rect.x = d_w * x + 1
        self.rect.y = d_h * y + 1

    def update(self):
        if self.vector == 180:
            self.rect.x -= step
        if self.vector == 0:
            self.rect.x += step
        if self.vector == 90:
            self.rect.y -= step
        if self.vector == 270:
            self.rect.y += step
        if pygame.sprite.spritecollideany(self, all_sprites):
            food = pygame.sprite.spritecollide(self, tiles_group, True)
            for i in food:
                if i.type == 'pound':
                    global score
                    score += 10
                elif i.type == 'energizer':
                    global mode
                    score += 50
                    mode = ['rush', 'scare']

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


lives = ['pac-man2.png', 'pac-man2.png', 'pac-man2.png', 'pac-man2.png']
mode = ['stabil', 'go']
ticks = 0
secund = 0
minute = 0
level = load_level('test_level.txt')
running = True
pygame.display.flip()
all_sprites.draw(screen)
while running:
    '''if len(lives) > 0 and kill_event:
        del lives[-1]
    else:
        f1 = pygame.font.SysFont('serif', 30)
        text1 = f1.render("Game over", 0, (255, 255, 0))
        screen.blit(text1, (300, 680))
        running_level = False'''
    player, width, height = generate_level(level)
    level_n += 1
    running_level = True
    while running_level:
        if len(tiles_group) == 0:
            running_level = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_level = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.uppdate_vector(180)
                if event.key == pygame.K_RIGHT:
                    player.uppdate_vector(0)
                if event.key == pygame.K_UP:
                    player.uppdate_vector(90)
                if event.key == pygame.K_DOWN:
                    player.uppdate_vector(270)
        if (ticks + secund * FPS + minute * 60 * FPS) % 4 == player.ticks % 4:
            player.uppdate_pos()
            player.uppdate_vector()
            player.uppdate_pos()
        if ticks % 2 == 0:
            player.image = load_image('pac-man1.png')
        elif ticks % 2 == 1:
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
        player_group.draw(screen)

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
        sprite.image=pygame.Surface((40, 5), pygame.SRCALPHA, 32)
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
