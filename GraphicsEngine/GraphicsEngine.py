
import pygame
import copy

class _GraphicsEngine:
	def __init__(self):
		pygame.init()
		self.screen_width = 720
		self.screen_height = 1280
		self.grid_size = 32
		self.grid_color = (255,255,255)

		#scan block
		self.scan_block_position = [0,0]
		self.scan_block_size = 32
		self.scan_block_color = (255,255,255)
		self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
		self.imageBuffer = list()

		pygame.display.set_caption("my PyGame Graphics")





	def _setScreenSize(self,screen_width,screen_height):
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))

	
	def _setScreenTitle(title):
		pygame.display.set_caption(title)



	def _addImage2Buffer(self,image_path):
		self.imageBuffer.append(pygame.image.load(image_path))


	def main_loop(self,GameObjects,levelObjects):

		#clear the screen
		self.screen.fill((0,0,0))

		for x in range(0, self.screen_width, self.grid_size):
			pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.screen_height))
		for y in range(0, self.screen_height, self.grid_size):
			pygame.draw.line(self.screen, self.grid_color, (0, y), (self.screen_width, y))
	
		#Update Graphics Here
		for objects in levelObjects:

			self.screen.blit(objects.image,(objects.position[0],objects.position[1]))

		#Update Graphics Here
		for objects in GameObjects:

			self.screen.blit(objects.image,(objects.position[0],objects.position[1]))


		#===========================================================================================================
    		# Draw the square
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
			placement_coords = copy.deepcopy(self.scan_block_position)
			print ("placement_coords: " + str(placement_coords))
		else:
			self.block_color = (255,255,255)

		pygame.draw.rect(self.screen, self.block_color, square_rect)

		#============================================================================================================

		#Update the display
		pygame.display.flip()


	
