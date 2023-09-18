

class _CollisionEngine:

	def __init__(self):

		self.collision = False
		self.collisionLeft = False
		self.collisionRight = False
		self.collisionDown = False

	def main_loop(self,collisionBuffer,GraphicsEngine,input_dict):

		i = 0
		currentObject = 0

		#only process collisions with objects that are rendered
		if len(GraphicsEngine.render_buffer) > 0:
			collisionBuffer = GraphicsEngine.render_buffer


		numObjects = len(collisionBuffer)
		while currentObject < numObjects:

			self.updateRectPosition(collisionBuffer[currentObject])

			#Reset collisions here please!
			collisionBuffer[currentObject].collisionDown = False
			collisionBuffer[currentObject].collisionLeft = False
			collisionBuffer[currentObject].collisionRight = False
			collisionBuffer[currentObject].collisionUp = False

			for objects in collisionBuffer:
				self.updateRectPosition(objects)
				
				if collisionBuffer[currentObject] != objects:

					if collisionBuffer[currentObject].subClass == 'player':

						
		
						#self.handle_left_collisions(collisionBuffer,objects,currentObject)
						
						#self.handle_right_collisions(collisionBuffer,objects,currentObject)

						self.handle_up_collisions(collisionBuffer,objects,currentObject)
						
						self.handle_down_collisions(collisionBuffer,objects,currentObject)



			currentObject += 1

	def handle_down_collisions(self,collisionBuffer,objects,currentObject):

		if collisionBuffer[currentObject].rect.colliderect(objects.rect) :
			if collisionBuffer[currentObject].rect.bottom > objects.rect.top:

				if collisionBuffer[currentObject].rect.centery < objects.rect.top:

					collisionBuffer[currentObject].collisionDown = True

			'''if collisionBuffer[currentObject].rect.midbottom[0] > objects.rect.topleft[0] and collisionBuffer[currentObject].rect.midbottom[0] < objects.rect.topright[0]:

				if collisionBuffer[currentObject].rect.centery < objects.rect.midbottom[1]:

					if collisionBuffer[currentObject].rect.bottom > objects.rect.top:
						print("scenario 1: down collision")
						collisionBuffer[currentObject].collisionDown = True


			if collisionBuffer[currentObject].rect.bottomright[0] > objects.rect.topleft[0] and collisionBuffer[currentObject].rect.bottomright[0] < objects.rect.midtop[0]:

				if collisionBuffer[currentObject].rect.midtop[1] < objects.rect.midbottom[1]:

					if collisionBuffer[currentObject].rect.bottom > objects.rect.top:
						print("scenario 2: down collision")
						collisionBuffer[currentObject].collisionDown = True


			if collisionBuffer[currentObject].rect.bottomleft[0] > objects.rect.midtop[0] and collisionBuffer[currentObject].rect.bottomleft[0] < objects.rect.topright[0]:
				if collisionBuffer[currentObject].rect.bottom > objects.rect.top:
					print("scenario 3: down collision")
					collisionBuffer[currentObject].collisionDown = True'''

			if collisionBuffer[currentObject].collisionDown:
					
				collisionBuffer[currentObject].position[1] = objects.rect.top - collisionBuffer[currentObject].rect.height


	def handle_left_collisions(self,collisionBuffer,objects,currentObject):


		if collisionBuffer[currentObject].rect.colliderect(objects.rect):

			'''
			scenario 1	
						 ___
			object	-->	|	|  ___
						|___| |   | <-- player
							  |___|				  

			'''
			if collisionBuffer[currentObject].rect.topleft[1] > objects.rect.midright[1] and collisionBuffer[currentObject].rect.topleft[1] < objects.rect.bottomright[1]:
		
				if collisionBuffer[currentObject].rect.midright[0] > objects.rect.centerx:

					if collisionBuffer[currentObject].rect.left < objects.rect.right:
						collisionBuffer[currentObject].collisionLeft = True
						print("scenario 1: left collision")
			'''d
			scenario 2	 __    ___
			object 	--> |	| |   |  <-- player 
						|___| |___| 
							  
			'''					
			if objects.rect.topright[1] < collisionBuffer[currentObject].rect.midleft[1] and collisionBuffer[currentObject].rect.midleft[1] < objects.rect.bottomright[1]:
				if collisionBuffer[currentObject].rect.midright[0] > objects.rect.centerx:

					if collisionBuffer[currentObject].rect.left > objects.rect.left:
					
						if collisionBuffer[currentObject].rect.left < objects.rect.right:
							print("scenario 2: left collision")
							collisionBuffer[currentObject].collisionLeft = True

			'''
			scenario 3		   ___
						 ___  |	  |	<-- player
			object 	--> |	| |___|
						|___|
			'''			
			if collisionBuffer[currentObject].rect.bottomleft[1] > objects.rect.topright[1]+10 and collisionBuffer[currentObject].rect.bottomleft[1] < objects.rect.midright[1]:

				if collisionBuffer[currentObject].rect.midright[0] > objects.rect.centerx:

					if collisionBuffer[currentObject].rect.left < objects.rect.right:
						print("scenario 3: left collision")
						collisionBuffer[currentObject].collisionLeft = True

	def handle_right_collisions(self,collisionBuffer,objects,currentObject):


		if collisionBuffer[currentObject].rect.colliderect(objects.rect):

			'''
			scenario 1	
						 ___
			player	-->	|	|  ___
						|___| |   | <-- object
							  |___|				  

			'''
			if collisionBuffer[currentObject].rect.bottomright[1] > objects.rect.topleft[1] + 10 and collisionBuffer[currentObject].rect.bottomright[1] < objects.rect.bottomleft[1]:
				if collisionBuffer[currentObject].rect.midleft[0] < objects.rect.midright[0]:
					if collisionBuffer[currentObject].rect.midright[0] > objects.rect.centerx:
						print("scenario 1: right collision")
						collisionBuffer[currentObject].collisionRight = True
			'''
			scenario 2	 __    ___
			player 	--> |	| |   |  <-- object 
						|___| |___| 
							  
			'''					
			if objects.rect.topleft[1] < collisionBuffer[currentObject].rect.midright[1] and collisionBuffer[currentObject].rect.midright[1] < objects.rect.bottomleft[1]:

				if collisionBuffer[currentObject].rect.midleft[0] < objects.rect.centerx:
					
					if collisionBuffer[currentObject].rect.right > objects.rect.left:
						collisionBuffer[currentObject].collisionRight = True
						print("scenario 2: right collision")

			'''
			scenario 3		   ___
						 ___  |	  |	<-- object
			player 	--> |	| |___|
						|___|
			'''			
			if collisionBuffer[currentObject].rect.topright[1] > objects.rect.midleft[1] and collisionBuffer[currentObject].rect.topright[1] < objects.rect.bottomleft[1]:
				if collisionBuffer[currentObject].rect.midleft[0] < objects.rect.centerx:
					if collisionBuffer[currentObject].rect.right > objects.rect.left:
						print("scenario 3: right collision")
						collisionBuffer[currentObject].collisionRight = True

	def handle_up_collisions(self,collisionBuffer,objects,currentObject):


		if collisionBuffer[currentObject].rect.colliderect(objects.rect):

			if collisionBuffer[currentObject].rect.midtop[0] > objects.rect.bottomleft[0] and collisionBuffer[currentObject].rect.midtop[0] < objects.rect.bottomright[0]:
				if objects.rect.centery < collisionBuffer[currentObject].rect.midbottom[1]:

					if collisionBuffer[currentObject].rect.top < objects.rect.bottom:
						collisionBuffer[currentObject].collisionUp = True
		#print(collisionBuffer[currentObject].collisionUp)
	def updateRectPosition(self,collisionObject):

		collisionObject.rect.x = collisionObject.position[0]
		
		collisionObject.rect.y = collisionObject.position[1]
