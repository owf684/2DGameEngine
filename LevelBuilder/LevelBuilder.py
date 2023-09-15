import pygame
import sys
sys.path.append('./GameObjects')
import GameObject
import copy
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

	def main_loop(self,input_dict,screen,levelObjects,collisionList):
		

		self.poll_mouse(input_dict,screen,levelObjects,collisionList)
		self.draw_grid(input_dict,screen)


	def draw_grid(self,input_dict,screen):

		for x in range(0, self.screen_width, self.grid_size):
			pygame.draw.line(screen, self.grid_color, (x, 0), (x, self.screen_height))
		for y in range(0, self.screen_height, self.grid_size):
			pygame.draw.line(screen, self.grid_color, (0, y), (self.screen_width, y))
		

	def poll_mouse(self,input_dict,screen,levelObjects,collisionList):


		if input_dict['left-click'] == '1':
			self.mouse_position = pygame.mouse.get_pos()
			self.get_snap_values(input_dict,screen,levelObjects)

			if self.can_place_block:

				self.place_block(input_dict,screen,levelObjects,collisionList)


	def get_snap_values(self,input_dict,screen,levelObjects):
		self.can_place_block = True
		#get x snap value
		self.snap_position[0] = int(self.mouse_position[0]/self.grid_size)*self.grid_size
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

		
	def place_block(self,input_dict,screen,levelObjects,collisionList):

		#add first platform
		levelObjects.append(GameObject._GameObject())
		levelObjects[-1]._set_sub_class('platform')
		levelObjects[-1]._set_image_path('./Assets/Platforms/mario_brick.png')
		levelObjects[-1]._set_image()
		levelObjects[-1].position = copy.deepcopy(self.snap_position)
		self.list_of_placed_objects.append(copy.deepcopy(self.snap_position))
		levelObjects[-1]._set_sprite_size(levelObjects[-1].image)
		levelObjects[-1]._set_rect(levelObjects[-1].sprite_size)
		collisionList.append(levelObjects[-1])
		print("levelObjects: " + str( len(levelObjects) ) )
	
