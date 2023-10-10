import pygame


class _InputsEngine:

	def __init__(self):
		self.hold_create =False
		self.horizontal = 0
		self.vertical = 0
		self.input_dict = {
			"up"			: "0",
			"left"			: "0",
			"right"			: "0",
			"down" 			: "0",
			"left-click"	: "0",
			"right-click" 	: "0",
			"create-level" 	: "0",
			"patch-level"	: "0",
			"load-level"	: "0",
			"arrow_vert"	: "0",
			"arrow_hori"	: "0",
			"l_shift"		: "0",
			"edit"    		: "0",
			"attack"		: "0"
		}

	def main_loop(self,GameObjects,delta,pygame_events):
		posVector = pygame.math.Vector2()
		for objects in GameObjects:

			#inputs geared toward player sprite
			if objects.subClass == 'player':

				#awsd
				keys = pygame.key.get_pressed()

				#update player position based on key states
				if keys[pygame.K_a]:
					self.input_dict["left"] = '-1'
					self.input_dict["right"] = '0'

				elif keys[pygame.K_d]:
					self.input_dict["right"] = '1'
					self.input_dict["left"] = '0'

				else:
					self.input_dict["left"] = '0'
					self.input_dict["right"] = '0'

				if keys[pygame.K_w]:
					self.input_dict["up"] = '1'
				else:
					self.input_dict["up"] = '0'

				if keys[pygame.K_c] and not self.hold_create:
					self.input_dict['create-level'] = '1'
					self.hold_create = True
				else:
					self.input_dict['create-level'] = '0'

				if self.hold_create and not keys[pygame.K_c]:
					self.hold_create = False

				if keys[pygame.K_l]:
					self.input_dict["load-level"] = '1'
				else:
					self.input_dict["load-level"] = '0'

				if keys[pygame.K_UP]:
					self.input_dict["arrow_vert"] = "1"
				elif keys[pygame.K_DOWN]:
					self.input_dict["arrow_vert"] = "-1"
				else:
					self.input_dict["arrow_vert"] = "0"

				if keys[pygame.K_LEFT]:
					self.input_dict['arrow_hori'] = '-1'
				elif keys[pygame.K_RIGHT]:
					self.input_dict['arrow_hori'] = '1'
				else:
					self.input_dict['arrow_hori'] = '0'
					
				if keys[pygame.K_p]:
					self.input_dict["patch-level"] = '1'
				else:
					self.input_dict["patch-level"] = '0'

				if keys[pygame.K_LSHIFT]:
					self.input_dict["l-shift"] = '1'
				else:
					self.input_dict["l-shift"] = '0'

				if keys[pygame.K_e]:
					self.input_dict['edit'] = '1'
				else:
					self.input_dict['edit'] = '0'
					
				if keys[pygame.K_SPACE]:
					self.input_dict['attack'] = '1'
				else:
					self.input_dict['attack'] = '0'

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

						

				
