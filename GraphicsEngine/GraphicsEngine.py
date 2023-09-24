
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


		#render buffer
		self.render_buffer = list()
		self.levelObjectsIndex = 0
		self.GameObjectsIndex = 0

		pygame.display.set_caption("Fario Faker")


	def _setScreenSize(self, screen_width, screen_height):
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.screen = pygame.display.set_mode((self.screen_width,self.screen_height),pygame.DOUBLEBUF)

	
	def _setScreenTitle(self, title):
		pygame.display.set_caption(title)



	def _addImage2Buffer(self, image_path):
		self.imageBuffer.append(pygame.image.load(image_path))


	def main_loop(self,GameObjects,levelObjects,levelHandler, levelBuilder):
		#clear the screen
		self.screen.fill((92,148,252))
	
		if levelBuilder.edit:

			for x in range(0, self.screen_width+int(abs(levelHandler.scroll_offset)), self.grid_size):

				pygame.draw.line(self.screen, self.grid_color, (x-levelHandler.scroll_offset, 0), (x-levelHandler.scroll_offset, self.screen_height))
				levelHandler.eox = x - abs(levelHandler.scroll_offset)
				levelHandler.scroll_delta = 1248 - levelHandler.eox

			for y in range(0, self.screen_height, self.grid_size):
				pygame.draw.line(self.screen, self.grid_color, (0, y), (self.screen_width, y))

		if levelHandler.clear_render_buffer:
			self.render_buffer.clear()
			levelHandler.clear_render_buffer = False

		self.load_render_buffer(levelObjects,GameObjects)
	
		
		#Update Graphics Here
		for objects in self.render_buffer:

			self.screen.blit(objects.image,(objects.position[0],objects.position[1]))

		#Update the display
		pygame.display.flip()
		return self.screen

	def load_render_buffer(self, levelObjects, GameObjects):

		for objects in levelObjects:
			if objects not in self.render_buffer:
		
				if not objects.position[0] < -objects.sprite_size[0] and not objects.position[0] > self.screen_width:
					self.render_buffer.append(objects)

			if objects in self.render_buffer:

					if objects.position[0] < -objects.sprite_size[0] or objects.position[0] > self.screen_width:
						self.render_buffer.remove(objects)

		for objects in GameObjects:
			if objects.subClass == "player":
				if objects not in self.render_buffer:
					self.render_buffer.append(objects)
					objects.isRendered = True

			if objects.subClass == 'enemy':
				
				if objects not in self.render_buffer:

					if not objects.position[0] < -objects.sprite_size[0] and not objects.position[0] > self.screen_width:
						objects.isRendered = True
						self.render_buffer.append(objects)

				if objects in self.render_buffer:

					if objects.position[0] < -objects.sprite_size[0] or objects.position[0] > self.screen_width:
						objects.isRendered = False
						self.render_buffer.remove(objects)



	
