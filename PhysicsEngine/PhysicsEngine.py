import math

class _PhysicsEngine:

	def __init__(self):
		self.gravity = 9.8*150
		self.y_displacement = 0
		self.jump_displacement = 0
		self.x_displacement = 0
		self.x_direction = 0
		self.x_decelleration = 0.01
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

				if self.x_direction != objects.accelerationX/abs(objects.accelerationX):
					self.x_direction = objects.accelerationX/abs(objects.accelerationX)
					objects.velocity_X2 = 0
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
				objects.jump_velocity_1 = 300
			elif objects.jump_velocity_1 > 0:
				objects.jump_velocity_1 -= 20
			
			if delta_t != 0:
				objects.position[1] -= objects.jump_velocity_1*delta_t + (0.5 * (objects.jump_velocity_1/delta_t) * math.pow(delta_t,2) )
			
			print ("objects.jumping: " + str(objects.jumping))
			



