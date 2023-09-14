import pygame


class _LevelBuilder:


	def __init__(self):

		self.mouse_position = [0,0]


	def main_loop(self,input_dict):
		

		self.poll_mouse(input_dict)

	def poll_mouse(self,input_dict):


		if input_dict['left-click'] == '1':
			self.mouse_position = pygame.mouse.get_pos()
			print(self.mouse_position)		







		
