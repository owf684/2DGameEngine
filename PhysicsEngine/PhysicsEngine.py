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

			#self.collision_physics(objects,delta_t)
			self.simulate_gravity(objects,delta_t)
			self.x_position(objects,delta_t)

	def simulate_gravity(self,objects, delta_t):

		'''
		KINEMATIC EQUATIONS
		P(t) = VY * t + 0.5 * a * t^2

		V(t) = VY + a * t
		'''

		if objects.isRendered and not objects.pause_physics:

			objects.velocityY -= self.gravity * delta_t


			if  not objects.collisionDown or objects.jumping:

				objects.y_displacement = objects.velocityY*delta_t + (self.gravity * math.pow(delta_t,2) )
				objects.position[1] -= objects.y_displacement

			elif objects.collisionDown:
				objects.y_displacement = 0
				objects.velocityY =0


	def x_position(self,objects,delta_t):


		if objects.isRendered and not objects.pause_physics:

			objects.velocity_X1 = objects.velocityX*objects.x_direction

			if delta_t !=0:

				objects.x_acceleration = objects.velocity_X1/delta_t

			else:
				objects.x_acceleration = 0

			if (not objects.collisionLeft and objects.x_direction == -1) or (not objects.collisionRight and objects.x_direction == 1 ) or (objects.subClass == 'powerup' and objects.collisionSubClass == 'player'):
				objects.x_displacement = objects.velocity_X1*delta_t + (0.5*objects.x_acceleration*math.pow(delta_t,2))
			else:
				objects.x_displacement = 0
			if not objects.scrolling:

				objects.position[0] += objects.x_displacement


	


