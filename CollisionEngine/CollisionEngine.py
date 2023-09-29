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

			self.updateRectPosition(collisionBuffer[currentObject])

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
		self.ray_scan_up(collisionBuffer,objects,currentObject)
		self.ray_scan_down(collisionBuffer,objects,currentObject)
		#self.mask_left(collisionBuffer,objects,currentObject)

	def mask_left(self,collisionBuffer,objects,currentObject):
		if collisionBuffer[currentObject].image_mask.overlap(objects.image_mask,(objects.position[0]-collisionBuffer[currentObject].position[0],objects.position[1]-collisionBuffer[currentObject].position[1])):
			if objects.rect.collidepoint(collisionBuffer[currentObject].rect.midleft[0],collisionBuffer[currentObject].rect.midleft[1] + 5):
				collisionBuffer[currentObject].collisionSubClass = objects.subClass
				collisionBuffer[currentObject].collisionObjDirection = objects.x_direction
				collisionBuffer[currentObject].collisionObjects = objects
				collisionBuffer[currentObject].collisionLeft = True			
	
	def ray_scan_down(self,collisionBuffer,objects,currentObject):
	
		scan_depth, scan_point, scan_step, width = self.configure_scan_variables_ud(collisionBuffer, currentObject)

		while scan_point <= width:

			if objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomleft[0] + scan_point,collisionBuffer[currentObject].rect.bottom + scan_depth ):

				if collisionBuffer[currentObject].rect.colliderect(objects.rect):

					collisionBuffer[currentObject].position[1] = objects.rect.top - collisionBuffer[currentObject].rect.height
					collisionBuffer[currentObject].collisionDown = True
					if objects.subClass == 'enemy' and collisionBuffer[currentObject].subClass == "player":

						collisionBuffer[currentObject].onEnemy = True
						objects.isHit = True


			scan_point += scan_step

	def ray_scan_up(self,collisionBuffer,objects,currentObject):

		for pixel_points in collisionBuffer[currentObject]._get_pixel_collision_map()[0]:

			translated_point = (pixel_points[0] + collisionBuffer[currentObject].rect.x , pixel_points[1] + collisionBuffer[currentObject].rect.y )
			if objects.rect.collidepoint(translated_point[0],translated_point[1]-5):
				collisionBuffer[currentObject].collisionSubClass = objects.subClass
				collisionBuffer[currentObject].collisionObjDirection = objects.x_direction
				collisionBuffer[currentObject].collisionObject = objects
				collisionBuffer[currentObject].collisionUp = True
				break

	def ray_scan_left(self,collisionBuffer,objects,currentObject):
	
		height, scan_depth, scan_offset, scan_point, scan_step = self.configure_scan_variables_lr(collisionBuffer, currentObject)

		while scan_point <= height - scan_offset:

			if objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomleft[0] - scan_depth,collisionBuffer[currentObject].rect.top + scan_point ):
				collisionBuffer[currentObject].collisionSubClass = objects.subClass
				collisionBuffer[currentObject].collisionObjDirection = objects.x_direction
				collisionBuffer[currentObject].collisionObjects = objects
				collisionBuffer[currentObject].collisionLeft = True

			scan_point += scan_step

	def ray_scan_right(self,collisionBuffer,objects,currentObject):

		height, scan_depth, scan_offset, scan_point, scan_step = self.configure_scan_variables_lr(collisionBuffer, currentObject)
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
		if collisionBuffer[currentObject].subClass == 'enemy':
			scan_resolution = 3
			scan_offset = 5
		else:

			scan_offset = 28
			scan_resolution = copy.deepcopy(height) / 8

		scan_depth = 5
		scan_step = height / scan_resolution
		scan_point = 0
		return height, scan_depth, scan_offset, scan_point, scan_step

	def configure_scan_variables_ud(self, collisionBuffer, currentObject):
	
		width = copy.deepcopy(collisionBuffer[currentObject].rect.width)
		if collisionBuffer[currentObject].subClass == 'enemy':
			scan_resolution = 3
		else:
			scan_resolution = copy.deepcopy(width)

		scan_step = width / scan_resolution
		scan_point = 0
		scan_depth = 5

		return scan_depth, scan_point, scan_step, width

	def updateRectPosition(self,collisionObject):
	
		collisionObject.rect.x = collisionObject.position[0]
		collisionObject.rect.y = collisionObject.position[1]
