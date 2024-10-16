import pygame
from cell import Cell

class Maze:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.thickness = 3
        self.grid_cells = [Cell(col, row, self.thickness) for row in range(self.rows) for col in range(self.cols)]

    def remove_walls(self, current, next):
        dx = current.x - next.x
        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls['top'] = False
            next.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next.walls['top'] = False

    def generate_maze(self, screen, tile):
        current_cell = self.grid_cells[0]
        array = []
        break_count = 1

        buffer_surface = pygame.Surface(screen.get_size())
        
        while break_count != len(self.grid_cells):
            current_cell.visited = True
            next_cell = current_cell.check_neighbors(self.cols, self.rows, self.grid_cells)

            # screen.fill((0, 0, 0))
            # self.draw_visited_cells(screen, tile)
            # self.highlight_cell(screen, current_cell, tile)
            buffer_surface.fill((0, 0, 0))
            self.draw_visited_cells(buffer_surface, tile)
            self.highlight_cell(buffer_surface, current_cell, tile)
            
            if next_cell:
                next_cell.visited = True
                break_count += 1
                array.append(current_cell)
                self.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif array:
                current_cell = array.pop()

            # [cell.draw(screen, tile) for cell in self.grid_cells]
            [cell.draw(buffer_surface, tile) for cell in self.grid_cells]
            screen.blit(buffer_surface, (0, 0))
            pygame.display.flip()
            # pygame.display.update()
            pygame.time.delay(10)  

    def highlight_cell(self, screen, cell, tile):
        x, y = cell.x * tile, cell.y * tile
        pygame.draw.rect(screen, (255, 0, 0), (x, y, tile, tile))  
        pygame.display.update()

    def draw_visited_cells(self, screen, tile):
        for cell in self.grid_cells:
            if cell.visited:
                x, y = cell.x * tile, cell.y * tile
                pygame.draw.rect(screen, (0, 255, 0), (x, y, tile, tile))

    def is_wall_at(self, x, y, tile):
        cell_x = int(x // tile)
        cell_y = int(y // tile)

        # Đảm bảo tọa độ nằm trong giới hạn của mê cung
        if 0 <= cell_x < self.cols and 0 <= cell_y < self.rows:
            cell = self.grid_cells[cell_x + cell_y * self.cols]
            
            # Kiểm tra xem ô hiện tại có tường nào không dựa trên vị trí
            if (x % tile == 0 and cell.walls['left']) or \
               (y % tile == 0 and cell.walls['top']) or \
               (x % tile == tile - 1 and cell.walls['right']) or \
               (y % tile == tile - 1 and cell.walls['bottom']):
                return True  # Có tường
        return False  # Không có 