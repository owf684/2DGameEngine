import pygame
import sys







class _AnimationSystem:

	def __init__(self):

		self.frame_size = (32,32)
		self.frame_count = 3
		self.frame_duration = 100

		self.current_time = 0
		self.elapsed_time = 0
		self.last_frame_time =0
		self.frame_index =0

		self.jumping = False
		self.idle_right = pygame.image.load("./Assets/PlayerSprites/mario_32x32_idle_right.png")
		self.idle_left = pygame.image.load('./Assets/PlayerSprites/mario_32x32_idle_left.png')
		self.jump_left = pygame.image.load("./Assets/PlayerSprites/mario_32x32_jump_left.png")
		self.jump_right = pygame.image.load("./Assets/PlayerSprites/mario_32x32_jump_right.png")
		self.run_right = self.extract_frames("./Assets/PlayerSprites/mario_32x32_run_right.png")
		self.run_left = self.extract_frames("./Assets/PlayerSprites/mario_32x32_run_left.png")
		self.jump_lock = False

		self.x_direction = 1
	def main_loop(self,GameObjects,input_dict):
		self.determine_frame_count()


		self.handle_run_animations(GameObjects,input_dict)

		self.handle_jump_animations(GameObjects,input_dict)

		self.handle_idle_animations(GameObjects,input_dict)


		print(self.jump_lock)

	def handle_jump_animations(self,GameObjects,input_dict):
		if input_dict['up'] == '1':
			for objects in GameObjects:
				if objects.subClass == 'player' and objects.jump_velocity_1> 0:
					if self.x_direction == 1:
						objects.image = self.jump_right
						self.jumping = True
					elif self.x_direction == -1:
						objects.image = self.jump_left
						self.jumping = True
					if objects.collisionDown and self.jumping:
						self.jumping = False

	def handle_run_animations(self,GameObjects,input_dict):
		if input_dict['l-shift'] == '1':
			self.frame_duration = 50
		else:
			self.frame_duration = 80

		if input_dict['right'] == '1':


			for objects in GameObjects:
				if objects.subClass == 'player' and not self.jumping:
					objects.image = self.run_right[self.frame_index]
					self.x_direction = 1
				elif objects.collisionDown and self.jumping:
					self.jumping = False

		if input_dict['left'] == '-1':
			for objects in GameObjects:
				if objects.subClass == 'player' and not self.jumping:
					objects.image = self.run_left[self.frame_index]
					self.x_direction = -1
				elif objects.collisionDown and self.jumping:
					self.jumping = False

	def handle_idle_animations(self,GameObjects,input_dict):
		if input_dict['right'] == '0' and input_dict['left'] == '0':

			for objects in GameObjects:
				if objects.subClass == 'player':
					if self.x_direction == 1 and not self.jumping:
						objects.image = self.idle_right
					elif self.x_direction == -1 and not self.jumping:
						objects.image = self.idle_left
					elif objects.collisionDown and self.jumping:
						self.jumping = False

	def determine_frame_count(self):
		self.current_time = pygame.time.get_ticks()
		self.elapsed_time = self.current_time - self.last_frame_time

		if self.elapsed_time >= self.frame_duration:
			self.frame_index = (self.frame_index + 1) % self.frame_count
			self.last_frame_time = self.current_time
	def extract_frames(self,frame_path):
		frames = list()
		sprite_sheet = pygame.image.load(frame_path)
		frame = sprite_sheet.subsurface((0,0,self.frame_size[0],self.frame_size[1]))
		frames.append(frame)
		frame = sprite_sheet.subsurface((32,0,self.frame_size[0],self.frame_size[1]))
		frames.append(frame)
		frame = sprite_sheet.subsurface((0, 32, self.frame_size[0], self.frame_size[1]))
		frames.append(frame)
		return frames




