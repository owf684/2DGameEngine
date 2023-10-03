import pygame

class _GraphicsEngineData:

	screen_width 	= 0
	screen_height 	= 0
	screen = pygame.display.set_mode((screen_width,screen_height))



class _PlayerSpriteData:
	def __init__(self):
		self.image_path = ''
		self.image = None


	def set_image_path(self,value):
			self.image_path= value


	def set_image(self,value):

		try:
			self.image = pygame.image.load(value)

		except:
			print("image_path not found.")

	def get_image(self):

		return self.image

	def get_image_path(self):
		return self.image_path