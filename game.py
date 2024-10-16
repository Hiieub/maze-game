# import pygame

# pygame.font.init()

# class Game:
# 	def __init__(self, goal_cell, tile):
# 		self.font = pygame.font.SysFont("impact", 35)
# 		self.message_color = pygame.Color("darkorange")
# 		self.goal_cell = goal_cell
# 		self.tile = tile

# 	def add_goal_point(self, screen):
# 		img_path = 'img/gate.png'
# 		img = pygame.image.load(img_path)
# 		img = pygame.transform.scale(img, (self.tile, self.tile))
# 		screen.blit(img, (self.goal_cell.x * self.tile, self.goal_cell.y * self.tile))

# 	def message(self):
# 		msg = self.font.render('You Win!!', True, self.message_color)
# 		return msg

# 	def is_game_over(self, player):
# 		goal_cell_abs_x, goal_cell_abs_y = self.goal_cell.x * self.tile, self.goal_cell.y * self.tile
# 		if player.x >= goal_cell_abs_x and player.y >= goal_cell_abs_y:
# 			return True
# 		else:
# 			return False

import pygame

pygame.font.init()

class Game:
    def __init__(self, goal_cell, tile):
        self.font = pygame.font.Font("font/DancingScript-VariableFont_wght.ttf", 30)
        self.message_color = pygame.Color("white")
        self.goal_cell = goal_cell
        self.tile = tile
        self.game_over = False

    def add_goal_point(self, screen):
        img_path = 'img/gate.png'
        img = pygame.image.load(img_path)
        img = pygame.transform.scale(img, (self.tile, self.tile))
        screen.blit(img, (self.goal_cell.x * self.tile, self.goal_cell.y * self.tile))

    def message(self, text):
        msg = self.font.render(text, True, self.message_color)
        return msg

    def is_game_over(self, player):
        goal_cell_abs_x, goal_cell_abs_y = self.goal_cell.x * self.tile, self.goal_cell.y * self.tile
        if player.x >= goal_cell_abs_x and player.y >= goal_cell_abs_y:
            return True
        else:
            return False
    # check enemy va player
    def check_enemy_catch_player(self, enemy, player):
        if abs(enemy.x - player.x) <= enemy.size and abs(enemy.y - player.y) <= enemy.size:
            self.game_over = True
            return True
        return False

    # def display_end_message(self, screen, player_wins):
    #     if player_wins:
    #         screen.blit(self.message('Thắng!!'), (100, 100))
    #     else:
    #         screen.blit(self.message('Chơi lại đi!!'), (100, 100))