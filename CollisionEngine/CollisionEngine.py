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

					if collisionBuffer[currentObject].subClass == 'player' or collisionBuffer[currentObject].subClass == 'enemy':

		
						self.detectCollisions(collisionBuffer,objects,currentObject)
						#self.collisionThread.append(threading.Thread(target=self.detectCollisions, args=(collisionBuffer,objects,currentObject,)))
						#self.collisionThread[-1].start()

		
			currentObject += 1
			#for processes in self.collisionThread:
				#processes.join()
			#self.collisionThread.clear()
	
	def detectCollisions(self,collisionBuffer,objects,currentObject):
		
		self.ray_scan_left(collisionBuffer,objects,currentObject)
		self.ray_scan_right(collisionBuffer,objects,currentObject)
		self.ray_scan_up(collisionBuffer,objects,currentObject)
		self.ray_scan_down(collisionBuffer,objects,currentObject)


	def ray_scan_down(self,collisionBuffer,objects,currentObject):
		width = copy.deepcopy(collisionBuffer[currentObject].rect.width)
		if collisionBuffer[currentObject].subClass == 'enemy':
			scan_resolution = 3
		else:
			scan_resolution = copy.deepcopy(width)/2
		scan_step = width/scan_resolution
		scan_point = 0
		scan_depth = 2

		while scan_point <= width:

			if objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomleft[0] + scan_point,collisionBuffer[currentObject].rect.bottom + scan_depth ):

				if collisionBuffer[currentObject].rect.colliderect(objects.rect):

					collisionBuffer[currentObject].collisionDown = True
					collisionBuffer[currentObject].position[1] = objects.rect.top - collisionBuffer[currentObject].rect.height
					break

			scan_point += scan_step

	def ray_scan_left(self,collisionBuffer,objects,currentObject):
		height = copy.deepcopy(collisionBuffer[currentObject].rect.height)

		if collisionBuffer[currentObject].subClass == 'enemy':
			scan_resolution = 3
			scan_offset = 10
		else:

			scan_offset = 5
			scan_resolution = copy.deepcopy(height)/2

		scan_step = height/scan_resolution
		scan_point = 0
		scan_depth = 5

		while scan_point <= height - scan_offset:

			if objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomleft[0] - scan_depth,collisionBuffer[currentObject].rect.top + scan_point ):

				collisionBuffer[currentObject].collisionLeft = True
				break

			scan_point += scan_step


	def ray_scan_right(self,collisionBuffer,objects,currentObject):

		height = copy.deepcopy(collisionBuffer[currentObject].rect.height)
		if collisionBuffer[currentObject].subClass == 'enemy':
			scan_offset = 10
			scan_resolution = 3
		else:

			scan_offset = 5
			scan_resolution = copy.deepcopy(height)/2
		scan_step = height/scan_resolution
		scan_point = 0
		scan_depth = 5

		while scan_point <= height - scan_offset:

			if objects.rect.collidepoint(collisionBuffer[currentObject].rect.bottomright[0] + scan_depth,  collisionBuffer[currentObject].rect.top + scan_point ):

				collisionBuffer[currentObject].collisionRight = True
				break
			scan_point += scan_step

	def ray_scan_up(self,collisionBuffer,objects,currentObject):

		width = copy.deepcopy(collisionBuffer[currentObject].rect.width)
		if collisionBuffer[currentObject].subClass == 'enemy':
			scan_resolution = 3
		else:
			scan_resolution = copy.deepcopy(width)/2
		scan_step = width/scan_resolution
		scan_point = 0
		scan_depth = 2

		while scan_point <= width:

			if objects.rect.collidepoint(collisionBuffer[currentObject].rect.topleft[0] + scan_point,collisionBuffer[currentObject].rect.top - scan_depth ):

				if collisionBuffer[currentObject].rect.colliderect(objects.rect):

					collisionBuffer[currentObject].collisionUp = True
					break
			scan_point += scan_step		

	def handle_up_collisions(self,collisionBuffer,objects,currentObject):
		if 	(	objects.rect.collidepoint(collisionBuffer[currentObject].rect.topleft[0]+5,collisionBuffer[currentObject].rect.topleft[1] - 1) or 
				objects.rect.collidepoint(collisionBuffer[currentObject].rect.midtop[0],collisionBuffer[currentObject].rect.midtop[1] - 1) or 
				objects.rect.collidepoint(collisionBuffer[currentObject].rect.topright[0]-5,collisionBuffer[currentObject].rect.topright[1] - 1)

			):
			collisionBuffer[currentObject].collisionUp = True



	def updateRectPosition(self,collisionObject):
		collisionObject.rect.x = collisionObject.position[0]
		
		collisionObject.rect.y = collisionObject.position[1]
