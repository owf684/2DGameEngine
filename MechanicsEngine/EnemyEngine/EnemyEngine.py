import pygame
import copy
import threading


class _EnemyEngine:


	def __init__(self):
		self.enemy_index = 0
		self.goomba_troops = list()
		self.change_dir = False
		self.thread_started = False
	def main_loop(self, GameObjects, PlayerEngine, GraphicsEngine):

		self.move_enemy(GameObjects, PlayerEngine, GraphicsEngine)

	def move_enemy(self, GameObjects, PlayerEngine, GraphicsEngine):

		for objects in GameObjects:

			if objects.subClass == 'enemy':

				if objects.isRendered:
					self.isHit(objects,GameObjects, GraphicsEngine)
					self.change_direction(objects)
					self.change_position(objects,PlayerEngine)
				self.track_scroll(objects,PlayerEngine)

	def isHit(self,objects,GameObjects,GraphicsEngine):
		if objects.isHit:
			GameObjects.remove(objects)
			GraphicsEngine.render_buffer.remove(objects)
	def change_position(self,objects,PlayerEngine):
		position = copy.deepcopy(objects.position)
		position[0] -= objects.x_speed*objects.x_direction
		objects.position = position


	def track_scroll(self,objects,PlayerEngine):
		if PlayerEngine.scroll_level:
			objects.position[0] -= PlayerEngine.x_displacement
	def change_direction(self,objects):

		if objects.collisionLeft:
			objects.x_direction = -1
		if objects.collisionRight:
			objects.x_direction = 1





		#if objects.collisionRight:
		#	objects.x_direction = 1


