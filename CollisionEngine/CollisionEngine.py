

class _CollisionEngine:

	def __init__(self):

		self.collision = False


	def main_loop(self,collisionBuffer,GraphicsEngine):

		i = 0
		currentObject = 0

		#only process collisions with objects that are rendered
		if len(GraphicsEngine.render_buffer) > 0:
			collisionBuffer = GraphicsEngine.render_buffer


		numObjects = len(collisionBuffer)
	
		while currentObject < numObjects:
			print(numObjects)
			print (currentObject)
			self.updateRectPosition(collisionBuffer[currentObject])
			collisionBuffer[currentObject].collisionDetected = False
			for objects in collisionBuffer:

				self.updateRectPosition(objects)
				
				if collisionBuffer[currentObject] != objects and collisionBuffer[currentObject].rect.colliderect(objects.rect):

					collisionBuffer[currentObject].collisionDetected = True
					if collisionBuffer[currentObject].subClass == 'player' and collisionBuffer[currentObject].rect.centery < objects.rect.centery:
						collisionBuffer[currentObject].position[1] = objects.rect.top - collisionBuffer[currentObject].rect.height
				

			currentObject += 1



	def updateRectPosition(self,collisionObject):

		collisionObject.rect.x = collisionObject.position[0]
		
		collisionObject.rect.y = collisionObject.position[1]
