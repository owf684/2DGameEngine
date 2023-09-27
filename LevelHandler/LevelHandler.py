import pygame




class _LevelHandler:


	def __init__(self):
		self.scroll_offset = 0
		self.scroll_delta = 0
		self.clear_render_buffer = False
		self.eox = 0
		self.load_level = False
		self.currentLevel = 'level_1'
		self.screen_width = 0
		# Question Block List
		self.question_blocks = list()

	def main_loop(self,levelHandler,GameObjects,levelObjects,collisionList,screen, PlayerEngine,levelBuilder):
		self.scroll_level(levelObjects,PlayerEngine,GameObjects)

		self.player_death(levelHandler,GameObjects,levelObjects,collisionList,self.currentLevel,screen,levelBuilder)

	def player_death(self,levelHandler,GameObjects,levelObjects,collisionList,level,screen,levelBuilder):
		if levelHandler.load_level:
			levelHandler.load_level = False
			levelBuilder.load_level(GameObjects, levelObjects, collisionList, level, screen, levelHandler)
	def scroll_level(self,levelObjects,PlayerEngine,GameObjects):

		if (PlayerEngine.scroll_level):
			self.scroll_offset += PlayerEngine.x_displacement
			for objects in levelObjects:
				objects.position[0] -= PlayerEngine.x_displacement
				objects.rect.x -= PlayerEngine.x_displacement

				if objects.item is not None:
					objects.item.position[0] -= PlayerEngine.x_displacement
					objects.item.rect.x -= PlayerEngine.x_displacement

			for objects in GameObjects:
				if objects.subClass != 'player':
					objects.rect.x -= PlayerEngine.x_displacement
				if objects.item is not None:
					objects.item.position[0] -= PlayerEngine.x_displacement
					objects.item.rect.x -= PlayerEngine.x_displacement
