

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

						
		
						self.handle_left_collisions(collisionBuffer,objects,currentObject)
						
						self.handle_right_collisions(collisionBuffer,objects,currentObject)

						self.handle_up_collisions(collisionBuffer,objects,currentObject)
						
						self.handle_down_collisions(collisionBuffer,objects,currentObject)



			currentObject += 1

	def handle_down_collisions(self,collisionBuffer,objects,currentObject):


		if collisionBuffer[currentObject].rect.colliderect(objects.rect) :

			if 	( 	objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomleft[0]+5, collisionBuffer[currentObject].rect.bottomleft[1] 	+ 1) or
					objects.rect.collidepoint(collisionBuffer[currentObject].rect.midbottom[0], collisionBuffer[currentObject].rect.midbottom[1] 	+ 1 ) or
					objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomright[0]-5, collisionBuffer[currentObject].rect.bottomright[1]+ 1) 

				):	

				collisionBuffer[currentObject].collisionDown = True

			if collisionBuffer[currentObject].collisionDown and not collisionBuffer[currentObject].collisionLeft and not collisionBuffer[currentObject].collisionRight:

				collisionBuffer[currentObject].position[1] = objects.rect.top - collisionBuffer[currentObject].rect.height

	def handle_left_collisions(self,collisionBuffer,objects,currentObject):

		if 	(	objects.rect.collidepoint(collisionBuffer[currentObject].rect.topleft[0] - collisionBuffer[currentObject].rect.width/20,collisionBuffer[currentObject].rect.topleft[1]) or
				objects.rect.collidepoint(collisionBuffer[currentObject].rect.midleft[0] - collisionBuffer[currentObject].rect.width/20,collisionBuffer[currentObject].rect.midleft[1]) or
				( objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomleft[0] - 5,collisionBuffer[currentObject].rect.bottomleft[1]) and 
				collisionBuffer[currentObject].rect.collidepoint(objects.rect.midright[0]-5, objects.rect.midright[1] ) ) 
			):
			collisionBuffer[currentObject].collisionLeft = True

	def handle_right_collisions(self,collisionBuffer,objects,currentObject):

		if 	(	objects.rect.collidepoint(collisionBuffer[currentObject].rect.topright[0] + collisionBuffer[currentObject].rect.width/20,collisionBuffer[currentObject].rect.topright[1]) or
				objects.rect.collidepoint(collisionBuffer[currentObject].rect.midright[0] + collisionBuffer[currentObject].rect.width/20,collisionBuffer[currentObject].rect.midright[1]) or
				( objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomright[0] + 5,collisionBuffer[currentObject].rect.bottomright[1]) and 
				collisionBuffer[currentObject].rect.collidepoint(objects.rect.midleft[0]+5, objects.rect.midleft[1] ) )

			):

			collisionBuffer[currentObject].collisionRight = True		

	def handle_up_collisions(self,collisionBuffer,objects,currentObject):
		if 	(	objects.rect.collidepoint(collisionBuffer[currentObject].rect.topleft[0]+5,collisionBuffer[currentObject].rect.topleft[1] - 1) or 
				objects.rect.collidepoint(collisionBuffer[currentObject].rect.midtop[0],collisionBuffer[currentObject].rect.midtop[1] - 1) or 
				objects.rect.collidepoint(collisionBuffer[currentObject].rect.topright[0]-5,collisionBuffer[currentObject].rect.topright[1] - 1)

			):
			collisionBuffer[currentObject].collisionUp = True



	def updateRectPosition(self,collisionObject):

		collisionObject.rect.x = collisionObject.position[0]
		
		collisionObject.rect.y = collisionObject.position[1]
