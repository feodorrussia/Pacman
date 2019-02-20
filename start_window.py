import pygame

pygame.init()
NICKNAMES_PATH = "nicknames.txt"
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.SysFont('arial', 25)
start_window = 0
Width = 770
Height = 890


class Logo(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load("logo.png")
        self.rect = self.image.get_rect()
        self.rect.x = (Width - 449) // 2
        self.rect.y = 20


class Box:
    def __init__(self, x, y, w, h, text='', text_limit=2281488, action="2281488"):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.text_limit = text_limit
        self.action = action

    def update(self):
        self.check_text()
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        self.check_text()
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def check_text(self):
        if len(self.text) > self.text_limit:
            self.text = self.text[:self.text_limit]


class InputBox(Box):
    def handle_event(self, event):
        self.check_text()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.action == "nickname_adding":
                        self.nickname_adding()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def nickname_adding(self):
        open('nicknames.txt', 'a').write(self.text + '\n')


class ButtonBox(Box):
    def handle_event(self, event):
        self.check_text()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action == "start_game":
                    self.start_game()

    def start_game(self):
        start_window.running = False


class StartWindow:
    def __init__(self):
        self.state = False

    def start(self):
        self.state = True
        pygame.init()
        clock = pygame.time.Clock()
        size = 770, 890
        screen = pygame.display.set_mode(size)
        self.running = True
        all_sprites = pygame.sprite.Group()
        logo = Logo(all_sprites)
        pygame.display.flip()
        screen.fill((255, 255, 255))
        nickname_input = InputBox(Width - 150, 100, 140, 80, text="personal account",
                                  text_limit=10,
                                  action="nickname_adding")
        start_game = ButtonBox((Width - 360) // 2, 2 * Height // 5, 360, 100,
                               text="start game",
                               text_limit=10,
                               action="start_game")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                nickname_input.handle_event(event)
                start_game.handle_event(event)
            screen.fill((0, 0, 0))
            all_sprites.draw(screen)
            nickname_input.draw(screen)
            start_game.draw(screen)
            pygame.display.flip()
            clock.tick(30)
        pygame.quit()

    def stop(self):
        self.state = False


start_window = StartWindow()
start_window.start()
