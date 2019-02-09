import os
import sys
import pygame

pygame.init()

FPS = 10
step = 5
score = 0
Width = 27 * 20
Height = 35 * 20

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

    max_width = 27

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_width = tile_height = 20
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(tiles_group, all_sprites)
        self.type = tile_type
        if tile_type == 'pound':
            image = pygame.Surface((40, 40), pygame.SRCALPHA, 32)
            pygame.draw.circle(image, pygame.Color("yellow"), (1, 1), 1)
            self.rect = pygame.Rect(x, y, 2, 2)
        if tile_type == 'energizer':
            image = pygame.Surface((40, 40), pygame.SRCALPHA, 32)
            pygame.draw.circle(image, pygame.Color("yellow"), (9, 9), 9)
            self.rect = pygame.Rect(x, y, 40, 40)
        self.image = image
        self.rect.x = tile_width * x
        self.rect.y = tile_height * y


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group)
        self.image = load_image('pac-man1.png')
        self.rect = pygame.Rect(x, y, 40, 40)
        self.vector = 0
        self.x=x
        self.y=y
        self.rect.x = tile_width * x
        self.rect.y = tile_height * y

    def update(self):
        if self.vector == 0:
            self.rect.x += step
        elif self.vector == 180:
            self.rect.x -= step
        elif self.vector == 90:
            self.rect.y -= step
        elif self.vector == 270:
            self.rect.y += step
        if pygame.sprite.spritecollideany(self, all_sprites):
            food = pygame.sprite.spritecollide(self, tiles_group, True)
            for i in food:
                if i.type == 'pound':
                    global score
                    score += 1
                elif i.type == 'energizer':
                    global mode
                    mode = ['rush', 'scare']


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '1':
                Tile('pound', x, y)
            elif level[y][x] == '2':
                Tile('energizer', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    return new_player, x + 1, y + 1


mode = ['stabil', 'go']
ticks = 0
secund = 0
minute = 0
level = load_level('test_level.txt')
running = True
pygame.display.flip()
all_sprites.draw(screen)
player, width, height = generate_level(level)
while running:
    running_level = True
    while running_level:
        if len(tiles_group) == 0:
            running_level = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if level[player.y][player.x - 1] != '/':
                        player.vector = 180
                if event.key == pygame.K_RIGHT:
                    if level[player.y][player.x + 1] != '/':
                        player.vector = 0
                if event.key == pygame.K_UP:
                    if level[player.y - 1][player.x] != '/':
                        player.vector = 90
                if event.key == pygame.K_DOWN:
                    if level[player.y + 1][player.x] != '/':
                        player.vector = 270
        if ticks % 2 == 0:
            player.image = load_image('pac-man1.png')
        elif ticks % 2 == 1:
            player.image = load_image('pac-man2.png')
        if player.vector!=180:
            player.image = pygame.transform.rotate(player.image, player.vector)
        else:
            player.image = pygame.transform.flip(player.image, True, False)
        screen.fill((0,0,0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        player.update()
        clock.tick(FPS)
        time()
        pygame.display.flip()
