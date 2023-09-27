import pygame
import copy




class _SuperMushroom:

	def __init__(self):
		self.velocity_x = 1

	def main_loop(self,GameObjects,levelHandler,PlayerEngine):
		for objects in GameObjects:
			if objects.subClass == 'powerup' and 'mushroom' in objects.imagePath:
				if objects.isRendered:

					self.move_mushroom(objects)
					
					self.detectCollisions(objects)

				self.track_scroll_mushroom(objects,levelHandler,PlayerEngine)

	def track_scroll_mushroom(self,objects,levelHandler,PlayerEngine):

		if PlayerEngine.scroll_level:
			objects.position[0] -= PlayerEngine.x_displacement

	def move_mushroom(self,objects):
		print(objects.subClass)
		position = copy.deepcopy(objects.position)
		position[0] -= self.velocity_x*objects.x_direction
		objects.position = position

	def detectCollisions(self,objects):

		if objects.collisionLeft:
			objects.x_direction = 1

		if objects.collisionRight:
			objects.x_direction = -1