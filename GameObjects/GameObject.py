
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
		self.hit_box = None
		self.kill_box = None
		self.imagePath=''
		self.animation_state = 0
		self.position = pygame.math.Vector2(0,0)
		self.initial_position = pygame.math.Vector2(0,0)
		self.isRendered = False
		self.image_mask = None
		self.power_up = 0

		#scrolling data
		self.scrollOffset = 0
		self.scrolling = False

		#Physics Data
		self.velocityX = 0
		self.velocityY = 0
		self.accelerationX = 1500
		self.accelerationY = 0
		self.forceX = 0
		self.forceY = 0
		self.mass = 100
		self.jumping = False
		self.x_direction = 1
		self.x_displacement = 0
		self.y_displacement =0
		self.pause_physics = False

		
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
	
	def _set_hit_box(self, sprite_size, y_offset):
		self.hit_box = pygame.Rect(self.position[0], self.position[1]- y_offset, sprite_size[0],sprite_size[1]/2)

	def _set_kill_box(self, sprite_size, y_offset):
		self.kill_box = pygame.Rect(self.position[0], self.position[1]+ y_offset, 26,sprite_size[1]/2)
	
	def _set_init_xPos(self,x_position):
		self.initial_position[0] = x_position

	def _set_init_yPos(self,y_position):
		self.initial_position[1] = y_position	

	def _set_mask(self):
		self.image_mask = pygame.mask.from_surface(self.image)

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