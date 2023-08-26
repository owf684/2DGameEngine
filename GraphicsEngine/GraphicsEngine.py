
import pygame


class _GraphicsEngine:
	def __init__(self):
		pygame.init()
		self.screen_width = 300
		self.screen_height = 400
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


	def main_loop(self):

		#clear the screen
		self.screen.fill((0,0,0))

		#Update Graphics Here
		for images in self.imageBuffer:

			self.screen.blit(images,(0,0))

		#Update the display
		pygame.display.flip()


	