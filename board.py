import pygame

class Board:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.board = [[0] * width for _ in range(height)]
        # [[0] * 5] * 8 - НЕЛЬЗЯ

        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.h):
            for j in range(self.w):
                Rect = ((j * self.cell_size + self.left, i * self.cell_size + self.top), 
                        (self.cell_size, self.cell_size))
                if self.board[i][j]:
                    pygame.draw.rect(screen, (255, 255, 255), Rect)
                pygame.draw.rect(screen, (255, 255, 255), Rect, 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        if mouse_pos[0] < self.left or mouse_pos[0] > self.left + self.cell_size * len(self.board[0]) or mouse_pos[1] \
            < self.top or mouse_pos[1] > self.top + self.cell_size * len(self.board):
            return None
        return (
            (mouse_pos[0] - self.left) // self.cell_size,
            (mouse_pos[1] - self.left) // self.cell_size
            )
        
    def on_click(self, cell):
        if not cell:
            return
        self.board[cell[1]][cell[0]] ^= 1