import pygame


class _InputsEngine:

	def __init__(self):
		self.horizontal = 0
		self.vertical = 0
		self.input_dict = {
			"up"			: "0",
			"left"			: "0",
			"right"			: "0",
			"down" 			: "0",
			"left-click"	: "0",
			"right-click" 	: "0"
		}

	def main_loop(self,GameObjects,delta):
		posVector = pygame.math.Vector2()
		for objects in GameObjects:

			#inputs geared toward player sprite
			if objects.subClass == 'player':

				#awsd
				keys = pygame.key.get_pressed()

				#update player position based on key states
				if keys[pygame.K_a]:
					self.input_dict["left"] = '1'
					self.input_dict["right"] = '0'
					objects.accelerationX = -5000

				elif keys[pygame.K_d]:
					self.input_dict["right"] = '1'
					self.input_dict["left"] = '0'

					objects.accelerationX = 5000
				else:
					objects.accelerationX = 0.0
					self.input_dict["left"] = '0'
					self.input_dict["right"] = '0'

				#Jump
				if keys[pygame.K_w]:
					self.input_dict["up"] = '1'
				else:
					self.input_dict["up"] = '0'

				if keys[pygame.K_w] and objects.collisionDetected:
					objects.jumping = True
				elif not keys[pygame.K_w]:
					objects.jumping = False	

		
		mouse_buttons = pygame.mouse.get_pressed()
		if mouse_buttons[0]:
			self.input_dict["left-click"] = '1'
		else:
			self.input_dict["left-click"] = '0'

		if mouse_buttons[2]:
			self.input_dict["right-click"] = '1'
		else:
			self.input_dict["right-click"] = '0'



		return self.input_dict
				