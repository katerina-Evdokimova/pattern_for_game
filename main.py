import pygame
import sys

import pygame_widgets # pip install pygame_widgets
from pygame_widgets.button import Button

def terminate():
    pygame.quit()
    sys.exit(0)

def game():
    # если хотите получить игру во весь пользовательский экран то необходимо выполнить следующие команды:
    infoObject = pygame.display.Info()
    w, h = infoObject.current_w, infoObject.current_h
    screen = pygame.display.set_mode((w, h))

    running = True    
    while running:
        screen.fill(pygame.Color('#4cbb17'))

        for event in pygame.event.get():
            # программа завершается, когда произошло нажатие на крестик
            if event.type == pygame.QUIT:
                running = False
                terminate()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()

    # размеры игрового экрана
    # size = w, h = 600, 600
    # screen = pygame.display.set_mode(size)

    # если хотите получить игру во весь пользовательский экран то необходимо выполнить следующие команды:
    infoObject = pygame.display.Info()
    w, h = infoObject.current_w, infoObject.current_h
    screen = pygame.display.set_mode((w, h))

    # задаем размеры основных кнопок (в процентах относительно экрана, в примере, 20% и 10%)
    w_button, h_button = 0.2 * w, 0.1 * h

    # Создание кнопки без изображения:
    button_exit = Button(
        # обязательные параметры
        screen,  # Surface
        (w - w_button) // 2,  # X-координата левого верхнего угла
        (h - h_button) // 2,  # Y-координата левого верхнего угла
        w_button,  # Width
        h_button,  # Height

        # Optional Parameters
        text='exit',  # текст на кнопке
        fontSize=50,  # размер шрифта
        margin=20,  # Минимальное расстояние между текстом/изображением и краем кнопки
        inactiveColour=(200, 50, 0),  # Цвет кнопки, когда с ней не взаимодействуют
        hoverColour=(150, 0, 0),  # Цвет кнопки при наведении курсора на нее
        pressedColour=(0, 200, 20),  # Цвет кнопки при нажатии
        radius=20,  # Радиус углов границы (оставьте пустым для не изогнутых)
        onClick=terminate # Функция, вызываемая при нажатии в этом случае закрытие игры
    )


    button_start_game = Button(
        # обязательные параметры
        screen,  # Surface
        (w - w_button) // 2,# X-координата левого верхнего угла
        h // 3, # Y-координата левого верхнего угла
        w_button,  # Width
        h_button,  # Height

        # Optional Parameters
        text='start',  # текст на кнопке
        fontSize=50,  # размер шрифта
        margin=20,  # Минимальное расстояние между текстом/изображением и краем кнопки
        inactiveColour=(200, 50, 0),  # Цвет кнопки, когда с ней не взаимодействуют
        hoverColour=(150, 0, 0),  # Цвет кнопки при наведении курсора на нее
        pressedColour=(0, 200, 20),  # Цвет кнопки при нажатии
        radius=20,  # Радиус углов границы (оставьте пустым для не изогнутых)
        onClick=game  # Функция, вызываемая при нажатии в этом случае открытие нового экрана
    )


    running = True    
    while running:
        screen.fill(pygame.Color('#ffcc00'))

        for event in pygame.event.get():
            # программа завершается, когда произошло нажатие на крестик
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos, y_pos = event.pos
        # button_exit.draw()
        # button_start_game.draw()
        pygame_widgets.update(pygame.event.get())
        pygame.display.flip()
    pygame.quit()