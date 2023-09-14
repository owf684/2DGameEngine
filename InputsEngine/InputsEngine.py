import pygame
class _InputsEngine:

	def __init__(self):
		self.horizontal = 0
		self.vertical = 0
		 

	def main_loop(self,GameObjects,delta):
		posVector = pygame.math.Vector2()
		for objects in GameObjects:

			#inputs geared toward player sprite
			if objects.subClass == 'player':

				#awsd
				keys = pygame.key.get_pressed()

				#update player position based on key states
				if keys[pygame.K_a]:

					objects.accelerationX = -5000

				elif keys[pygame.K_d]:
					objects.accelerationX = 5000
				else:
					objects.accelerationX = 0.0
				#Jump
				if keys[pygame.K_w] and objects.collisionDetected:
					objects.jumping = True
				else:
					objects.jumping = False		
				