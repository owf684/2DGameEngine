

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
		print(numObjects)
		while currentObject < numObjects:

			self.updateRectPosition(collisionBuffer[currentObject])

			#Reset collisions here please!
			collisionBuffer[currentObject].collisionDown = False
			collisionBuffer[currentObject].collisionLeft = False


			for objects in collisionBuffer:
				self.updateRectPosition(objects)
				
				if collisionBuffer[currentObject] != objects:

					if collisionBuffer[currentObject].subClass == 'player':

						
						self.handle_down_collisions(collisionBuffer,objects,currentObject)
		
						self.handle_left_collisions(collisionBuffer,objects,currentObject)
						





			currentObject += 1

	def handle_down_collisions(self,collisionBuffer,objects,currentObject):

		if collisionBuffer[currentObject].rect.colliderect(objects.rect) :

			if collisionBuffer[currentObject].rect.bottom > objects.rect.top:

				if not collisionBuffer[currentObject].rect.centery > objects.rect.top and not collisionBuffer[currentObject].rect.centery < objects.rect.bottom:

					collisionBuffer[currentObject].collisionDown = True
					collisionBuffer[currentObject].position[1] = objects.rect.top - collisionBuffer[currentObject].rect.height


		print ("collisonBuffer.collisionDown: " + str(collisionBuffer[currentObject].collisionDown))

	def handle_left_collisions(self,collisionBuffer,objects,currentObject):

		'''
		scenario 1	
					 ___
		object	-->	|	|  ___
					|___| |   | <-- player
						  |___|				  

		'''
		if collisionBuffer[currentObject].rect.top > objects.rect.top and collisionBuffer[currentObject].rect.top < objects.rect.bottom:

			if collisionBuffer[currentObject].rect.left < objects.rect.right:

					collisionBuffer[currentObject].collisionLeft = True
					print("scenario 1")
		'''
		scenario 2	 __    ___
		object 	--> |	| |   |  <-- player 
					|___| |___| 
						  
		'''					
		if collisionBuffer[currentObject].rect.centery == objects.rect.centery:

				if collisionBuffer[currentObject].rect.left < objects.rect.right:

					if collisionBuffer[currentObject].rect.right > objects.rect.left:

						collisionBuffer[currentObject].collisionLeft = True
						print("scenario 2")
		'''
		scenario 3		   ___
					 ___  |	  |	<-- player
		object 	--> |	| |___|
					|___|
		'''			
		if collisionBuffer[currentObject].rect.bottom < objects.rect.bottom  and collisionBuffer[currentObject].rect.bottom - 5 > objects.rect.top:

			if collisionBuffer[currentObject].rect.left < objects.rect.right and collisionBuffer[currentObject].rect.right > objects.rect.right:

					collisionBuffer[currentObject].collisionLeft = True
					print("player_bottom: " + str(collisionBuffer[currentObject].rect.bottom))
					print("objects_bottom: " + str(objects.rect.bottom))
					print("objects_top: " + str(objects.rect.top))
					print ("scenario 3")


	def updateRectPosition(self,collisionObject):

		collisionObject.rect.x = collisionObject.position[0]
		
		collisionObject.rect.y = collisionObject.position[1]
