import pygame
from random import choice

class Cell:
	def __init__(self, x, y, thickness):
		self.x, self.y = x, y
		self.thickness = thickness
		self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
		self.visited = False

	#  cols và rows
		@property
		def cols(self):
			return max(cell.x for cell in self.grid_cells) + 1

		@property
		def rows(self):
			return max(cell.y for cell in self.grid_cells) + 1

	def draw(self, sc, tile):
		x, y = self.x * tile, self.y * tile
		if self.walls['top']:
			pygame.draw.line(sc, pygame.Color('darkgreen'), (x, y), (x + tile, y), self.thickness)
		if self.walls['right']:
			pygame.draw.line(sc, pygame.Color('darkgreen'), (x + tile, y), (x + tile, y + tile), self.thickness)
		if self.walls['bottom']:
			pygame.draw.line(sc, pygame.Color('darkgreen'), (x + tile, y + tile), (x , y + tile), self.thickness)
		if self.walls['left']:
			pygame.draw.line(sc, pygame.Color('darkgreen'), (x, y + tile), (x, y), self.thickness)

	def check_cell(self, x, y, cols, rows, grid_cells):
		find_index = lambda x, y: x + y * cols
		if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
			return False
		return grid_cells[find_index(x, y)]

	def check_neighbors(self, cols, rows, grid_cells):
		neighbors = []
		top = self.check_cell(self.x, self.y - 1, cols, rows, grid_cells)
		right = self.check_cell(self.x + 1, self.y, cols, rows, grid_cells)
		bottom = self.check_cell(self.x, self.y + 1, cols, rows, grid_cells)
		left = self.check_cell(self.x - 1, self.y, cols, rows, grid_cells)
		if top and not top.visited:
			neighbors.append(top)
		if right and not right.visited:
			neighbors.append(right)
		if bottom and not bottom.visited:
			neighbors.append(bottom)
		if left and not left.visited:
			neighbors.append(left)
		return choice(neighbors) if neighbors else False
	
	def __lt__(self, other):
		return self.x + self.y < other.x + other.y