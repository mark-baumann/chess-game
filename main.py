
import pygame
from constants import WIDTH, HEIGHT, FPS
from draw import  draw_board, draw_pieces


def run_game():
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('Two-Player Pygame Chess!')
    font = pygame.font.Font(None, 20)
    medium_font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(screen, font)
        draw_pieces(screen, font)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    run_game()