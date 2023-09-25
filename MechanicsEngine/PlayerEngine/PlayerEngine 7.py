
import math

class _PlayerEngine:

	def __init__(self):
		self.gravity = 9.8*150
		self.y_displacement = 0
		self.x_displacement = 0
		self.x_direction = 0
		self.x_decelleration = 0.01
		self.screen_width = 1280
		self.scroll_level = False
		self.x_acceleration = 0
		self.stop_jump = False
		self.start_jump = False
		self.total_y_displacement = 0
		self.reached_max_height = False

	def main_loop(self,GameObjects,delta_t,input_dict,CollisionEngine):

		self.horizontal_movement(GameObjects,delta_t,input_dict,CollisionEngine)
		self.jump(GameObjects,delta_t,input_dict)
		


	def jump(self,GameObjects,delta_t,input_dict):

		for objects in GameObjects:

			if objects.subClass == 'player':

				#Handle jump velocity
				if input_dict['up'] == '1' and not objects.collisionUp and not self.reached_max_height:

					objects.jumping = True
					objects.jump_velocity_1 = 500

				elif (input_dict['up'] == '0' or self.reached_max_height) and not objects.collisionDown:

					objects.jump_velocity_1 -= 15	

				if objects.jump_velocity_1 < 0:
					objects.jump_velocity_1 = 0

				print ("jump_velocity_1: " + str(objects.jump_velocity_1))
				print ("y-displacement: " + str(self.y_displacement))
				if objects.collisionDown and input_dict['up'] == '0': 
					self.total_y_displacement = 0
					objects.jumping = False
					objects.jump_velocity_1 = 0
					self.reached_max_height = False

				if objects.collisionUp and not self.reached_max_height:
					self.total_y_displacement = 0
					objects.jumping = False
					objects.jump_velocity_1 = 0
					self.reached_max_height = True 

				#handle position calculations
				if delta_t != 0:

					self.y_displacement	= objects.jump_velocity_1*delta_t + (0.5 * (objects.jump_velocity_1/delta_t) * math.pow(delta_t,2) )
				
				objects.position[1] -= self.y_displacement

				self.total_y_displacement += self.y_displacement

				if self.total_y_displacement > 150:

					self.reached_max_height = True


	def horizontal_movement(self,GameObjects,delta_t,input_dict,CollisionEngine):

		'''KINEMATIC EQUATIONS
		delta_x = v_initial * delta_t + 0.5 * a * delta_t^2
		velocitx_2 = sqrt(velocitx_1^2 + 2 * a * delta_x )

		'''

		for objects in GameObjects:

			if objects.subClass == "player":

				self.set_x_acceleration(objects,input_dict,CollisionEngine)

				self.set_scroll_state(objects,input_dict)

				self.x_displacement = (objects.velocity_X1 * delta_t) + (0.5 * self.x_acceleration * math.pow(delta_t,2))

				if objects.collisionLeft and input_dict['right'] != '1' or objects.collisionRight and input_dict['left'] != '-1':
					self.x_displacement= 0


				if not self.scroll_level:
					objects.position[0] += self.x_displacement

				try:

					objects.velocity_X2 = math.sqrt( math.pow(objects.velocity_X1,2) + 2*abs(self.x_acceleration) + self.x_displacement)
				except:
					None

				self.set_x_direction(objects,input_dict)

				#update velocity
				objects.velocity_X1 = objects.velocity_X2*self.x_direction

	def set_x_acceleration(self,objects,input_dict,CollisionEngine):
		if input_dict['right'] == '1' and not CollisionEngine.collisionRight:
			self.x_acceleration = objects.accelerationX
		elif input_dict['left'] == '-1' and not CollisionEngine.collisionLeft:
			self.x_acceleration  = objects.accelerationX*int( input_dict['left'] )
		else:
			self.x_acceleration = 0 

	def set_x_direction(self,objects,input_dict):
		if self.x_acceleration != 0:

			if self.x_direction != self.x_acceleration/abs(self.x_acceleration):
				self.x_direction = self.x_acceleration/abs(self.x_acceleration)
				objects.velocity_X2 = 0
		else:
			#deccelerate 
			if self.x_direction > 0:
				self.x_direction -= self.x_decelleration
			else:
				self.x_direction += self.x_decelleration


	def set_scroll_state(self,objects,input_dict):

		
		#handle level scrolling left
		if objects.position[0] >= self.screen_width/2 and self.x_direction > 0 and input_dict['right'] == '1':
			self.scroll_level = True

		#handle level scrolling right
		elif objects.position[0] <= self.screen_width/8 and self.x_direction < 0 and input_dict['left'] == '-1':
			self.scroll_level = True
		else:
			self.scroll_level = False
