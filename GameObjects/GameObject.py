
import pygame

class _GameObject:


	def __init__(self):
		#Object stupid subclass 
		#[player,platform,enemy]
		self.subClass = ''

		#Sprite Data
		self.image = None
		self.sprite_size = [0,0]
		self.rect = None
		self.imagePath=''
		self.animation_state = 0
		self.position = pygame.math.Vector2(0,0)
		self.initial_position = pygame.math.Vector2(0,0)
		self.isRendered = False
		self.scrollOffset = 0
		self.image_mask = None
		#Physics Data
		self.weight = 10
		self.maxHorizontalVelocity = 10
		self.velocity_Y2 = 0
		self.velocity_Y1 = 0
		self.jump_velocity_1 = 0
		self.jump_velocity_2 = 0
		self.jump_velocity = 400
		self.jump_decelleration = 20
		self.velocityX = 0
		self.velocity_X2 = 0
		self.velocity_X1 = 0
		self.accelerationX = 1500
		self.accelerationY = 0
		self.forceY = 0
		self.mass = 100
		self.jumping = False
		self.x_direction = 1
		self.x_speed = 1
		self.y_displacement =0
		self.pause_physics = False
		self.scrolling = False

		
		#Collision Data
		self.collisionDown = False
		self.collisionLeft = False
		self.collisionRight= False
		self.collisionUp = False
		self.onEnemy = False
		self.isHit = False
		self.collisionSubClass = None
		self.collisionObjDirection = 0
		self.collisionObject = None
		self.hit = False

		# [0 = up , 1 = down, 2 = left, 3 = right]
		self.pixelCollisionMap = (list(),list(),list(),list())
		self.item = None

		#Audio Data
		self.audioFootSteep = None
		self.audioAttack = None
		self.audioTakeDamage = None
		self.audioJump = None

	'''SETTERS'''
	def _set_image_path(self,imagePath):
	
		self.imagePath = imagePath

	def _set_image(self):
		self.image = pygame.image.load(self.imagePath).convert_alpha()

	def _set_weight(self,weight):
		self.weight = weight

	def _set_max_horizontal_velocity(self,maxHorizontalVelocity):
		self.maxHorizontalVelocity = maxHorizontalVelocity

	def _set_jump_force(self,jumpForce):
		self.jumpForce = jumpForce

	def _set_position(self,position):
		self.position = position

	def _set_max_jump_height(self,maxJumpHeight):
		self.maxJumpHeight = maxJumpHeight

	def _set_sub_class(self,subClass):
		self.subClass = subClass
	
	def _set_velocityX(self,velocityX):
		self.velocityX = velocityX

	def _set_accelerationX(self,accelerationX):
		self.accelerationX = accelerationX

	def _set_sprite_size(self,image):
		self.sprite_size = image.get_size()

	def _set_rect(self,sprite_size):
		self.rect = pygame.Rect(self.position[0],self.position[1],sprite_size[0],sprite_size[1])

	def _set_init_xPos(self,x_position):
		self.initial_position[0] = x_position

	def _set_init_yPos(self,y_position):
		self.initial_position[1] = y_position	

	def _set_mask(self):
		self.image_mask = pygame.mask.from_surface(self.image)

	def _set_pixel_collision_map(self):
		i = 0
		#up pixels
		while i < 4:

			for x in range (self.rect.width):
				pixel_color = self.image.get_at((x,i))
				if pixel_color[3] > 0:
					self.pixelCollisionMap[0].append((x,i))
			i+=1

		#down pixels
		i = 1
		while i < 2:

			for x in range (self.rect.width):
				pixel_color = self.image.get_at((x,self.rect.height-i))
				if pixel_color[3] > 0:
					self.pixelCollisionMap[1].append((x,self.rect.height-i))
			i+= 1
		#left pixels
		#ight pixels


	'''GETTERS'''
	def _get_weight(self):
		return self.weight

	def _get_max_horizontal_velocity(self):
		return self.maxHorizontalVelocity

	def _get_jump_force(self):
		return self.jumpForce

	def _get_image_path(self):

		return self.imagePath	

	def _get_position(self):

		return self.position

	def _get_max_jump_height(self):
		return self.maxJumpHeight

	def _get_sub_class(self):
		return self.subClass

	def _get_velocityX(self):
		return self.velocityX

	def _get_accelerationX(self):
		return self.accelerationX

	def _get_pixel_collision_map(self):
		return self.pixelCollisionMap