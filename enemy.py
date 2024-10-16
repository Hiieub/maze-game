import pygame
import heapq

class Enemy:
    def __init__(self, x, y, maze, tile, player):
        self.x = int(x)
        self.y = int(y)
        self.maze = maze
        self.tile = tile
        self.player = player
        self.size = 12
        # self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        # self.color = (255, 0, 0)
        self.speed = 2
        self.start_time = pygame.time.get_ticks()

        # lưu đường dẫn đã tính toán
        self.cached_path = []
        self.last_player_position = (self.player.x, self.player.y)

        self.enemy_image = pygame.image.load("img/enemy/enemy.png").convert_alpha()
        self.enemy_image = pygame.transform.scale(self.enemy_image, (self.size, self.size))

    # def draw_path(self, screen):
    #     if self.cached_path:
    #         for cell in self.cached_path:
    #             pygame.draw.rect(screen, (0, 255, 0), (cell.x * self.tile, cell.y * self.tile, self.tile, self.tile), 2)

    def draw(self, screen):
        # self.draw_path(screen)
        screen.blit(self.enemy_image, (int(self.x), int(self.y)))

    def get_neighbors(self, cell):
        neighbors = []
        x, y = cell.x, cell.y
        if not cell.walls['top']:
            neighbors.append(self.maze.grid_cells[x + (y - 1) * self.maze.cols])
        if not cell.walls['right']:
            neighbors.append(self.maze.grid_cells[(x + 1) + y * self.maze.cols])
        if not cell.walls['bottom']:
            neighbors.append(self.maze.grid_cells[x + (y + 1) * self.maze.cols])
        if not cell.walls['left']:
            neighbors.append(self.maze.grid_cells[(x - 1) + y * self.maze.cols])
        return neighbors

    def heuristic(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def a_star(self):
        start_cell = self.maze.grid_cells[int(self.x // self.tile + (self.y // self.tile) * self.maze.cols)]
        end_cell = self.maze.grid_cells[int(self.player.x // self.tile + (self.player.y // self.tile) * self.maze.cols)]

        # if (self.player.x, self.player.y) == self.last_player_position and self.cached_path:
        #     return self.cached_path

        open_list = []
        heapq.heappush(open_list, (0, start_cell))
        came_from = {}

        # Sử dụng tọa độ x, y để tính chỉ số của mỗi ô trong lưới
        g_score = {cell: float('inf') for cell in self.maze.grid_cells}
        f_score = {cell: float('inf') for cell in self.maze.grid_cells}

        g_score[start_cell] = 0
        f_score[start_cell] = self.heuristic(start_cell, end_cell)

        while open_list:
            current_cell = heapq.heappop(open_list)[1]

            if current_cell == end_cell:
                path = []
                while current_cell in came_from:
                    path.append(current_cell)
                    current_cell = came_from[current_cell]
                path.append(start_cell)
                self.cached_path = path[::-1]
                self.last_player_position = (self.player.x, self.player.y)
                return self.cached_path

            for neighbor in self.get_neighbors(current_cell):
                tentative_g_score = g_score[current_cell] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_cell
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end_cell)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return []

    def move(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        # di chuyển sau 10s (19s-10s delay tạo mê cung)
        if elapsed_time >= 19000:
            path = self.a_star()
            if len(path) > 1:
                next_cell = path[1]
                target_x = next_cell.x * self.tile + self.tile // 2
                target_y = next_cell.y * self.tile + self.tile // 2

                dir_x = target_x - self.x
                dir_y = target_y - self.y

                distance = (dir_x ** 2 + dir_y ** 2) ** 0.5

                # cập nhật tốc độ dựa trên khoảng cách
                if distance > 0:
                    new_x = self.x + self.speed * (dir_x / distance)
                    new_y = self.y + self.speed * (dir_y / distance)

                    # check va chạm với tường
                    if not self.maze.is_wall_at(new_x, new_y, self.tile):
                        self.x = new_x
                        self.y = new_y

                # enemy vào trung tâm
                if abs(dir_x) < self.speed:
                    self.x = target_x
                if abs(dir_y) < self.speed:
                    self.y = target_y


                # self.rect.x = int(self.x)
                # self.rect.y = int(self.y)

    def is_wall_at(self, x, y):
        cell_x = int(x // self.tile)
        cell_y = int(y // self.tile)
        cell = self.maze.grid_cells[cell_x + cell_y * self.maze.cols]
        return cell.walls['top'] or cell.walls['bottom'] or cell.walls['left'] or cell.walls['right']