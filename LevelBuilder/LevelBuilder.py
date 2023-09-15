import pygame

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
	def main_loop(self,input_dict,screen):
		

		self.poll_mouse(input_dict,screen)
		self.draw_grid(input_dict,screen)


	def draw_grid(self,input_dict,screen):
		for x in range(0, self.screen_width, self.grid_size):
			pygame.draw.line(screen, self.grid_color, (x, 0), (x, self.screen_height))
		for y in range(0, self.screen_height, self.grid_size):
			pygame.draw.line(screen, self.grid_color, (0, y), (self.screen_width, y))
	

	def poll_mouse(self,input_dict,screen):


		if input_dict['left-click'] == '1':
			self.mouse_position = pygame.mouse.get_pos()
			print(self.mouse_position)		
			self.scan_screen(screen)




	def scan_screen(self,screen):
		# Create a surface with alpha transparency
		transparent_block = pygame.Surface((self.scan_block_size,self.scan_block_size), pygame.SRCALPHA)

		# Set the color and transparency for the block (RGBA format)
		self.block_color = (1, 1, 1, 10)  # Red with 50% transparency




		width_poll = self.screen_width/self.scan_block_size
		height_poll = self.screen_height/self.scan_block_size

		iterate = width_poll*height_poll
		i = 0
		while (i < iterate):
			square_rect = pygame.Rect(self.scan_block_position[0], self.scan_block_position[1], self.scan_block_size, self.scan_block_size)
			placement_coords = [0,0]
			if self.scan_block_position[0] < self.screen_width:
				self.scan_block_position[0] += self.scan_block_size
			else:
				self.scan_block_position[0] = 0
				if self.scan_block_position[1] < self.screen_height:
					self.scan_block_position[1] += self.scan_block_size
				else:
					self.scan_block_position[1] = 0


			#check if cursor is in contact with mouse
 			# Check for collision with the mouse cursor
			mouse_x, mouse_y = pygame.mouse.get_pos()

			if square_rect.collidepoint(mouse_x, mouse_y):
				self.block_color = (0, 255, 0)  # Change block color when cursor touches it
				self.scan_block_position[0] -= self.scan_block_size
				placement_coords = copy.deepcopy(self.scan_block_position)
				self.placement_coords = placement_coords[0],placement_coords[1]

				print ("placement_coords: " + str(placement_coords))
				break

			else:
				self.block_color = (1, 1, 1, 10)




			#pygame.draw.rect(screen, self.block_color, square_rect)
			pygame.draw.rect(transparent_block, self.block_color, transparent_block.get_rect())
			# Blit (draw) the transparent block onto the screen
			screen.blit(transparent_block, self.scan_block_position)

			pygame.display.flip()
			i+=1
		
