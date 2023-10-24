import sys
sys.path.append("./GameObject")
import block_object

class LevelHandler:


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

	def main_loop(self,l_game_objects,l_level_objects,l_collision_objects,screen, o_player_engine,o_level_builder, o_enemy_engine):
		self.scroll_level(l_level_objects,o_player_engine,l_game_objects)

		o_enemy_engine.track_scroll(l_game_objects, o_player_engine)
		
		self.player_death(l_game_objects,l_level_objects,l_collision_objects,self.currentLevel, screen,o_level_builder)

	def player_death(self,l_game_objects,l_level_objects,l_collision_objects,level,screen,o_level_builder):
		if self.load_level:
			self.load_level = False
			o_level_builder.load_level(l_game_objects, l_level_objects, l_collision_objects, level, screen, self)
	def scroll_level(self,l_level_objects,o_player_engine,l_game_objects):
		if (o_player_engine.scroll_level):

			self.scroll_offset += o_player_engine.x_displacement

			for objects in l_level_objects:
				objects.position[0] -= o_player_engine.x_displacement
				objects.rect.x -= o_player_engine.x_displacement

				if isinstance(objects,block_object.BlockObject):
					if objects.item is not None:
						objects.item.position[0] -= o_player_engine.x_displacement
						objects.item.rect.x -= o_player_engine.x_displacement

			for objects in l_game_objects:
				if objects.subClass != 'player':
					objects.rect.x -= o_player_engine.x_displacement
					if objects.hit_box is not None:

						objects.hit_box.x -= o_player_engine.x_displacement

				if isinstance(objects,block_object.BlockObject):
					if objects.item is not None:
						objects.item.position[0] -= o_player_engine.x_displacement
						objects.item.rect.x -= o_player_engine.x_displacement
