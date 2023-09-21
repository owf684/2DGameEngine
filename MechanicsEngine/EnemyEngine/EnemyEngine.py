import pygame
import copy



class _EnemyEngine:


	def __init__(self):
		self.enemy_speed = 1
		self.enemy_direction = -1



	def main_loop(self,GameObjects,PlayerEngine):


		self.move_enemy(GameObjects,PlayerEngine)

	def move_enemy(self,GameObjects,PlayerEngine):

		for objects in GameObjects:

			if objects._get_sub_class() == 'enemy':

				if objects.isRendered:

					self.change_position(objects)
					self.change_direction(objects)




				if PlayerEngine.scroll_level:

					objects.position[0] -= PlayerEngine.x_displacement

	def change_position(self,objects):
		position = copy.deepcopy(objects.position)
		position[0] -= self.enemy_speed*self.enemy_direction
		objects.position = position
	def change_direction(self,objects):

		if objects.collisionLeft:
			self.enemy_direction = -1
		if objects.collisionRight:
			self.enemy_direction = 1