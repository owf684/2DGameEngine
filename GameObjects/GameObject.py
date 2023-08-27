
import pygame

class _GameObject:


	def __init__(self):
		#Object stupid subclass 
		#[player,platform,enemy]
		self.subClass = ''

		#Sprite Data
		self.image = None
		self.imagePath=''
		self.animation_state = 0
		self.position = [0,0]

		#Physics Data
		self.weight = 10
		self.maxHorizontalVelocity = 1000
		self.horizontalVelocity = 10
		self.jumpForce = 10
		self.maxJumpHeight = 10

		#Audio Data
		self.audioFootSteep = None
		self.audioAttack = None
		self.audioTakeDamage = None
		self.audioJump = None

	'''SETTERS'''
	def _set_image_path(self,imagePath):
	
		self.imagePath = imagePath

	def _set_image(self):
		self.image = pygame.image.load(self.imagePath)

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
	
	def _set_horizontal_velocity(self,horizontalVelocity):
		self.horizontalVelocity = horizontalVelocity

	'''GETTERS'''
	def _get_weight(self):
		return self.get_weight

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
	def _get_horizontal_velocity(self):
		return self.horizontalVelocity
