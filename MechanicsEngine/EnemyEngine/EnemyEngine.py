import pygame
import copy
import threading


class _EnemyEngine:


	def __init__(self):
		self.enemy_index = 0
		self.t1 = list()
		self.t2 = list()

		self.thread_started = False
	def main_loop(self,GameObjects,PlayerEngine):


		self.move_enemy(GameObjects,PlayerEngine)

	def move_enemy(self,GameObjects,PlayerEngine):

		for objects in GameObjects:

			if objects._get_sub_class() == 'enemy':

				if objects.isRendered:

					self.change_direction(objects)
					self.change_position(objects,PlayerEngine)




	def change_position(self,objects,PlayerEngine):
		position = copy.deepcopy(objects.position)
		position[0] -= objects.x_speed*objects.x_direction
		objects.position = position
		if PlayerEngine.scroll_level:
			objects.position[0] -= PlayerEngine.x_displacement
	def change_direction(self,objects):

		if objects.collisionLeft:
			objects.x_direction = -1
		if objects.collisionRight:
			objects.x_direction = 1