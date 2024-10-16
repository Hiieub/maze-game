import pygame, sys # Gọi thư viện pygame và thư viện sys

pygame.init() # Khởi tạo một chương trình pygame

# Khởi tạo kích thước màn hình game có ngang là 400, chiều dọc là 300
screen = pygame.display.set_mode((400, 300))

# Tiêu đề của chương trình Pygame
pygame.display.set_caption('Hello World!')

# Vòng lặp vô hạn
while True:
    # Vòng lặp bắt các sự kiện của chương trình pygame
    for event in pygame.event.get():
        # sự kiện ấn thoát game
        if event.type == pygame.QUIT:
            pygame.quit()  # Thoát khỏi chương trình pygame
            sys.exit()     # Thoát hệ thống

    # Cập nhật màn hình
    pygame.display.update()