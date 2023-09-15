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

		








