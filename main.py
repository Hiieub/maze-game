import pygame, sys, cv2
from maze import Maze
from player import Player
from game import Game
from clock import Clock
from enemy import Enemy

pygame.init()
pygame.font.init()

class Main():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("font/DancingScript-VariableFont_wght.ttf", 30)
        self.message_color = pygame.Color("white")
        self.running = True
        self.game_over = False
        self.win = False
        self.FPS = pygame.time.Clock()

    def instructions(self):
        instructions1 = self.font.render('Hãy đọc', True, self.message_color)
        instructions2 = self.font.render('hướng dẫn', True, self.message_color)
        instructions3 = self.font.render('trc khi chơi', True, self.message_color)
        self.screen.blit(instructions1, (610, 300))
        self.screen.blit(instructions2, (610, 331))
        self.screen.blit(instructions3, (610, 362))

    # vẽ mê cung, player, thời gian, enemy
    def _draw(self, maze, tile, player, game, clock, enemy):
        [cell.draw(self.screen, tile) for cell in maze.grid_cells]
        game.add_goal_point(self.screen)
        player.draw(self.screen)
        enemy.draw(self.screen)
        player.update(tile, maze.grid_cells, maze.thickness)

        self.instructions()

        if self.game_over:
            clock.stop_timer()
            if game.is_game_over(player):
                self.screen.blit(game.message('Tạm được!!'), (610, 120))
            else:
                self.screen.blit(game.message('Chơi lại đê!!'), (610, 120))
        else:
            clock.update_timer()
        self.screen.blit(clock.display_timer(), (625, 20))
        
        pygame.display.flip()

    # vòng lặp chính của game
    def main(self, frame_size, tile):
        cols, rows = frame_size[0] // tile, frame_size[-1] // tile
        maze = Maze(cols, rows)
        game = Game(maze.grid_cells[-1], tile)
        player = Player(tile // 3 + tile, tile // 3 + tile)
        enemy = Enemy(tile // 3, tile // 3, maze, tile, player)
        # enemy = Enemy(tile * (cols - 2), tile * (rows - 2), maze, tile, player)
        clock = Clock()

        #quá trình tạo mê cung
        maze.generate_maze(self.screen, tile)

        cap = cv2.VideoCapture(0)

        clock.start_timer()
        while self.running:
            self.screen.fill("gray")
            self.screen.fill(pygame.Color("darkslategray"), (603, 0, 752, 752))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            enemy.move()
            # enemy.draw(self.screen)

            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)

                # vẽ 2 kẽ đỏ trong cam
                frame_height, frame_width, _ = frame.shape
                mid_x = frame_width // 2
                mid_y = frame_height // 2
                cv2.line(frame, (mid_x, 0), (mid_x, frame_height), (0, 0, 255), 2)
                cv2.line(frame, (0, mid_y), (frame_width, mid_y), (0, 0, 255), 2)

                player.process_hand_gesture(frame)

                player.check_move(tile, maze.grid_cells, maze.thickness)

                cv2.imshow('CAMERA', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # if game.is_game_over(player):
            #     self.game_over = True
            #     player.left_pressed = False
            #     player.right_pressed = False
            #     player.up_pressed = False
            #     player.down_pressed = False

            # điều kiện thắng/thua
            if game.is_game_over(player):
                self.game_over = True
                # self.running = False
                self.win = True
                # player.left_pressed = False
                # player.right_pressed = False
                # player.up_pressed = False
                # player.down_pressed = False
                player.speed = 0
                enemy.speed = 0
            if game.check_enemy_catch_player(enemy, player):
                self.game_over = True
                # self.running = False
                self.win = False
                # player.left_pressed = False
                # player.right_pressed = False
                # player.up_pressed = False
                # player.down_pressed = False
                player.speed = 0

            # vẽ lại mê cung, player, thời gian, enemy
            self._draw(maze, tile, player, game, clock, enemy)
            self.FPS.tick(60)

            # thông báo thắng/thua
            if self.game_over:
                if self.win:
                    self.screen.blit(game.message('Thắng!!'), (610, 120))
                else:
                    lose_msg = self.font.render('Chơi lại đi!!', True, pygame.Color("red"))
                    self.screen.blit(lose_msg, (610, 120)) 

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    window_size = (600, 600)
    screen = (window_size[0] + 150, window_size[-1])
    tile_size = 30
    screen = pygame.display.set_mode(screen)
    pygame.display.set_caption("Maze")

    game = Main(screen)
    game.main(window_size, tile_size)