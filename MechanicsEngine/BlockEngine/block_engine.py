import pygame
import copy
import math
import break_block
import question_block
class BlockEngine:

	def __init__(self):
		
		self.o_break_block = break_block.BreakBlock()
		self.o_question_block = question_block.QuestionBlock()
	def main_loop(self,l_game_objects,l_level_objects,o_player_engine,delta_t, objects):
		self.o_break_block.main_loop(l_game_objects, l_level_objects, o_player_engine, delta_t, objects)
		self.o_question_block.main_loop(l_game_objects, l_level_objects, o_player_engine, delta_t, objects)