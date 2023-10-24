
import pygame
import copy
import sys
sys.path.append('./GameObjects')
import fire_power

class GraphicsEngine:
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
		self.image_buffer = list()


		#render buffer
		self.render_buffer = list()
		self.unrendered_size = 32
		self.level_objects_index = 0
		self.game_objects_index = 0
		self.environment_sprites = list()
		self.level_sprites = list()
		pygame.display.set_caption("Fario Faker")


	def set_screen_size(self, screen_width, screen_height):
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.screen = pygame.display.set_mode((self.screen_width,self.screen_height),pygame.DOUBLEBUF)

	
	def set_screen_title(self, title):
		pygame.display.set_caption(title)



	def add_image_2_buffer(self, image_path):
		self.image_buffer.append(pygame.image.load(image_path))


	def main_loop(self,l_game_objects,l_level_objects,o_level_handler, o_level_builder):
		#clear the screen
		self.screen.fill((92,148,252))
	


		if o_level_handler.clear_render_buffer:
			self.render_buffer.clear()
			o_level_handler.clear_render_buffer = False

		self.load_render_buffer(l_level_objects,l_game_objects)
		# Update Graphics Here
		for objects in self.render_buffer:
			self.screen.blit(objects.image,(objects.position[0],objects.position[1]))
			#pygame.draw.rect(self.screen,(255,0,0),objects.rect,2)
			#if objects.hit_box is not None:
			#	pygame.draw.rect(self.screen,(255,0,0),objects.hit_box,2)
			#if objects.kill_box is not None:
			#	pygame.draw.rect(self.screen,(255,0,0),objects.kill_box,2)

		if o_level_builder.edit:

			for x in range(0, self.screen_width+int(abs(o_level_handler.scroll_offset)), self.grid_size):
				pygame.draw.line(self.screen, self.grid_color, (x-o_level_handler.scroll_offset, 0), (x-o_level_handler.scroll_offset, self.screen_height))
				o_level_handler.eox = x - abs(o_level_handler.scroll_offset)
				o_level_handler.scroll_delta = 1248 - o_level_handler.eox
				o_level_handler.screen_width = self.screen_width + int(abs(o_level_handler.scroll_offset))

			for y in range(0, self.screen_height, self.grid_size):
				pygame.draw.line(self.screen, self.grid_color, (0, y), (self.screen_width, y))

			for uie in o_level_builder.ui_elements:
				self.screen.blit(uie.active_image, (uie.position[0], uie.position[1]))
				if uie.item_image is not None:
					self.screen.blit(uie.item_image,(uie.item_position[0],uie.item_position[1]) )
				if uie.rect is not None:
					pygame.draw.rect(self.screen,(0,0,255),uie.rect,2)



		# Update the display
		pygame.display.flip()
		return self.screen

	def load_render_buffer(self, levelObjects, GameObjects):

		for objects in levelObjects:
			if objects not in self.render_buffer:
		
				if not objects.position[0] < -objects.sprite_size[0]-self.unrendered_size and not objects.position[0] > self.screen_width+self.unrendered_size:
					if objects.subClass == 'environment':
						self.render_buffer.insert(0,objects) # using insert ensures player is always drawn last.
					else:
						self.render_buffer.append(objects)

			if objects in self.render_buffer:

				if objects.position[0] < -objects.sprite_size[0]-self.unrendered_size or objects.position[0] > self.screen_width+self.unrendered_size:
					self.render_buffer.remove(objects)



		for objects in GameObjects:
			if objects.subClass == "player":
				if objects not in self.render_buffer:
					self.render_buffer.append(objects)
					objects.isRendered = True

			if objects.subClass == 'enemy' or objects.subClass =='powerup' or isinstance(objects,fire_power.FirePower) or objects.subClass == 'item':
				
				if objects not in self.render_buffer:

					if not objects.position[0] < -objects.sprite_size[0] and not objects.position[0] > self.screen_width:
						objects.isRendered = True
						self.render_buffer.append(objects)

				if objects in self.render_buffer:

					if objects.position[0] < -objects.sprite_size[0] or objects.position[0] > self.screen_width:
						objects.isRendered = False
						self.render_buffer.remove(objects)



	
