import pygame, time

pygame.font.init()

class Clock:
	def __init__(self):
		self.start_time = None
		self.elapsed_time = 0
		self.font = pygame.font.Font("font/DancingScript-VariableFont_wght.ttf", 35)
		self.message_color = pygame.Color("yellow")

	def start_timer(self):
		self.start_time = time.time()

	def update_timer(self):
		if self.start_time is not None:
			self.elapsed_time = time.time() - self.start_time

	def display_timer(self):
		secs = int(self.elapsed_time % 60)
		mins = int(self.elapsed_time / 60)
		my_time = self.font.render(f"{mins:02}:{secs:02}", True, self.message_color)
		return my_time

	def stop_timer(self):
		self.start_time = None