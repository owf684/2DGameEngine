import math

class _PhysicsEngine:

	def __init__(self):
		self.gravity = 9.8*100
		self.y_displacement = 0
		self.jump_displacement = 0
		self.x_displacement = 0
		self.x_direction = 0
		self.x_decelleration = 0.01
		self.jumping = False
		self.uc = 0
		self.highestUc = -1
		self.total_jump_displacement = 0
		self.jump_height = 0
		self.max_jump_height = 500
		self.time_tracker =0
		self.seconds = 0
	def main_loop(self,GameObjects, delta_t):


		self.simulate_gravity(GameObjects,delta_t)
		self.horizontal_acceleration(GameObjects,delta_t)
		self.jump(GameObjects,delta_t)
	def simulate_gravity(self,GameObjects, delta_t):

		'''
		KINEMATIC EQUATIONS
		P(t) = VY * t + 0.5 * a * t^2

		V(t) = VY + a * t
		'''

		for objects in GameObjects:


			objects.velocity_Y1 += self.gravity * delta_t

			objects.position[1] += objects.velocity_Y1*delta_t + ( 0.5 * self.gravity * math.pow(delta_t,2) )

			if objects.collisionDetected:
				objects.velocity_Y1 = 0

		self.time_tracker += delta_t
		if self.time_tracker >= 1:
			self.seconds += 1
			self.time_tracker = 0


	def horizontal_acceleration(self,GameObjects,delta_t):

		'''KINEMATIC EQUATIONS
		delta_x = v_initial * delta_t + 0.5 * a * delta_t^2
		velocitx_2 = sqrt(velocitx_1^2 + 2 * a * delta_x )

		'''

		for objects in GameObjects:

			self.x_displacement = (objects.velocity_X1 * delta_t) + (0.5 * objects.accelerationX * math.pow(delta_t,2))

			objects.position[0] += self.x_displacement
			try:

				objects.velocity_X2 = math.sqrt( math.pow(objects.velocity_X1,2) + 2*abs(objects.accelerationX) + self.x_displacement)
			except:
				None

			#set direction	
			if objects.accelerationX != 0:
				self.x_direction = objects.accelerationX/abs(objects.accelerationX)
			else:
				#deccelerate 
				if self.x_direction > 0:
					self.x_direction -= self.x_decelleration
				else:
					self.x_direction += self.x_decelleration

			#update velocity
			objects.velocity_X1 = objects.velocity_X2*self.x_direction



	def jump(self,GameObjects,delta_t):

		for objects in GameObjects:

			if objects.jumping:
				objects.jump_velocity_1 = 500
			
			if not objects.jumping and objects.jump_velocity_1 > 0 and not objects.collisionDetected :
				objects.jump_velocity_1 -= 10
			
			objects.position[1] -= objects.jump_velocity_1*delta_t
			self.jump_height += objects.jump_velocity_1*delta_t
			



