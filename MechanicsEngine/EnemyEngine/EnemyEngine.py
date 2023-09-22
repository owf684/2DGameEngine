import pygame
import copy
import threading


class _EnemyEngine:


	def __init__(self):
		self.enemy_index = 0
		self.t1 = list()
		self.t2 = list()


	def main_loop(self,GameObjects,PlayerEngine):


		self.move_enemy(GameObjects,PlayerEngine)

	def move_enemy(self,GameObjects,PlayerEngine):

		for objects in GameObjects:

			if objects._get_sub_class() == 'enemy':

				if objects.isRendered:
					self.t1.append(threading.Thread(target=self.change_direction,args=(objects,)))
					self.t2.append(threading.Thread(target=self.change_position,args=(objects,)))

					self.t1[-1].start()
					self.t2[-1].start()
					self.t1[-1].join()
					self.t2[-1].join()
				#self.change_direction(objects)
				#self.change_position(objects)
					

				if PlayerEngine.scroll_level:

					objects.position[0] -= PlayerEngine.x_displacement

		for threads in self.t1:
			threads.join()
		for thread in self.t2:
			thread.join()
		self.t1.clear()
		self.t2.clear()	

	def change_position(self,objects):
		position = copy.deepcopy(objects.position)
		position[0] -= objects.x_speed*objects.x_direction
		objects.position = position
	def change_direction(self,objects):

		if objects.collisionLeft:
			objects.x_direction = -1
		if objects.collisionRight:
			objects.x_direction = 1