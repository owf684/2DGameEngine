import pygame
import sys
sys.path.append('./GameObjects')
import GameObject
import copy
import glob
import os
class _LevelBuilder:


	def __init__(self):

		self.mouse_position = [0,0]
		self.scan_block_position = [0,0]
		self.scan_block_size = 32
		self.screen_width = 1280
		self.screen_height = 720
		self.block_color = (255,255,255)
		self.grid_size = 32
		self.grid_color = (255,255,255)
		self.placement_coords = [0,0]
		self.snap_position = [0,0]
		self.can_place_block = True
		self.list_of_placed_objects = list()
		self.scroll_offset_magnitude = 1
		self.scroll_offset_fudge = 0.5
		self.building_blocks = list()

		self.block_select_key = False
		self.selected_block_index = 0

		self.initialize_building_blocks()

	def initialize_building_blocks(self):
		block_list = glob.glob('./Assets/Platforms/*.png')

		for blocks in block_list:
			new_block = GameObject._GameObject()
			new_block._set_sub_class('platform')
			new_block._set_image_path(blocks)
			new_block._set_image()
			new_block.position = [self.screen_width/2,self.screen_height/20]
			new_block._set_sprite_size(new_block.image)
			self.building_blocks.append(new_block)
	

	

	def main_loop(self,input_dict,screen,levelObjects,collisionList,levelHandler,PlayerEngine):
		
		self.poll_mouse(input_dict,screen,levelObjects,collisionList,levelHandler)
		self.ui(input_dict,screen,levelObjects,collisionList,levelHandler)
				
	def poll_mouse(self,input_dict,screen,levelObjects,collisionList,levelHandler):


		if input_dict['left-click'] == '1':

			self.mouse_position = pygame.mouse.get_pos()
			
			self.get_snap_values(input_dict,screen,levelObjects,levelHandler)

			if self.can_place_block:

				self.place_block(input_dict,screen,levelObjects,collisionList,levelHandler)


	def get_snap_values(self,input_dict,screen,levelObjects,levelHandler):

		self.can_place_block = True
		#get x snap value
		if levelHandler.scroll_offset != 0:
			self.scroll_offset_magnitude = levelHandler.scroll_offset/levelHandler.scroll_offset
		else:
			self.scroll_offset_magnitude = 1
			self.scroll_offset_fudge = 0


		self.snap_position[0] = int((self.mouse_position[0]) /self.grid_size)*self.grid_size-(levelHandler.scroll_delta*self.scroll_offset_magnitude)
		#print(self.snap_position[0])
		#get y snap value
		self.snap_position[1] = int(self.mouse_position[1]/self.grid_size)*self.grid_size

		#draw the placement sqaure
		square_rect = pygame.Rect(self.snap_position[0], self.snap_position[1], self.scan_block_size, self.scan_block_size)
		
		#check if block already exists
		if self.snap_position in self.list_of_placed_objects:
			self.can_place_block = False

		pygame.draw.rect(screen, self.block_color, square_rect)
		#update the screen
		pygame.display.flip()

		
	def place_block(self,input_dict,screen,levelObjects,collisionList,levelHandler):

		#add first platform
		levelObjects.append(GameObject._GameObject())
		levelObjects[-1]._set_sub_class('platform')
		levelObjects[-1]._set_image_path(self.building_blocks[self.selected_block_index]._get_image_path())
		levelObjects[-1]._set_image()
		levelObjects[-1].position = copy.deepcopy(self.snap_position)
		self.list_of_placed_objects.append(copy.deepcopy(self.snap_position))
		levelObjects[-1]._set_sprite_size(levelObjects[-1].image)
		levelObjects[-1]._set_rect(levelObjects[-1].sprite_size)
		collisionList.append(levelObjects[-1])
	


	def ui(self,input_dict,screen,levelObjects,collisionList,levelHandler):
			
		self.handle_user_input(input_dict)

		self.limit_selection_index()

		screen.blit(self.building_blocks[self.selected_block_index].image,(self.building_blocks[self.selected_block_index].position[0],self.building_blocks[self.selected_block_index].position[1]))
		pygame.display.flip()


	def handle_user_input(self,input_dict):

		if input_dict["arrow_vert"] == "1" and not self.block_select_key:
			self.block_select_key = True
			self.selected_block_index += 1
		elif input_dict["arrow_vert"] == "-1" and not self.block_select_key:
			self.block_select_key = True
			self.selected_block_index -= 1
		else:
			self.block_select_key = False	

	def limit_selection_index(self):

		if self.selected_block_index < 0:
			self.selected_block_index = 0

		elif self.selected_block_index >= len(self.building_blocks):
			self.selected_block_index = len(self.building_blocks)-1	

		#print(self.selected_block_index)