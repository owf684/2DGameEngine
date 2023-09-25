import pygame
import copy
import math
import break_block
import question_block
class _BlockEngine:

	def __init__(self):
		
		self.bb = break_block._break_block()
		self.qb = question_block._question_block()

	def main_loop(self,GameObjects,levelObjects,PlayerEngine):

		self.bb.main_loop(GameObjects,levelObjects,PlayerEngine)
		self.qb.main_loop(GameObjects,levelObjects,PlayerEngine)