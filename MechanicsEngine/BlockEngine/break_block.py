import pygame
import copy
import math

class _break_block:

	def __init__(self):

		self.push_block_trigger= False
		self.theta = 1
		self.step = .1
		self.push_block_object = None
		self.release_item_trigger = False

	def main_loop(self,GameObjects,levelObjects,PlayerEngine):
		
		self.handle_break_blocks(GameObjects,levelObjects,PlayerEngine)
		
		if self.push_block_trigger:

			self.push_block_animation(self.push_block_object)

		if self.release_item_trigger:

			self.release_item(self.push_block_object,GameObjects)

	def handle_break_blocks(self,GameObjects,levelObjects,PlayerEngine):

		for objects in GameObjects:
			if objects.subClass == 'player':
				if objects.collisionUp and objects.collisionSubClass == 'platform':
					if "break" in objects.collisionObject.imagePath and not PlayerEngine.superMario:
						self.push_block_object = objects.collisionObject
						self.push_block_trigger = True
						self.release_item_trigger = True

	def push_block_animation(self,objects):

		objects.position[1] += 2*math.cos(self.theta*math.pi)
		self.theta -= self.step 

		if self.theta <= 0:
			self.push_block_trigger = False
			self.theta = 1

	def release_item(self,push_block_object,GameObjects):
		if push_block_object.item is not None:
			item = push_block_object.item
			item.position[1] -= push_block_object.rect.height/2
			item.rect.y = item.position[1]
			item.pause_physics = False
			push_block_object.item = None
			item._set_mask()
			self.release_item_trigger = False
			GameObjects.append(item)
