import pygame
import copy
import math

class _question_block:

	def __init__(self):

		self.question_block_trigger= False
		self.theta = 1
		self.step = .1
		self.question_block_object = None

	
	def main_loop(self,GameObjects,levelObjects,PlayerEngine):
		
		self.handle_question_blocks(GameObjects,levelObjects,PlayerEngine)
		
		if self.question_block_trigger:

			self.question_block_animation(self.question_block_object)

		self.question_block_color_change(levelObjects)


	def handle_question_blocks(self,GameObjects,levelObjects,PlayerEngine):

		for objects in GameObjects:
			if objects.subClass == 'player':
				if objects.collisionUp and objects.collisionSubClass == 'platform':
					if "Question" in objects.collisionObject.imagePath:
						self.question_block_object = objects.collisionObject
						self.question_block_trigger = True


	def question_block_animation(self,objects):

		objects.position[1] += math.cos(self.theta*math.pi)
		self.theta -= self.step 

		if self.theta <= 0:
			self.question_block_trigger = False
			self.theta = 1

	def question_block_color_change(self,levelObjects):
		for objects in levelObjects:
			if "Question" in objects.imagePath:
				print("hahahah")
				objects.image.convert()
				objects.image.set_colorkey((0, 255, 255))  # Set white color as transparent
