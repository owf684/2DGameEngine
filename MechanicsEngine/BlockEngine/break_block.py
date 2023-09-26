import pygame
import copy
import math

class _break_block:

	def __init__(self):

		self.push_block_trigger= False
		self.theta = 1
		self.step = .1
		self.push_block_object = None

	def main_loop(self,GameObjects,levelObjects,PlayerEngine):
		
		self.handle_break_blocks(GameObjects,levelObjects,PlayerEngine)
		
		if self.push_block_trigger:

			self.push_block_animation(self.push_block_object)



	def handle_break_blocks(self,GameObjects,levelObjects,PlayerEngine):

		for objects in GameObjects:
			if objects.subClass == 'player':
				if objects.collisionUp and objects.collisionSubClass == 'platform':
					if "break" in objects.collisionObject.imagePath and not PlayerEngine.superMario:
						self.push_block_object = objects.collisionObject
						self.push_block_trigger = True


	def push_block_animation(self,objects):

		objects.position[1] += 2*math.cos(self.theta*math.pi)
		self.theta -= self.step 

		if self.theta <= 0:
			self.push_block_trigger = False
			self.theta = 1