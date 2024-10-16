import pygame
import sys
from main import Main

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 255)

font = pygame.font.Font("font/DancingScript-VariableFont_wght.ttf", 40)
# nền menu
background = pygame.image.load("img/background.jpg") 
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
# nền mục hướng dẫn
instructions_bgr = pygame.image.load("img/instructions_bgr.jpg")
instructions_bgr = pygame.transform.scale(instructions_bgr, (SCREEN_WIDTH, SCREEN_HEIGHT))
# ảnh hướng dẫn
instructions_img = pygame.image.load("img/instructions.png")
instructions_img = pygame.transform.scale(instructions_img, (400, 300))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu():
    while True:
        screen.blit(background, (0, 0))

        draw_text('Maze Game', font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text('1. Bắt đầu', font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        draw_text('2. Hướng dẫn', font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text('3. Thoát', font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    start_game()
                elif event.key == pygame.K_2:
                    instructions()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def start_game():
    window_size = (600, 600)
    tile_size = 30
    game_screen = pygame.display.set_mode((window_size[0] + 150, window_size[1]))
    pygame.display.set_caption("Maze Game")

    game = Main(game_screen)
    game.main(window_size, tile_size)

# menu hướng dẫn
def instructions():
    while True:
        screen.blit(instructions_bgr, (0, 0))
        draw_text('Hãy chắc chắn rằng máy có camera,', font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4-80)
        draw_text('Giơ ngón trỏ trước màn hình camera', font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4-30)
        draw_text('Để điều khiển nhân vật.', font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4+20)
        screen.blit(instructions_img, (SCREEN_WIDTH // 2 -200, SCREEN_HEIGHT // 4 + 70))
        draw_text('Nhấn Esc để quay lại', font, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2+250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()

if __name__ == "__main__":
    main_menu()