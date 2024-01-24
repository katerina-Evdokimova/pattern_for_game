from typing import Any
import pygame
import os, sys

def load_image(name, colorkey=None):
    """функция для загрузки изображения,ю а также удаления фона у спрайтов

    Args:
        name (_type_): название картинки
        colorkey (_type_, optional): флаг для удаления фона, если -1 то удаляем. Defaults to None.
    """
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f'Файла не существует: {fullname}')
        sys.exit()
    
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    return image

class Sprites(pygame.sprite.Sprite):
    """Класс родитель. Здесь прописываются основные функции для анимации и базовых движений

    Args:
        pygame (_type_): _description_
    """
    def __init__(self, *group):
        super().__init__(*group)
        self.rect = None
        self.pos = None
        self.frames = []


    def cut_frames(self, img, columns, rows):
        self.rect = pygame.Rect(0, 0, img.get_width() // columns, img.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(
                    img.subsurface(pygame.Rect(frame_location, self.rect.size))
                )
    
    def move(self, x, y):
        # перемещение спрайта в заданные координаты
        x_c, y_c = self.image.get_size()
        self.rect = self.image.get_rect(center=(x_c // 2, y_c // 2)).move(x, y)
        self.pos = x, y


class TestSprite(Sprites):
    """Данный класс спрайта обладает следующими свойствами:
            1. Есть анимация +
            2. Умеет передвигаться по полю, благодаря нажатию на клавиши WASD +
            3. При нажатии на него "умирает", те полностью исчезает с поля +
    """

    image = load_image('image_sprite.png')
    # количество изображение в картинке спрайта:
    columns = 4
    rows = 4

    def __init__(self, x: int, y: int, size_sprite: int, *groups) -> None:
        """создание спрайта
        В данном конструкторе спрайт получает размер и координаты размещения.

        Args:
            x (int): координата размещения
            y (int): координата размещения
            size_sprite (int): размер спрайта 
        """
        super().__init__(*groups)
        self.frames = []  # список в котором хранятся картинки спрайта

        # Выравнивание спрайта под общий размер игры:
        img = pygame.transform.scale(TestSprite.image, (size_sprite * TestSprite.columns, size_sprite * TestSprite.rows))  
        self.cut_frames(img, TestSprite.columns, TestSprite.rows)

        self.cur_frames = 0  # номер картинки для отображения
        self.image = self.frames[self.cur_frames]
        self.rect = self.rect.move(x, y)
        self.pos = x, y

        self.v = 30 # пискселей/сек. - скорость передвижения спрайта.

        # Флаги для проверки движения по той или иной кнопке
        self.dict_flags = {
            pygame.K_s: False,
            pygame.K_a: False,
            pygame.K_w: False,
            pygame.K_d: False
        }
        self.time_frame = pygame.time.get_ticks()

    def update(self, FPS, *args: Any) -> None:
        # В случае данного спрайта: если он стоит, то у него меняются толкьо первые 2 картинки:
        if not any(self.dict_flags.values()):

            # чтобы спрайт не трясся, как безумец будем изменять его картинки раз в 0.5 секунды
            if abs(self.time_frame - pygame.time.get_ticks()) > 500:
                self.cur_frames = (self.cur_frames + 1) % 2
                self.time_frame = pygame.time.get_ticks()
            self.image = self.frames[self.cur_frames]
        else:
            # есть какое-то движение
            if self.dict_flags[pygame.K_s]:
                self.move(self.pos[0], self.pos[1] + self.v // FPS)
                self.update_frames(0)
            if self.dict_flags[pygame.K_w]:
                self.move(self.pos[0], self.pos[1] - self.v // FPS)
                self.update_frames(1)
            if self.dict_flags[pygame.K_a]:
                self.move(self.pos[0]  - self.v // FPS, self.pos[1])
                self.update_frames(2)
            if self.dict_flags[pygame.K_d]:
                self.move(self.pos[0]  + self.v // FPS, self.pos[1])
                self.update_frames(3)

        # реализация шагов. Здесь продемонстрировано самая сложныя реализация. При этом вы ее можете упростить.
        '''
        Чтобы упростить написание кода можено делать движение просто по нажатию, те обрабатывать только pygame.KEYDOWN
        '''
        if args and args[0].type == pygame.KEYDOWN:
            key = args[0].key
            if key in self.dict_flags:
                self.dict_flags[key] = True

        if args and args[0].type == pygame.KEYUP:
            key = args[0].key
            if key in self.dict_flags:
                self.dict_flags[key] = False
        
        # при нажатии на персонажа он должен погибнуть:
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            pos = args[0].pos
            if self.rect.collidepoint(pos): # проверяем было ли попадение точки клика на персонаж или нет
                self.kill() # в случае попадения уничтожаем спрайт
        
               
    def update_frames(self, start=0):
        # так как каждая строка отвечаает за движение в разные стороны записываем такое выражение:
        if abs(self.time_frame - pygame.time.get_ticks()) > 100:
            self.cur_frames = start * TestSprite.rows + (self.cur_frames + 1) % TestSprite.columns
            self.time_frame = pygame.time.get_ticks()
        self.image = self.frames[self.cur_frames]