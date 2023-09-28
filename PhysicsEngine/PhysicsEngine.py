import math

class _PhysicsEngine:

	def __init__(self):
		self.gravity = 9.8*100
		self.y_displacement = 0
		self.jump_displacement = 0
		self.x_displacement = 0
		self.x_direction = 0
		self.x_decelleration = 0.01
		self.y_displacement = 0
	def main_loop(self,GameObjects, delta_t):

		for objects in GameObjects:

			self.collision_physics(objects,delta_t)
			self.simulate_gravity(objects,delta_t)
			self.x_position(objects,delta_t)

	def simulate_gravity(self,objects, delta_t):

		'''
		KINEMATIC EQUATIONS
		P(t) = VY * t + 0.5 * a * t^2

		V(t) = VY + a * t
		'''

		if objects.isRendered and not objects.pause_physics:

			objects.velocity_Y1 -= self.gravity * delta_t


			if objects.collisionDown:
				objects.y_displacement = 0
				objects.velocity_Y1 =0
			else:
				objects.y_displacement = objects.velocity_Y1*delta_t + ( 0.5 * self.gravity * math.pow(delta_t,2) )
			
			objects.position[1] -= objects.y_displacement


	def x_position(self,objects,delta_t):


		if objects.isRendered and not objects.pause_physics:

			objects.velocity_X1 = objects.velocityX*objects.x_direction

			if delta_t !=0:

				objects.x_acceleration = objects.velocity_X1/delta_t

			else:
				objects.x_acceleration = 0

			objects.x_displacement = objects.velocity_X1*delta_t + (0.5*objects.x_acceleration*math.pow(delta_t,2))

			if not objects.scrolling:

				objects.position[0] += objects.x_displacement


	#change in momentum due to collision with another object
	def calculate_momentum(self,objects,delta_t):

		'''
		delta_p = change in momentum
		delta_p = m*delta_v
		'''
		objects.delta_p = objects.mass*objects.delta_v

	#change of velocity due to collision with another object
	def calculate_delta_v(self,objects,delta_t): 

		objects.final_v =(objects.mass*objects.initial_v + objects.collisionObject.mass*objects.collisionObject.initial_v)
		objects.final_v = objects.final_v/(objects.mass + objects.collisionObject.mass)
		objects.delta_v = objects.final_v - objects.initial_v 


	def collision_physics(self,objects,delta_t):
		if objects.velocity_X1 is not None:

			if objects.collisionLeft or objects.collisionRight:
				objects.initial_v = objects.velocity_X1
				objects.collisionObject.initial_v = objects.collisionObject.velocity_X1
				self.calculate_delta_v(objects,delta_t)
				self.calculate_momentum(objects,delta_t)
				objects.velocity_X1 = objects.delta_v
				print("objects.delta_p: " + str(objects.delta_p))
				print("objects.delta_v: "  + str(objects.delta_v))



