import copy
import pygame
import threading
from multiprocessing import Process
class _CollisionEngine:

	def __init__(self):

		self.collision = False
		self.collisionLeft = False
		self.collisionRight = False
		self.collisionDown = False
		self.threadStarted = False
		self.screen = None
		self.collisionThread = list()
	def main_loop(self,collisionBuffer,GraphicsEngine,input_dict,screen):
		self.screen = screen
		i = 0
		currentObject = 0

		# only process collisions with objects that are rendered
		if len(GraphicsEngine.render_buffer) > 0:
			collisionBuffer = GraphicsEngine.render_buffer

		numObjects = len(collisionBuffer)
	
		while currentObject < numObjects:

			#self.updateRectPosition(collisionBuffer[currentObject])

			# Reset collisions here please!
			collisionBuffer[currentObject].collisionDown = False
			collisionBuffer[currentObject].collisionLeft = False
			collisionBuffer[currentObject].collisionRight = False
			collisionBuffer[currentObject].collisionUp = False




			for objects in collisionBuffer:

				self.updateRectPosition(objects)
				if collisionBuffer[currentObject] != objects:

					if (collisionBuffer[currentObject].subClass == 'player' or collisionBuffer[currentObject].subClass == 'enemy' or collisionBuffer[currentObject].subClass == 'powerup') and objects.subClass != 'environment':
						self.detectCollisions(collisionBuffer, objects, currentObject)
			
			currentObject += 1

	

	def detectCollisions(self,collisionBuffer,objects,currentObject):

		self.ray_scan_left(collisionBuffer,objects,currentObject)
		self.ray_scan_right(collisionBuffer,objects,currentObject)
		self.mask_scan_up(collisionBuffer,objects,currentObject)
		self.mask_scan_down(collisionBuffer,objects,currentObject)

		if collisionBuffer[currentObject].subClass == 'player':

			if collisionBuffer[currentObject].collisionLeft:

				print("collisionLeft: " + str(collisionBuffer[currentObject].collisionLeft))
			if collisionBuffer[currentObject].collisionRight:

				print("collisionRight: " + str(collisionBuffer[currentObject].collisionRight))
			if collisionBuffer[currentObject].collisionUp:

				print("collisionUp: " + str(collisionBuffer[currentObject].collisionUp))
			if collisionBuffer[currentObject].collisionDown:

				print("collisionDown: " + str(collisionBuffer[currentObject].collisionDown))
	def mask_scan_up(self,collisionBuffer,objects,currentObject):
		if collisionBuffer[currentObject].rect.colliderect(objects.rect):
			if collisionBuffer[currentObject].rect.top < objects.rect.bottom:
				if collisionBuffer[currentObject].rect.bottom > objects.rect.bottom:
					if collisionBuffer[currentObject].rect.bottom > objects.rect.top:
						collisionBuffer[currentObject]._set_mask()
						objects._set_mask()
						if collisionBuffer[currentObject].image_mask.overlap(objects.image_mask, (
						collisionBuffer[currentObject].position[0] - objects.position[0],
						collisionBuffer[currentObject].position[1] - objects.position[1])):
							collisionBuffer[currentObject].collisionSubClass = objects.subClass
							collisionBuffer[currentObject].collisionObjDirection = objects.x_direction
							collisionBuffer[currentObject].collisionObject = objects
							collisionBuffer[currentObject].collisionUp = True
							objects.isHit = True


	def mask_scan_down(self,collisionBuffer,objects,currentObject):
		if collisionBuffer[currentObject].rect.colliderect(objects.rect):
			if collisionBuffer[currentObject].rect.bottom > objects.rect.top:
				if collisionBuffer[currentObject].rect.top < objects.rect.bottom:
					if collisionBuffer[currentObject].rect.top < objects.rect.top:
						if collisionBuffer[currentObject].rect.centery+5 < objects.rect.centery:
							collisionBuffer[currentObject]._set_mask()
							objects._set_mask()
							if collisionBuffer[currentObject].image_mask.overlap(objects.image_mask, (objects.position[0] - collisionBuffer[currentObject].position[0],objects.position[1] - collisionBuffer[currentObject].position[1] )):
								collisionBuffer[currentObject].position[1] = objects.rect.top - collisionBuffer[currentObject].rect.height
								collisionBuffer[currentObject].collisionDown = True
								if objects.subClass == 'enemy' and collisionBuffer[currentObject].subClass == "player":
									collisionBuffer[currentObject].onEnemy = True
									objects.isHit = True

	def ray_scan_left(self,collisionBuffer,objects,currentObject):
	
		height, scan_depth, scan_offset, scan_point, scan_step = self.configure_scan_variables_lr(collisionBuffer, currentObject)
		if objects.subClass == 'enemy' and collisionBuffer[currentObject].subClass != 'enemy':
			scan_depth = 0
		while scan_point <= height - scan_offset:

			if objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomleft[0] - scan_depth,collisionBuffer[currentObject].rect.top + scan_point ):
				collisionBuffer[currentObject].collisionSubClass = objects.subClass
				collisionBuffer[currentObject].collisionObjDirection = objects.x_direction
				collisionBuffer[currentObject].collisionObjects = objects
				collisionBuffer[currentObject].collisionLeft = True

			scan_point += scan_step

	def ray_scan_right(self,collisionBuffer,objects,currentObject):

		height, scan_depth, scan_offset, scan_point, scan_step = self.configure_scan_variables_lr(collisionBuffer, currentObject)
		if objects.subClass == 'enemy' and collisionBuffer[currentObject].subClass != 'enemy':
			scan_depth = 0
		while scan_point <= height - scan_offset:

			if objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomright[0] + scan_depth,  collisionBuffer[currentObject].rect.top + scan_point ):
				collisionBuffer[currentObject].collisionSubClass = objects.subClass
				collisionBuffer[currentObject].collisionObjDirection = objects.x_direction
				collisionBuffer[currentObject].collisionObject = objects
				collisionBuffer[currentObject].collisionRight = True
				break
			scan_point += scan_step


	def configure_scan_variables_lr(self, collisionBuffer, currentObject):
	
		height = copy.deepcopy(collisionBuffer[currentObject].rect.height)
		if collisionBuffer[currentObject].subClass != 'player':
			scan_resolution = 3
			scan_offset = 5
		else:

			scan_offset = 10
			scan_resolution = copy.deepcopy(height)

		scan_depth = 10
		scan_step = height / scan_resolution
		scan_point = 0
		return height, scan_depth, scan_offset, scan_point, scan_step


	def updateRectPosition(self,collisionObject):
	
		collisionObject.rect.x = collisionObject.position[0]
		collisionObject.rect.y = collisionObject.position[1]
