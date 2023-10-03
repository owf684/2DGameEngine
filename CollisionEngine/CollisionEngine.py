import copy
import sys
sys.path.append("./GameObjects")
import BlockObject

class _CollisionEngine:

	def __init__(self):

		self.collision = False
		self.collisionLeft = False
		self.collisionRight = False
		self.collisionDown = False
		self.threadStarted = False
		self.screen = None
		self.collisionThread = list()
	def main_loop(self,objects ,GraphicsEngine,input_dict,screen):
		self.screen = screen
		i = 0
		currentObject = 0
		# Reset collisions here please!
		objects.collisionDown = False
		objects.collisionLeft = False
		objects.collisionRight = False
		objects.collisionUp = False

		for objs in GraphicsEngine.render_buffer:

			try:

				self.updateRectPosition(objects)
				if objects != objs:
					if (objects.subClass == 'player' or objects.subClass == 'enemy' or objects.subClass == 'powerup') and objs.subClass != 'environment':
						self.detectCollisions(objects, objs)
			except:
				pass


	def detectCollisions(self, objects, objs ):

		self.ray_scan_left(objects, objs)
		self.ray_scan_right(objects, objs)
		self.mask_scan_up(objects, objs)
		self.mask_scan_down(objects, objs)

	def mask_scan_up(self, objects, objs):
		if objects.rect.colliderect(objs.rect):
			if objects.rect.top < objs.rect.bottom:
				if objects.rect.bottom > objs.rect.bottom:
					if objects.rect.bottom > objs.rect.top:
						objects._set_mask()
						objs._set_mask()
						if objects.image_mask.overlap(objs.image_mask, (
						objects.position[0] - objs.position[0],
						objects.position[1] - objs.position[1])):
							objects.collisionSubClass = objs.subClass
							objects.collisionObjDirection = objs.x_direction
							objects.collisionObject = objs
							objects.collisionUp = True
							if isinstance(objs,BlockObject._BlockObject):
								objs.hit = True


	def mask_scan_down(self, objects ,objs):
		if objects.rect.colliderect(objs.rect):
			if objects.rect.bottom > objs.rect.top:
				if objects.rect.top < objs.rect.bottom:
					if objects.rect.top < objs.rect.top:
						if objects.rect.centery+5 < objs.rect.centery:
							objects._set_mask()
							objs._set_mask()
							if objects.image_mask.overlap(objs.image_mask, (objs.position[0] - objects.position[0],objs.position[1] - objects.position[1] )):
								objects.position[1] = objs.rect.top - objects.rect.height
								objects.collisionDown = True
								objects.collisionObject = objs
								if objs.subClass == 'enemy' and objects.subClass == "player":
									objects.onEnemy = True
									objs.isHit = True

	def ray_scan_left(self, objects, objs):
	
		height, scan_depth, scan_offset, scan_point, scan_step = self.configure_scan_variables_lr(objects)
		if objs.subClass == 'enemy' and objects.subClass != 'enemy' or objs.subClass == 'powerup':
			scan_depth = 0
		while scan_point <= height - scan_offset:
			if objects.rect.collidepoint(objects.rect.bottomleft[0] - scan_depth,objects.rect.top + scan_point ):
				objects.collisionSubClass = objs.subClass
				objects.collisionObjDirection = objs.x_direction
				objects.collisionObjects = objs
				objects.collisionLeft = True

			scan_point += scan_step

	def ray_scan_right(self, objects, objs):

		height, scan_depth, scan_offset, scan_point, scan_step = self.configure_scan_variables_lr(objects)
		if objs.subClass == 'enemy' and objects.subClass != 'enemy' or objs.subClass == 'powerup':
			scan_depth = 0
		while scan_point <= height - scan_offset:

			if objects.rect.collidepoint(objects.rect.bottomright[0] + scan_depth,  objects.rect.top + scan_point ):
				objects.collisionSubClass = objs.subClass
				objects.collisionObjDirection = objs.x_direction
				objects.collisionObject = objs
				objects.collisionRight = True

			scan_point += scan_step


	def configure_scan_variables_lr(self, objects):
	
		height = copy.deepcopy(objects.rect.height)
		if objects.subClass != 'player':
			scan_resolution = 3
			scan_offset = 5
		else:
			scan_offset = 10
			scan_resolution = copy.deepcopy(height)/8

		scan_depth = 10
		scan_step = height / scan_resolution
		scan_point = 0
		return height, scan_depth, scan_offset, scan_point, scan_step


	def updateRectPosition(self,collisionObject):
	
		collisionObject.rect.x = collisionObject.position[0]
		collisionObject.rect.y = collisionObject.position[1]
