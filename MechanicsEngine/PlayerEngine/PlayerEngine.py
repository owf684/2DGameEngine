import copy
import math

class _PlayerEngine:

	def __init__(self):
		self.gravity = 9.8*100
		self.y_displacement = 0
		self.x_displacement = 0
		self.x_direction = 0
		self.x_decelleration = 0.1
		self.screen_width = 1280
		self.scroll_level = False
		self.x_acceleration = 0
		self.total_y_displacement = 0
		self.reached_max_height = False
		self.max_walk_velocity = 150
		self.max_run_velocity = 300
		self.superMario = False
		self.jump_latch = False
		self.runningFactor = 1

	def main_loop(self, GameObjects, delta_t, input_dict, CollisionEngine,levelHandler):
		for objects in GameObjects:
			if objects.subClass == 'player':
				self.horizontal_movement(objects, delta_t, input_dict, CollisionEngine,levelHandler)
				self.jump(objects,delta_t,input_dict)
				self.onEnemy(objects)
				self.handle_damage(objects,levelHandler)

	def handle_damage(self, objects,levelHandler):
		if (objects.collisionLeft or objects.collisionRight) and objects.collisionSubClass == 'enemy':
			levelHandler.load_level = True

	def onEnemy(self,objects):
		if objects.subClass =='player':
			if objects.onEnemy:
				objects.jump_velocity_1 = 250
				objects.onEnemy = False

	def jump(self,objects,delta_t,input_dict):
			#Handle jump velocity
			if input_dict['up'] == '1' and not objects.collisionUp and not self.reached_max_height:
				objects.jumping = True
				objects.jump_velocity_1 = 450

			elif input_dict['up'] == '0' or self.reached_max_height:
				objects.jump_velocity_1 -= 15

			if objects.collisionDown:

				if input_dict['up'] == '0':
					self.total_y_displacement = 0
					objects.jumping = False
					self.reached_max_height = False

			if self.total_y_displacement > 100:
				self.reached_max_height = True

			if objects.collisionUp and not self.reached_max_height:
				self.total_y_displacement = 0
				objects.jumping = False
				objects.jump_velocity_1 = 0
				self.reached_max_height = True
			if objects.jump_velocity_1 < 0:
				objects.jump_velocity_1 = 0
			#handle position calculations
			if delta_t != 0:
				self.y_displacement	= objects.jump_velocity_1*delta_t + (0.5 * (objects.jump_velocity_1/delta_t) * math.pow(delta_t,2) )
				if self.y_displacement < 0:
					self.y_displacement = 0
				objects.position[1] -= self.y_displacement
				objects.rect.y -= self.y_displacement
				self.total_y_displacement += self.y_displacement


	def horizontal_movement(self,objects,delta_t,input_dict,CollisionEngine,levelHandler):

		self.set_scroll_state(objects,input_dict,levelHandler)

		if input_dict['right'] == '1':
			objects.velocityX = 100*self.runningFactor
			objects.x_direction = 1
		elif input_dict['left'] == '-1':
			objects.velocityX = 100*self.runningFactor
			objects.x_direction = -1
		else:
			objects.velocityX = 0
		
		if input_dict['l-shift'] == '1':
			self.runningFactor = 2
		else:
			self.runningFactor = 1

		self.x_displacement = objects.x_displacement
		self.x_direction = objects.x_direction


	def set_scroll_state(self,objects,input_dict,levelHandler):

		#handle level scrolling left
		if objects.position[0] >= self.screen_width/2 and self.x_direction > 0 and input_dict['right'] == '1':
			self.scroll_level = True
			objects.scrolling = True
		#handle level scrolling right
		elif objects.position[0] < self.screen_width/2 and self.x_direction < 0 and input_dict['left'] == '-1' and levelHandler.scroll_offset > 0:
			self.scroll_level = True
			objects.scrolling = True
		else:
			self.scroll_level = False
			objects.scrolling = False

