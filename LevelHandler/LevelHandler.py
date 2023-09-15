import pygame




class _LevelHandler:


	def __init__(self):
		self.scroll_offset = 0

		


	def main_loop(self,levelObjects,PlayerEngine):

		self.scroll_level(levelObjects,PlayerEngine)


	def scroll_level(self,levelObjects,PlayerEngine):

		if (PlayerEngine.scroll_level):
			self.scroll_offset += PlayerEngine.x_displacement

			for objects in levelObjects:
				objects.position[0] -= PlayerEngine.x_displacement
		print(self.scroll_offset)
	def _get_scroll_offset(self):
		return self.scroll_offset