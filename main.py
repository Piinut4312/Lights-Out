from game import Game
import pygame
import numpy as np
from linear_algebra import solve

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (130, 130, 130)
DARK_GRAY_2 = (110, 110, 110)
GRAY = (170, 170, 170)
LIGHT_GRAY = (210, 210, 210)
YELLOW = (230, 190, 30)
YELLOW_2 = (210, 170, 10)

OUTLINE_COLORMAP = [DARK_GRAY_2, YELLOW_2]
INTERIOR_COLORMAP = [DARK_GRAY, YELLOW]

GAME_SHAPE = (9, 9)
SCREEN_SHAPE = (500, 700)
OUTLINE_SIZE = 5
BOARD_TOP = 240
BOARD_LEFT = 50
CELL_SIZE = (SCREEN_SHAPE[0]-2*BOARD_LEFT)//GAME_SHAPE[0]


def draw_text(surface: pygame.surface.Surface, content: str, font: pygame.font.Font, color, pos):
    text = font.render(content, True, color)
    text_rect = text.get_rect(center=pos)
    surface.blit(text, text_rect)


def main():

    game = Game(shape=GAME_SHAPE)
    game.randomize(game.n_cells//4)
    solution = solve(game.adj_matrix, np.expand_dims(game.board.flatten(), axis=1), 2).reshape(game.shape)
    print("Solution: \n", solution)
    
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SHAPE)
    pygame.display.set_caption("Lights Out")

    title_font = pygame.font.Font(pygame.font.get_default_font(), 64)
    text_font = pygame.font.Font(pygame.font.get_default_font(), 24)

    click_sound = pygame.mixer.Sound("click.mp3")

    running = True
    steps = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                col, row = event.pos
                col = (col-BOARD_LEFT)//CELL_SIZE
                row = (row-BOARD_TOP)//CELL_SIZE
                if game.in_range(row, col):
                    game.click_at(row, col)
                    pygame.mixer.Sound.play(click_sound)
                    steps += 1

        screen.fill(LIGHT_GRAY)
        draw_text(screen, "Lights Out!", title_font, BLACK, (SCREEN_SHAPE[0]//2, 50))
        draw_text(screen, "Steps used: {}".format(steps), text_font, BLACK, (SCREEN_SHAPE[0]//2, 150))
        draw_text(screen, "Remaining lights: {}".format(np.sum(game.board)), text_font, BLACK, (SCREEN_SHAPE[0]//2, 200))
        for i in range(game.shape[1]):
            for j in range(game.shape[0]):
                rect_left = BOARD_LEFT + CELL_SIZE*i
                rect_top = BOARD_TOP + CELL_SIZE*j
                pygame.draw.rect(
                    screen, 
                    OUTLINE_COLORMAP[game.board[j, i]], 
                    pygame.Rect(rect_left, rect_top, CELL_SIZE, CELL_SIZE)
                )
                pygame.draw.rect(
                    screen, 
                    INTERIOR_COLORMAP[game.board[j, i]], 
                    pygame.Rect(rect_left+OUTLINE_SIZE, rect_top+OUTLINE_SIZE, CELL_SIZE-2*OUTLINE_SIZE, CELL_SIZE-2*OUTLINE_SIZE)
                )
        pygame.display.update()
    

if __name__ == '__main__':
    main()