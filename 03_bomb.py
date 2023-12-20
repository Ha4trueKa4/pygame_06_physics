import os
import random
import pygame

size = width, height = 500, 500
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
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


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb2.png")
    image_boom = load_image("boom.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        # ищем свободное место до тех пор, пока не найдем
        while True:
            self.rect.topleft = (
                (random.randint(0, width - self.rect.width), random.randint(0, height - self.rect.height)))
            if len(pygame.sprite.spritecollide(self, all_sprites, False)) == 1:
                break

    def process_event(self, event):
        # если спрайт содержит точку с координатами event.pos, взрываемся
        raise NotImplementedError()


# группа, содержащая все спрайты
all_sprites = pygame.sprite.Group()


# ... инициализируем 10 бомбочек ...


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bomb in all_sprites:
                bomb.get_event(event)
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()