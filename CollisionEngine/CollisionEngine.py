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
		self.collisionThread = list()
	def main_loop(self,collisionBuffer,GraphicsEngine,input_dict):

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

					if (collisionBuffer[currentObject].subClass == 'player' or collisionBuffer[currentObject].subClass == 'enemy') and objects.subClass != 'environment':

						self.detectCollisions(collisionBuffer, objects, currentObject)

			currentObject += 1


	def detectCollisions(self,collisionBuffer,objects,currentObject):

		self.ray_scan_left(collisionBuffer,objects,currentObject)
		self.ray_scan_right(collisionBuffer,objects,currentObject)
		self.ray_scan_up(collisionBuffer,objects,currentObject)
		self.ray_scan_down(collisionBuffer,objects,currentObject)


	def ray_scan_down(self,collisionBuffer,objects,currentObject):
		scan_depth, scan_point, scan_step, width = self.configure_scan_variables_ud(collisionBuffer, currentObject)

		while scan_point <= width:

			if objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomleft[0] + scan_point,collisionBuffer[currentObject].rect.bottom + scan_depth ):

				if collisionBuffer[currentObject].rect.colliderect(objects.rect):

					collisionBuffer[currentObject].collisionDown = True
					collisionBuffer[currentObject].collisionSubClass = objects.subClass
					collisionBuffer[currentObject].position[1] = objects.rect.top - collisionBuffer[currentObject].rect.height
					if objects.subClass == 'enemy' and collisionBuffer[currentObject].subClass == "player":
						collisionBuffer[currentObject].onEnemy = True
						objects.isHit = True
					break

			scan_point += scan_step

	def configure_scan_variables_ud(self, collisionBuffer, currentObject):
		width = copy.deepcopy(collisionBuffer[currentObject].rect.width)
		if collisionBuffer[currentObject].subClass == 'enemy':
			scan_resolution = 3
		else:
			scan_resolution = copy.deepcopy(width) / 8
		scan_step = width / scan_resolution
		scan_point = 0
		scan_depth = 2
		return scan_depth, scan_point, scan_step, width

	def ray_scan_left(self,collisionBuffer,objects,currentObject):
		height, scan_depth, scan_offset, scan_point, scan_step = self.configure_scan_variables_lr(collisionBuffer, currentObject)

		while scan_point <= height - scan_offset:

			if objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomleft[0] - scan_depth,collisionBuffer[currentObject].rect.top + scan_point ):
				collisionBuffer[currentObject].collisionSubClass = objects.subClass
				collisionBuffer[currentObject].collisionLeft = True
				break

			scan_point += scan_step

	def configure_scan_variables_lr(self, collisionBuffer, currentObject):
		height = copy.deepcopy(collisionBuffer[currentObject].rect.height)
		if collisionBuffer[currentObject].subClass == 'enemy':
			scan_resolution = 3
			scan_offset = 10
		else:

			scan_offset = 5
			scan_resolution = copy.deepcopy(height) / 8
		scan_step = height / scan_resolution
		scan_point = 0
		scan_depth = 5
		return height, scan_depth, scan_offset, scan_point, scan_step

	def ray_scan_right(self,collisionBuffer,objects,currentObject):

		height, scan_depth, scan_offset, scan_point, scan_step = self.configure_scan_variables_lr(collisionBuffer, currentObject)
		while scan_point <= height - scan_offset:

			if objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomright[0] + scan_depth,  collisionBuffer[currentObject].rect.top + scan_point ):
				collisionBuffer[currentObject].collisionSubClass = objects.subClass
				collisionBuffer[currentObject].collisionRight = True
				break
			scan_point += scan_step

	def ray_scan_up(self,collisionBuffer,objects,currentObject):

		scan_depth, scan_point, scan_step, width = self.configure_scan_variables_ud(collisionBuffer, currentObject)

		while scan_point <= width:

			if objects.rect.collidepoint(collisionBuffer[currentObject].rect.topleft[0] + scan_point,collisionBuffer[currentObject].rect.top - scan_depth ):

				if collisionBuffer[currentObject].rect.colliderect(objects.rect):
					collisionBuffer[currentObject].collisionSubClass = objects.subClass
					collisionBuffer[currentObject].collisionUp = True
					break
			scan_point += scan_step

	def updateRectPosition(self,collisionObject):
		collisionObject.rect.x = collisionObject.position[0]

		collisionObject.rect.y = collisionObject.position[1]
