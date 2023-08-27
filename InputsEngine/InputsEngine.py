import pygame
class _InputsEngine:

	def __init__(self):
		self.horizontal = 0
		self.vertical = 0
		


	def main_loop(self,GameObjects,delta):

		for objects in GameObjects:

			#inputs geared toward player sprite
			if objects.subClass == 'player':

				#awsd
				keys = pygame.key.get_pressed()

				#update player position based on key states
				if keys[pygame.K_a]:

					 
					objects.position[0] -= objects._get_horizontal_velocity()*delta

					objects._set_horizontal_velocity(objects._get_horizontal_velocity()*2)
				
					if (objects._get_horizontal_velocity() > objects._get_max_horizontal_velocity()):

						objects._get_horizontal_velocity = objects._get_max_horizontal_velocity


				if keys[pygame.K_d]:
					objects.position[0] += objects._get_max_horizontal_velocity()*delta

    		
    			#if keys[pygame.K_w]:
        		#	player_y -= player_speed
    			#if keys[pygame.K_s]:
        		#	player_y += player_speed

