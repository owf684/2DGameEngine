

class _CollisionEngine:

	def __init__(self):

		self.collision = False


	def main_loop(self,collisionList):

		i = 0
		numObjects = len(collisionList)
		currentObject = 0

		while currentObject < numObjects:
			self.updateRectPosition(collisionList[currentObject])
			collisionList[currentObject].collisionDetected = False
			for objects in collisionList:

				self.updateRectPosition(objects)
				
				if collisionList[currentObject] != objects and collisionList[currentObject].rect.colliderect(objects.rect):

					collisionList[currentObject].collisionDetected = True
					if collisionList[currentObject].subClass == 'player' and collisionList[currentObject].rect.centery < objects.rect.centery:
						collisionList[currentObject].position[1] = objects.rect.top - collisionList[currentObject].rect.height
				

			currentObject += 1



	def updateRectPosition(self,collisionObject):

		collisionObject.rect.x = collisionObject.position[0]
		
		collisionObject.rect.y = collisionObject.position[1]
