import sys
sys.path.append("./GameObject")
import BlockObject
import FirePower
class _LevelHandler:


	def __init__(self):
		self.scroll_offset = 0
		self.scroll_delta = 0
		self.clear_render_buffer = False
		self.eox = 0
		self.load_level = False
		self.currentLevel = 'level_1'
		self.screen_width = 0
		self.pause_for_damage = False
		self.freeze_damage = False
		self.decrease_power = False
		self.trigger_death_animation = False
		self.trigger_powerup_animation = False
		self.trigger_block_fx = False
		self.edit_mode = False
		# Question Block List
		self.question_blocks = list()

	def main_loop(self,levelHandler,GameObjects,levelObjects,collisionList,screen, PlayerEngine,levelBuilder, EnemyEngine):
		self.scroll_level(levelObjects,PlayerEngine,GameObjects, levelHandler)

		EnemyEngine.track_scroll(GameObjects, PlayerEngine)
		
		self.player_death(GameObjects,levelObjects,collisionList,self.currentLevel, screen,levelBuilder)

	def player_death(self,GameObjects,levelObjects,collisionList,level,screen,levelBuilder):
		if self.load_level:
			self.load_level = False
			levelBuilder.load_level(GameObjects, levelObjects, collisionList, level, screen, self)
	def scroll_level(self,levelObjects,PlayerEngine,GameObjects, levelHandler):
		if (PlayerEngine.scroll_level):

			self.scroll_offset += PlayerEngine.x_displacement

			for objects in levelObjects:
				objects.position[0] -= PlayerEngine.x_displacement
				objects.rect.x -= PlayerEngine.x_displacement

				if isinstance(objects,BlockObject._BlockObject):
					if objects.item is not None:
						objects.item.position[0] -= PlayerEngine.x_displacement
						objects.item.rect.x -= PlayerEngine.x_displacement

			for objects in GameObjects:
				if objects.subClass != 'player':
					objects.rect.x -= PlayerEngine.x_displacement
					if objects.hit_box is not None:

						objects.hit_box.x -= PlayerEngine.x_displacement

				if isinstance(objects,BlockObject._BlockObject):
					if objects.item is not None:
						objects.item.position[0] -= PlayerEngine.x_displacement
						objects.item.rect.x -= PlayerEngine.x_displacement
