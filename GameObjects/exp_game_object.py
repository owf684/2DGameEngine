
import pygame
import sys
sys.path.append("./AnimationSystem")
sys.path.append("./GameObjects/CompositionObjects")
import anim_util
import sprite_object
import physics_object
import collider_object
class GameObject(anim_util.AnimUtil):

	def __init__(self):

		super().__init__()
		self.current_sprite = sprite_object.SpriteObject()
		self.idle_sprite    = sprite_object.SpriteObject()	
		self.walking_sprite = sprite_object.SpriteObject()
		self.jump_sprite    = sprite_object.SpriteObject()
		self.death_sprite   = sprite_object.SpriteObject()

		physics = physics_object.PhysicsObject()
		
		collider = collider_object.ColliderObject()

		self.position = [0,0]
		self.initial_position = [0,0]

		self.destroy = False

		#scrolling data
		self.scrollOffset = 0
		self.scrolling = False
		

	
		#Audio Data
		self.audioFootSteep = None
		self.audioAttack = None
		self.audioTakeDamage = None
		self.audioJump = None

	'''SETTERS'''
	def set_image_path(self,imagePath):
	
		self.imagePath = imagePath

	def set_image(self):
		self.image = pygame.image.load(self.imagePath).convert_alpha()

	def set_weight(self,weight):
		self.weight = weight

	def set_max_horizontal_velocity(self,maxHorizontalVelocity):
		self.maxHorizontalVelocity = maxHorizontalVelocity

	def set_jump_force(self,jumpForce):
		self.jumpForce = jumpForce

	def set_position(self,position):
		self.position = position

	def set_max_jump_height(self,maxJumpHeight):
		self.maxJumpHeight = maxJumpHeight

	def set_sub_class(self,subClass):
		self.subClass = subClass
	
	def set_velocityX(self,velocityX):
		self.velocityX = velocityX

	def set_accelerationX(self,accelerationX):
		self.accelerationX = accelerationX

	def set_sprite_size(self,image):
		self.sprite_size = image.get_size()

	def set_rect(self,sprite_size):
		self.rect = pygame.Rect(self.position[0],self.position[1],sprite_size[0],sprite_size[1])
	
	def set_hit_box(self, sprite_size, y_offset):
		self.hit_box = pygame.Rect(self.position[0], self.position[1]- y_offset, sprite_size[0],sprite_size[1]/2)

	def set_kill_box(self, sprite_size, y_offset):
		self.kill_box = pygame.Rect(self.position[0], self.position[1]+ y_offset, 16,sprite_size[1]/4)
	
	def set_init_xPos(self,x_position):
		self.initial_position[0] = x_position

	def set_init_yPos(self,y_position):
		self.initial_position[1] = y_position	

	def set_mask(self):
		self.image_mask = pygame.mask.from_surface(self.image)

	'''GETTERS'''
	def get_weight(self):
		return self.weight

	def get_max_horizontal_velocity(self):
		return self.maxHorizontalVelocity

	def get_jump_force(self):
		return self.jumpForce

	def get_image_path(self):

		return self.imagePath	

	def get_position(self):

		return self.position

	def get_max_jump_height(self):
		return self.maxJumpHeight

	def get_sub_class(self):
		return self.subClass

	def get_velocityX(self):
		return self.velocityX

	def get_accelerationX(self):
		return self.accelerationX

	
